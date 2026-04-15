import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

FILE_NAME = "global_leaderboard.json"

class LeaderboardHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        # Allow Cross-Origin if someone makes a web page for it
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_GET(self):
        if self.path == '/leaderboard':
            self._set_headers()
            data_structure = {"users": {}}
            if os.path.exists(FILE_NAME):
                try:
                    with open(FILE_NAME, 'r') as f:
                        data_structure = json.load(f)
                except:
                    pass
            
            # Format pro klienta
            leaderboard = {}
            for user, info in data_structure.get("users", {}).items():
                leaderboard[user] = info.get("score", 0)
                
            self.wfile.write(json.dumps(leaderboard).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            name = req_data.get("name")
            password = req_data.get("password")
            score = req_data.get("score")
            
            if not name or not password:
                self._set_headers(400)
                self.wfile.write(b'{"error": "Chybi jmeno nebo heslo!"}')
                return
            
            # Load
            data_structure = {"users": {}}
            if os.path.exists(FILE_NAME):
                try:
                    with open(FILE_NAME, 'r') as f:
                        data_structure = json.load(f)
                except:
                    pass
            users = data_structure.setdefault("users", {})
            
            if self.path == '/login':
                if name not in users:
                    self._set_headers(404)
                    self.wfile.write(b'{"success": false, "error": "Ucet neexistuje!"}')
                    return
                if users[name]["password"] != password:
                    self._set_headers(401)
                    self.wfile.write(b'{"success": false, "error": "Spatne heslo!"}')
                    return
                self._set_headers()
                self.wfile.write(b'{"success": true}')
                
            elif self.path == '/register':
                if name in users:
                    self._set_headers(409)
                    self.wfile.write(b'{"success": false, "error": "Prezdivka je uz zabrana!"}')
                    return
                users[name] = {"password": password, "score": 0}
                with open(FILE_NAME, 'w') as f:
                    json.dump(data_structure, f)
                self._set_headers()
                self.wfile.write(b'{"success": true}')
                
            elif self.path == '/leaderboard':
                if name not in users or users[name]["password"] != password:
                    self._set_headers(401)
                    self.wfile.write(b'{"success": false, "error": "Neautorizovano!"}')
                    return
                
                # Update score
                if score is not None and score > users[name].get("score", 0):
                    users[name]["score"] = score
                    with open(FILE_NAME, 'w') as f:
                        json.dump(data_structure, f)
                
                # Návrat tabulky
                leaderboard = {}
                for user, info in data_structure.get("users", {}).items():
                    leaderboard[user] = info.get("score", 0)
                
                self._set_headers()
                self.wfile.write(json.dumps(leaderboard).encode('utf-8'))
            else:
                self._set_headers(404)
                self.wfile.write(b'{"error": "Not Found"}')
                
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=LeaderboardHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting leaderboard server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
