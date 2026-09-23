"""Declared benign native approval Provider; no upstream; fixed Runtime remains the approval authority."""
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
ledger = json.loads(a.ledger.read_text()) if a.ledger.exists() else {'provider': 'declared_local_fixture', 'real_calls': 0, 'requests': []}


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
            if len(ledger['requests']) >= 6:
                self.send_error(429)
                return
            ledger['requests'].append({'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'model': body['model'], 'fixture': 'normal_native_approval'})
            a.ledger.write_text(json.dumps(ledger, indent=2) + '\n')
        item = {'id': 'message_single_local_' + str(len(ledger['requests'])), 'type': 'message', 'role': 'assistant', 'phase': 'final_answer', 'status': 'completed', 'content': [{'type': 'output_text', 'text': 'FEAT155 本机交互验收完成', 'annotations': []}]}
        # A declared ordinary tool result, not a fabricated approval event.
        # It requests only /usr/bin/true; the UI verifier will deny it.
        def names(tools):
            result = []
            for tool in tools:
                if isinstance(tool, dict):
                    if tool.get('name'):
                        result.append(tool['name'])
                    result.extend(names(tool.get('tools', [])))
            return result
        tool_names = names(body.get('tools', []))
        if len(ledger['requests']) == 3:
            ledger['requests'][-1]['available_tool_names'] = tool_names
            a.ledger.write_text(json.dumps(ledger, indent=2) + '\n')
            if 'exec_command' not in tool_names:
                item['content'][0]['text'] = 'Declared fixture: exec_command was not offered; no approval request was fabricated.'
            else:
                item = {'id': 'fc_declared_approval_3', 'type': 'function_call', 'name': 'exec_command', 'call_id': 'call_declared_approval_3', 'status': 'completed', 'arguments': json.dumps({'cmd': '/usr/bin/true', 'login': False, 'sandbox_permissions': 'require_escalated', 'justification': '是否批准本次无文件和网络副作用的 true 命令？'})}
        elif len(ledger['requests']) == 4:
            item['content'][0]['text'] = '声明式本机 Provider 已收到工具响应；请以原生审批和工具记录为准。'
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
            time.sleep(0.1)
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
