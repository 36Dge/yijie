# FEAT-153 native playground integration notes

Actual upstream page: frontend/packages/workflow/adapter/playground/src/page.tsx -> playground/src/workflow-playground.tsx -> components/workflow-container/index.tsx. The current changes mount the original container, header, toolbar, NodeRenderNew, native forms and float layout.

## Initial effects explicitly bypassed in local profile
- workflow-playground.tsx: useSpaceStore is read but effect returns before fetchSpaces/checkSpaceID/setSpace; inited gate does not block local. No browser identity forged.
- services/workflow-save-service.ts: loadLocalDocument consumes the in-memory adapter snapshot. It does not call globalState.load/loadHistory, loadGlobalVariables, modelsService.load, TriggerService.load or initNodeData of arbitrary registries.
- workflow-playground-context.ts: local static node metadata/templates only; no NodeTemplateList or favorite plugin request. Original native SVG assets imported directly from bot-icons.
- components/workflow-header-info: local does not mount WorkflowReferencesTip; edit modal uses Coze modal/input and changeName, does not mount CreateWorkflowModal upstream transport.
- components/workflow-header: local hides SaaS collaboration/reference/copy actions regardless IS_OPEN_SOURCE.
- components/workflow-container: local does not mount template preview, template panel, database modal, retrieve/modify banners, chat pause sheet; data-compensation auto-save effect skipped.
- preset: encapsulation and operation reporting plugin omitted; test form DI plugin retained because it only registers services, no requests.
- node panel: local catalogue only one text node. Search filters local catalogue and never NodePanelSearch; upstream open-source favorite plugin branch is empty already.
- visible StartTestRunButton local branch opens original float layout slot with native Coze components and adapter test/refreshTest. Upstream useTestRunFlowV2 component is not mounted.
- visible PublishButton local branch reads canPublish and calls adapter.publish; upstream force publication UI/service is not used. No awaited result is treated as success.

## Profile invariants
- LocalWorkflowDocument subclasses the real WorkflowDocumentWithFormat; creation rejects unknown types, duplicates, clones, wrong start/end IDs. No graph editor replacement.
- Local registry is the original Start/TextProcess/End registry filtered at registerDocument, with copy disabled and node debug hidden. No global registry mutation in local branch.
- Copy/paste/import shortcuts and comment toolbar item disabled in local profile. Native add-node panel limits unique type15. Normal upstream behavior remains unchanged.
- Line options local branch allows only start->text and text->end; current native default ports omit explicit IDs. Backend still validates complete graph, duplicate links, refs, limits.
- Start input, text input and end output fields use their native readonly options. Native text processing form hides split and array settings; expression editor remains original, validator permits prefix <=1024 UTF-8 bytes followed by {{input}}.
- Native serializer produces empty allArrayItemConcatChars; local codec removes only this known empty optional field; nonempty arrays throw. It does not filter arbitrary graph data or lines.
- End binding updates only after actual user text create/delete, not initial hydration/reload. No normalization writes to server.

## Lifecycle
- Local adapter is an explicit in-process interface; root keeps contracts/DraftModel/RunModel/CAS/message generations.
- Real onContentChange calls adapter.change; no automatic save/debounce retries. Snapshot is sole success/dirty/status source.
- Same-canvas own-save revision acknowledgements never reload, preserving native undo/selection.
- Clean remote document replacement uses readonly lock, generation/disposed guards and checks current snapshot revision/document/dirty before normalize.
- Real playground.toDispose.onDispose plus React container unmount dispose subscriptions. The nonexistent FlowDocumentContribution onDispose hook was removed.
- Initialization catches failures into loadingError. Native container retains header and explicit return action. Loading becomes false only after document/normalize, then upstream fit waits for real renderer bounds; fitting while hidden loading spinner would have no bounds.

Build and real App qualification pending root execution; these source edits alone are not acceptance evidence.
