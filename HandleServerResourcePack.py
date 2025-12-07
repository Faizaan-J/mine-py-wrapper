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

            def handle(self):
                full_ip = f"{self.client_address[0]}:{self.client_address[1]}"
                self.connection = self.request
                first_few_bytes = self.connection.recv(3, socketserver.socket.MSG_PEEK)
                if (len(first_few_bytes) >= 3 and first_few_bytes[0] == 0x16 and first_few_bytes[1] == 0x03 and (first_few_bytes[2] in (0x00, 0x01, 0x02, 0x03))): # hopefully this works idk apparently this is what an https handshake looks like
                    log_message(Logger.LogLevel.WARNING, f"Rejected connection from {full_ip} for attempting to do an HTTPS handshake on HTTP server.")
                    self.connection.sendall(b"HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nAttempted to do HTTPS Handshake on HTTP port.\r\n\r\n")
                    self.connection.close()
                    return
                return super().handle()

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