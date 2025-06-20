from http.server import HTTPServer, BaseHTTPRequestHandler
import json

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
            try:
                data = json.loads(post_data.decode('utf-8'))
                print("[+] Received client info:")
                print(json.dumps(data, indent=2))
                self.send_response(200)
                _set_cors_headers(self)
                self.end_headers()
                self.wfile.write(b"Info received.")
            except json.JSONDecodeError:
                self.send_response(400)
                _set_cors_headers(self)
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
        else:
            self.send_error(404, 'Not Found')

def run():
    server_address = ('0.0.0.0', 8000)
    httpd = HTTPServer(server_address, CatcherHandler)
    print("[*] Server running on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

