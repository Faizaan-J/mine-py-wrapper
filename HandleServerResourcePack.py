import http.server
import socketserver
import threading
import os

import ConfigHandler
import Logger

def start_resource_pack_server():
    def log_message(level: Logger.LogLevel, *args):
        Logger.Log(level, f"CDN: {' '.join(str(arg) for arg in args)}")

    server_resource_pack = ConfigHandler.config["server_resource_pack"]

    pack_path = server_resource_pack["path"]

    ip = server_resource_pack["ip"]
    if ip == "localhost":
        ip = "127.0.0.1"
    if ip in [None, ""]:
        ip = "0.0.0.0"
    
    port = server_resource_pack["port"]

    file_name = os.path.basename(pack_path)

    def run():
        class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            daemon_threads = True
            allow_reuse_address = True

        class RPHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                log_message(Logger.LogLevel.INFO, args)

            def do_GET(self):
                with open(pack_path, 'rb') as f:
                    self.send_response(200)
                    self.send_header("Content-Type", "application/zip")
                    self.send_header("Content-Disposition", f'attachment; filename="{file_name}"')
                    fstats = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fstats.st_size))
                    self.end_headers()
                    
                    Supports_Sendfile = hasattr(os, 'sendfile')

                    if Supports_Sendfile:
                        sent = 0
                        while sent < fstats.st_size:
                            sent += os.sendfile(self.wfile.fileno(), f.fileno(), sent, fstats.st_size - sent)
                    else:
                        f.seek(0)
                        chunk = f.read(64 * 1024)
                        while chunk:
                            self.wfile.write(chunk)
                            chunk = f.read(64 * 1024)

                    f.close()

        with ThreadingTCPServer((ip, port), RPHandler) as httpd:
            log_message(Logger.LogLevel.INFO, f"Resource pack server running at http://{ip}:{port}")
            httpd.serve_forever()

    threading.Thread(target=run, daemon=True).start()

start_resource_pack_server()