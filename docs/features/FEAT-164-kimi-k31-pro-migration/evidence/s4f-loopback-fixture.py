#!/usr/bin/env python3
"""FEAT-164 S4 App fixture. Synthetic local Responses only; no external client.

Serves ordinary explicit cases and existing local artifact publication. Never
reads credentials, invokes tools itself, changes app data, or forwards traffic.
"""
import argparse
import hashlib
import http.server
import json
import threading
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--ledger', type=Path, required=True)
a = parser.parse_args()
assert not a.ledger.exists(), 'Use a fresh offline ledger; never overwrite an old one'
lock = threading.Lock()
ledger = {'scope': 'FEAT-164 S4F synthetic App acceptance, not real model qualification', 'external_requests': 0, 'attempts': 0, 'requests': [], 'rejected': [], 'state': 'starting', 'limit': 16}
profiles = {'kimi-k3.1-pro': ('feat164-build-only-dummy', 'max'), 'MiniMax-M3': ('feat164-build-only-dummy', 'high')}

def save():
    a.ledger.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')

def text_item(text):
    return {'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'status': 'completed', 'content': [{'type': 'output_text', 'text': text, 'annotations': []}]}

def text_parts(value):
    if isinstance(value, dict):
        if value.get('type') in ('text', 'input_text') and isinstance(value.get('text'), str):
            yield value['text']
        for child in value.values():
            yield from text_parts(child)
    elif isinstance(value, list):
        for child in value:
            yield from text_parts(child)

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass
    def do_GET(self):
        if self.path != '/health':
            self.send_error(404)
            return
        with lock:
            raw = json.dumps({'fixture': 'FEAT164_S4F_LOOPBACK_ONLY', 'requests': len(ledger['requests']), 'attempts': ledger['attempts'], 'rejected': len(ledger['rejected']), 'external_requests': 0}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
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
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 < size <= 1024 * 1024:
                raise ValueError('bounded request required')
            body = json.loads(self.rfile.read(size))
            profile = profiles.get(body.get('model'))
            if profile is None or self.headers.get('Authorization') != 'Bearer ' + profile[0] or (body.get('reasoning') or {}).get('effort') != profile[1]:
                raise ValueError('profile mismatch')
            if ledger['attempts'] > ledger['limit']:
                raise ValueError('offline request limit')
            schema = ((body.get('text') or {}).get('format') or {}).get('schema') or {}
            user_inputs = [x for x in body.get('input', []) if isinstance(x, dict) and x.get('role') == 'user']
            prompt = '\n'.join(text_parts(user_inputs[-1:]))
            kind = next((name for name in ('DRAFT', 'PLAN_RUN', 'MINIMAX', 'KIMI', 'REOPEN', 'PAUSED') if 'FEAT164_S4F_' + name in prompt), 'ordinary')
            response_kind = 'text'
            if set(schema.get('properties', {})) == {'title'}:
                item = text_item(json.dumps({'title': 'S4本机合成验收'}, ensure_ascii=False))
                response_kind = 'title'
            else:
                item = text_item('FEAT164 S4F 本机验收完成。这是合成响应，未访问真实模型。')
                if kind == 'DRAFT':
                    if body.get('tools') != []:
                        raise ValueError('draft must be input-only')
                    item = text_item(json.dumps({'schema_version': 1, 'kind': 'candidate', 'name': 'FEAT164 S4F 安全离线计划', 'content': 'FEAT164_S4F_PLAN_RUN 请回复本机计划验证完成，不调用工具。', 'schedule': {'frequency': 'daily', 'time_zone': 'Asia/Shanghai', 'local_time': '23:59'}, 'target': {'mode': 'dedicated_chat'}}, ensure_ascii=False))
                    response_kind = 'draft_candidate'
                elif kind == 'ordinary':
                    raise ValueError('explicit S4F case marker required')
        except (ValueError, KeyError, TypeError, AttributeError):
            with lock:
                ledger['rejected'].append({'attempt': ledger['attempts'], 'reason': 'invalid local fixture request'})
                save()
            self.send_error(400, 'Local synthetic fixture rejected the request')
            return
        with lock:
            number = len(ledger['requests']) + 1
            ledger['requests'].append({'ordinal': number, 'model': body['model'], 'effort': profile[1], 'case': kind, 'response_kind': response_kind, 'request_sha256': hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest(), 'tool_count': len(body.get('tools', [])), 'input_only': body.get('tools') == []})
            save()
        item['id'] = f'feat164_s4f_item_{number}'
        rid = f'feat164_s4f_response_{number}'
        events = [{'type': 'response.created', 'response': {'id': rid, 'status': 'in_progress', 'output': []}}, {'type': 'response.output_item.added', 'output_index': 0, 'item': item}, {'type': 'response.output_item.done', 'output_index': 0, 'item': item}, {'type': 'response.completed', 'response': {'id': rid, 'status': 'completed', 'output': [item], 'usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}}]
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.end_headers()
        for event in events:
            self.wfile.write(('data: ' + json.dumps(event) + '\n\n').encode())
            self.wfile.flush()

server = http.server.ThreadingHTTPServer(('127.0.0.1', 18083), Handler)
ledger['state'] = 'running'
save()
print('FEAT164 S4F loopback fixture ready; external requests impossible in this fixture', flush=True)
try:
    server.serve_forever()
finally:
    server.server_close()
    ledger['state'] = 'stopped_normally'
    save()
