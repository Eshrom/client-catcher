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

            print("[Raw POST data]")
            try:
                decoded = post_data.decode('utf-8')
                print(decoded)
            except UnicodeDecodeError:
                print("[!] Could not decode POST data")
                decoded = None

            try:
                if decoded:
                    data = json.loads(decoded)
                    print("[+] Received client info:")
                    print(json.dumps(data, indent=2))
                else:
                    raise json.JSONDecodeError("No valid data", "", 0)

                self.send_response(200)
                _set_cors_headers(self)
                self.end_headers()
                self.wfile.write(b"Info received.")
            except json.JSONDecodeError as e:
                print(f"[!] JSON Decode Error: {e}")
                self.send_response(400)
                _set_cors_headers(self)
                self.end_he_
