"""Declared local text Provider for native UI composition; never contacts upstream."""
import argparse
import http.server
import json
from pathlib import Path
import threading
import time

p = argparse.ArgumentParser()
p.add_argument('--ledger', type=Path, required=True)
a = p.parse_args()
lock = threading.Lock()
ledger = {'provider': 'declared_local_fixture', 'real_calls': 0, 'requests': []}


class Provider(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        if self.path != '/v1/responses':
            self.send_error(404)
            return
        length = int(self.headers.get('Content-Length', '0'))
        if not 0 < length <= 32 * 1024 * 1024:
            self.send_error(400)
            return
        body = json.loads(self.rfile.read(length))
        if body.get('model') != 'MiniMax-M3':
            self.send_error(400)
            return
        with lock:
            if len(ledger['requests']) >= 2:
                self.send_error(429)
                return
            ledger['requests'].append({'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'model': body['model']})
            a.ledger.write_text(json.dumps(ledger, indent=2) + '\n')
        item = {'id': 'message_single_local_' + str(len(ledger['requests'])), 'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'status': 'completed', 'content': [{'type': 'output_text', 'text': '4C3 本机单次与重跑验证完成', 'annotations': []}]}
        events = [
            {'type': 'response.created', 'response': {'id': 'response_single_local_' + str(len(ledger['requests'])), 'status': 'in_progress', 'output': []}},
            {'type': 'response.output_item.added', 'output_index': 0, 'item': item},
            {'type': 'response.output_item.done', 'output_index': 0, 'item': item},
            {'type': 'response.completed', 'response': {'id': 'response_single_local_' + str(len(ledger['requests'])), 'status': 'completed', 'output': [item], 'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}},
        ]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event, ensure_ascii=False) + '\n\n').encode())
            self.wfile.flush()


a.ledger.write_text(json.dumps(ledger, indent=2) + '\n')
server = http.server.ThreadingHTTPServer(('127.0.0.1', 18083), Provider)
print('Declared local Provider ready; upstream requests are impossible.', flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    server.server_close()
