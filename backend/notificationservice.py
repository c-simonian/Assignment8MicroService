import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

latest_notification = None

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self, content_type='application/json'):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/notifications':
            self._set_response()
            if latest_notification:
                self.wfile.write(json.dumps([latest_notification]).encode())
            else:
                self.wfile.write(json.dumps([]).encode())

    def do_POST(self):
        global latest_notification
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/notify':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            message = data.get('message', 'Conversion has been completed')
            latest_notification = {'message': message}
            self._set_response()
            self.wfile.write(json.dumps({'status': 'Notification sent'}).encode())

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
