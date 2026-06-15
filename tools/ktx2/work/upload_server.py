import os, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
SAVE = r"E:\GitHub\Dev\Ramen-Shop\tools\ktx2\work"

class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        name = os.path.basename(q.get('name', ['upload.bin'])[0])
        n = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(n)
        with open(os.path.join(SAVE, name), 'wb') as f:
            f.write(data)
        self.send_response(200); self.cors(); self.end_headers(); self.wfile.write(b'ok')
    def log_message(self, *a):
        pass

print("upload server on :9999 ->", SAVE, flush=True)
ThreadingHTTPServer(('0.0.0.0', 9999), H).serve_forever()
