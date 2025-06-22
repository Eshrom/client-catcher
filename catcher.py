from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

def _set_cors_headers(handler):
    handler.send_header('Access-Control-Allow-Origin', '*')
    handler.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
    handler.send_header('Access-Control-Allow-Headers', 'Content-Type')

class CatcherHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        _set_cors_headers(self)
        self.end_headers()

    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            print("[Raw POST data]:", post_data.decode('utf-8', errors='replace'))

            try:
                data = json.loads(post_data.decode('utf-8'))
                print("[+] Parsed client info:")
                for k, v in data.items():
                    print(f"  {k}: {v}")
            except Exception as e:
                print(f"[!] JSON decode error: {e}")

            self.send_response(200)
            _set_cors_headers(self)
            self.end_headers()
            self.wfile.write(b"Info received.")
        else:
            self.send_response(404)
            _set_cors_headers(self)
            self.end_headers()
            self.wfile.write(b"Not Found")

def run():
    port = int(os.environ.get('PORT', 8000))
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, CatcherHandler)
    print(f"[*] Server running on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
