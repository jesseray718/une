#!/data/data/com.termux/files/usr/bin/bash
pkill -f "UnifiedJSONRPCHandler" || true
sleep 1
python3 -c "
import http.server
import socketserver
import json
import sys
sys.path.append('\$HOME/une/src')
from une.une_atomic_library import *

SECRET_TOKEN = 'une-local-token-2026'

class UnifiedJSONRPCHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            req = json.loads(body)
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            if token != SECRET_TOKEN:
                self._error(-32001, 'Unauthorized')
                return
            if req.get('jsonrpc') != '2.0':
                self._error(-32600, 'Invalid Request')
                return
            method = req.get('method')
            params = req.get('params', {})
            rid = req.get('id')
            if method in ['unified_effective_power', 'unified_power_acceleration', 
                          'global_grid_mass', 'transmission_loss_mass']:
                result = globals()[method](**params)
            else:
                result = {'error': 'Method not supported in this build'}
            self._reply({'jsonrpc': '2.0', 'result': result, 'id': rid})
        except Exception as e:
            self._error(-32603, str(e))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'UNE Server'}).encode())

    def _reply(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _error(self, code, message):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'jsonrpc': '2.0', 'error': {'code': code, 'message': message}}).encode())

print('Persistent UNE JSON-RPC Server started on port 8080')
with socketserver.TCPServer(('127.0.0.1', 8080), UnifiedJSONRPCHandler) as httpd:
    httpd.serve_forever()
" &
echo "Server running in background"
