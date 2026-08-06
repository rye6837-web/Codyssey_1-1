import http.server
import os
import socketserver

PORT = int(os.environ.get("APP_PORT", 8080))
MESSAGE = os.environ.get("APP_MESSAGE", "Hello from Codyssey custom image")

class AppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/index.html"]:
            content = f"""
<html>
<head><meta charset='utf-8'><title>Codyssey Custom Image</title></head>
<body>
<h1>{MESSAGE}</h1>
<p>Custom Linux base image with user, environment variable, and health check.</p>
<ul>
<li>USER: {os.environ.get('USER', 'unknown')}</li>
<li>APP_PORT: {PORT}</li>
</ul>
</body>
</html>
"""
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Content-length", str(len(content.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), AppHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
