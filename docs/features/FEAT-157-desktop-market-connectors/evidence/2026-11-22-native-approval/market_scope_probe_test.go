// Run as an added test in yijie-agent-host/internal/codex with go test -overlay.
// This probe uses the pinned Runtime, a temporary Home and loopback model/MCP
// peers. The product market Worker is covered separately by its integration test.
package codex

import (
	"context"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"slices"
	"sync/atomic"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pelletier/go-toml/v2"
)

// Match the conservative annotations of a generic market tool. All this peer
// can actually do is count a lookup of the fixed local value blue.
func nativeScopeProbePeer(t *testing.T, calls *atomic.Int64) *httptest.Server {
	t.Helper()
	peer := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var req struct {
			ID     json.RawMessage
			Method string
			Params json.RawMessage
		}
		if r.Method != http.MethodPost || json.NewDecoder(r.Body).Decode(&req) != nil {
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		if len(req.ID) == 0 {
			w.WriteHeader(http.StatusAccepted)
			return
		}
		var result any
		switch req.Method {
		case "initialize":
			result = map[string]any{
				"protocolVersion": "2025-11-25", "capabilities": map[string]any{"tools": map[string]any{}},
				"serverInfo": map[string]string{"name": "ordinary-catalog", "version": "1"},
			}
		case "tools/list":
			result = map[string]any{"tools": []any{map[string]any{
				"name": "ordinary_lookup", "description": "Read an ordinary local sample.",
				"annotations": map[string]bool{"readOnlyHint": false, "destructiveHint": true, "openWorldHint": true},
				"inputSchema": map[string]any{
					"type": "object", "additionalProperties": false,
					"properties": map[string]any{"key": map[string]string{"type": "string"}}, "required": []string{"key"},
				},
			}}}
		case "tools/call":
			var p struct {
				Name      string
				Arguments map[string]string
			}
			if json.Unmarshal(req.Params, &p) != nil || p.Name != "ordinary_lookup" || p.Arguments["key"] != "blue" {
				t.Error("unexpected local lookup")
				w.WriteHeader(http.StatusBadRequest)
				return
			}
			calls.Add(1)
			result = map[string]any{"content": []any{map[string]string{"type": "text", "text": "ordinary local result: 42"}}}
		case "ping":
			result = map[string]any{}
		default:
			t.Errorf("unexpected local MCP method %q", req.Method)
			w.WriteHeader(http.StatusBadRequest)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(map[string]any{"jsonrpc": "2.0", "id": req.ID, "result": result})
	}))
	t.Cleanup(peer.Close)
	return peer
}

