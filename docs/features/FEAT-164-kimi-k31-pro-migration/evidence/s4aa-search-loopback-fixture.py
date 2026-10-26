"""Ordinary public search metadata, loopback only; no external HTTP client."""
import hashlib
import http.server
import json
import threading
from pathlib import Path

root = Path(__file__).resolve().parent
source = root.parent / 'feat164-s4aa-qualification-20261027/yijie-contracts/tests/fixtures/agent/native-search-sources/ordinary-url-components.json'
cases = json.loads(source.read_text())['cases'][:20]
ledger_path = root / 'loopback-ledger.json'
assert not ledger_path.exists()
ledger = {'scope': 'S4AA synthetic URL projection only', 'attempts': 0, 'requests': [], 'external_requests': 0, 'state': 'starting', 'limit': 2, 'fixture_sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
lock = threading.Lock()

def save():
    ledger_path.write_text(json.dumps(ledger, indent=2) + '\n')

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_GET(self):
        if self.path != '/health':
            self.send_error(404)
            return
        data = json.dumps({'fixture': 'S4AA_LOOPBACK_ONLY', 'attempts': ledger['attempts'], 'external_requests': 0}).encode()
        self.send_response(200)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if self.path == '/shutdown':
            self.send_response(204)
            self.end_headers()
            threading.Thread(target=self.server.shutdown).start()
            return
        if self.path != '/v1/responses':
            self.send_error(404)
            return
        with lock:
            ledger['attempts'] += 1
            save()
        size = int(self.headers.get('Content-Length', '0'))
        if not 0 < size <= 1024 * 1024:
            self.send_error(400)
            return
        body = json.loads(self.rfile.read(size))
        if ledger['attempts'] > 2 or body.get('model') != 'kimi-k3.1-pro' or (body.get('reasoning') or {}).get('effort') != 'max' or self.headers.get('Authorization') != 'Bearer feat164-local-dummy':
            self.send_error(400)
            return
        title = set((((body.get('text') or {}).get('format') or {}).get('schema') or {}).get('properties', {})) == {'title'}
        number = ledger['attempts']
        output = []
        if not title:
            output.append({'id': f'ws_s4aa_{number}', 'type': 'web_search_call', 'status': 'completed', 'action': {'type': 'search', 'query': 'FEAT164_S4AA 普通公开来源本机复验', 'sources': [{'type': 'url', 'url': c['url'], 'title': f'普通公开来源 {i+1}'} for i, c in enumerate(cases)]}})
        output.append({'id': f'msg_s4aa_{number}', 'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'status': 'completed', 'content': [{'type': 'output_text', 'text': json.dumps({'title': 'S4AA来源离线复验'}, ensure_ascii=False) if title else 'FEAT164 S4AA 来源离线验证完成。这是合成响应，未访问真实模型或搜索服务。', 'annotations': []}]})
        with lock:
            ledger['requests'].append({'model': body['model'], 'effort': 'max', 'title': title, 'source_count': 0 if title else 20, 'request_sha256': hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()})
            save()
        rid = f'resp_s4aa_{number}'
        events = [{'type': 'response.created', 'response': {'id': rid, 'status': 'in_progress', 'output': []}}]
        for index, item in enumerate(output):
            events.extend([{'type': 'response.output_item.added', 'output_index': index, 'item': item}, {'type': 'response.output_item.done', 'output_index': index, 'item': item}])
        events.append({'type': 'response.completed', 'response': {'id': rid, 'status': 'completed', 'output': output, 'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}})
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())
            self.wfile.flush()

server = http.server.ThreadingHTTPServer(('127.0.0.1', 18083), Handler)
ledger['state'] = 'running'
save()
print('S4AA loopback fixture ready', flush=True)
try:
    server.serve_forever()
finally:
    server.server_close()
    ledger['state'] = 'stopped_normally'
    save()