func TestAuditNativeMarketScopeChoices(t *testing.T) {
	for _, choice := range []string{"session", "always", "full"} {
		t.Run(choice, func(t *testing.T) {
			var calls, prompts atomic.Int64
			peer := nativeScopeProbePeer(t, &calls)
			h := newNativeToolsHarness(t, func(_ *nativeToolsHarness, _ map[string]any, step int64) map[string]any {
				switch step % 3 {
				case 1:
					return feat164AuxTool("", "tool_search", uuid.NewString(), map[string]any{"query": "ordinary local sample lookup", "limit": 1})
				case 2:
					return feat164AuxTool("", "exec", uuid.NewString(), map[string]any{"input": "text(await tools.mcp__yijie_market__ordinary_lookup({key:'blue'}));"})
				default:
					return feat164AuxText("Ordinary lookup completed.")
				}
			}, toolSearchConfig, dailySkillMarkets(t))

			connectUI := func() {
				for _, root := range h.manager.config.SkillMarketplaceRoots {
					if err := h.manager.RegisterSkillMarketplace(context.Background(), root); err != nil {
						t.Fatal(err)
					}
				}
				h.manager.SetSkillSubmissionReady(true)
				h.manager.client.setServerRequestHandler(func(ctx context.Context, req serverRequest) serverRequestResult {
					if req.method != "mcpServer/elicitation/request" {
						return h.manager.handleServerRequest(ctx, req)
					}
					prompts.Add(1)
					var p struct {
						Server string `json:"serverName"`
						Meta   struct {
							Kind    string   `json:"codex_approval_kind"`
							Persist []string `json:"persist"`
						} `json:"_meta"`
					}
					if choice == "full" || json.Unmarshal(req.params, &p) != nil || p.Server != marketServerName ||
						p.Meta.Kind != "mcp_tool_call" || !slices.Contains(p.Meta.Persist, "session") || !slices.Contains(p.Meta.Persist, "always") {
						t.Error("unexpected native approval or missing native scope")
						return serverRequestResult{respond: true, value: map[string]any{"action": "decline"}}
					}
					return serverRequestResult{respond: true, value: map[string]any{
						"action": "accept", "content": map[string]any{}, "_meta": map[string]string{"persist": choice},
					}}
				})
			}
			mode := PermissionAsk
			if choice == "full" {
				mode = PermissionFull
			}
			ctx := WithPermissionMode(feat164AuxCtx(), mode)
			profile, _ := ModelProfile(KimiK31ProfileID)
			start := func() string {
				proxy := map[string]any{"url": peer.URL, "enabled": true, "default_tools_approval_mode": "auto"}
				prepared := &MarketPrepared{Config: map[string]any{
					"mcp_servers": map[string]any{marketServerName: proxy}, "features.tool_call_mcp_elicitation": true,
				}}
				thread, err := h.manager.StartThread(WithMarketPrepared(ctx, prepared), h.cwd)
				if err != nil {
					t.Fatal(err)
				}
				return thread.ID
			}
			lookup := func(thread string) {
				input, err := TextUserInput("Use the ordinary local lookup.")
				if err != nil {
					t.Fatal(err)
				}
				turn, err := h.manager.StartTurnV2(ctx, thread, []UserInput{input}, profile.Effort)
				if err != nil {
					t.Fatal(err)
				}
				status, _, err := h.notifications.waitForTurn(turn.ID, 30*time.Second)
				if err != nil || status != "completed" {
					_ = h.manager.InterruptTurn(context.Background(), thread, turn.ID)
					t.Fatalf("local lookup: status=%q err=%v", status, err)
				}
			}

			connectUI()
			first := start()
			lookup(first)
			afterFirst := prompts.Load()
			lookup(first)
			afterSecond := prompts.Load()
			wantPrompts := int64(1)
			if choice == "full" {
				wantPrompts = 0
			}
			if afterFirst != wantPrompts || afterSecond != wantPrompts || calls.Load() != 2 {
				t.Fatalf("first=%d sameThread=%d calls=%d", afterFirst, afterSecond, calls.Load())
			}

			var config struct {
				Servers map[string]struct {
					Tools map[string]struct {
						ApprovalMode string `toml:"approval_mode"`
					} `toml:"tools"`
				} `toml:"mcp_servers"`
			}
			raw, err := os.ReadFile(filepath.Join(h.home, "config.toml"))
			if err == nil {
				if err := toml.Unmarshal(raw, &config); err != nil {
					t.Fatal("invalid isolated native configuration")
				}
			} else if !os.IsNotExist(err) {
				t.Fatal(err)
			}
			stored := config.Servers[marketServerName].Tools["ordinary_lookup"].ApprovalMode == "approve"
			h.restart(t, h.manager.config)
			connectUI()
			lookup(start())
			if calls.Load() != 3 || (choice == "session" && prompts.Load() != 2) || (choice == "full" && prompts.Load() != 0) {
				t.Fatalf("restart: prompts=%d calls=%d", prompts.Load(), calls.Load())
			}
			// An observation for this build, not an assertion that a future
			// product must keep falling back to session for a dynamic server.
			t.Logf("choice=%s prompts(first/sameThread/freshAfterRestart)=%d/%d/%d persistedToolOverride=%t localCalls=%d",
				choice, afterFirst, afterSecond, prompts.Load(), stored, calls.Load())
		})
	}
}
