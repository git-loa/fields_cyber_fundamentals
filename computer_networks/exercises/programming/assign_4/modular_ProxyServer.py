import socket
import sys

class ProxyServer:
    def __init__(self, server_ip, port=8888):
        self.server_ip = server_ip
        self.port = port
        self.tcp_ser_sock = None

    def start_server(self):
        self.tcp_ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_ser_sock.bind((self.server_ip, self.port))
        self.tcp_ser_sock.listen(5)
        print('Proxy server started on IP:', self.server_ip, 'and port:', self.port)

    def serve_forever(self):
        print('Ready to serve...')
        while True:
            try:
                tcp_cli_sock, addr = self.tcp_ser_sock.accept()
                print('Received a connection from:', addr)
                self.handle_client(tcp_cli_sock)
            except OSError as e:
                print("Error accepting connection:", e)

    def handle_client(self, tcp_cli_sock):
        try:
            message = tcp_cli_sock.recv(1024).decode(encoding="utf-8", errors="ignore")
            print(message)
            method, path, _ = message.split(' ', 2)
            filename = path[1:].replace('/', '_')

            if method == 'GET':
                self.handle_get_request(tcp_cli_sock, path, filename)
            elif method == 'POST':
                content_length = int([line.split(": ")[1] for line in message.split("\r\n") if "Content-Length" in line][0])
                body = tcp_cli_sock.recv(content_length).decode(encoding="utf-8", errors="ignore")
                self.handle_post_request(tcp_cli_sock, path, filename, body)
            else:
                self.send_error_response(tcp_cli_sock, "405 Method Not Allowed")

        except OSError as e:
            print("Error receiving message:", e)
        finally:
            tcp_cli_sock.close()

    def file_exists(self, filename):
        try:
            with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                return True
        except IOError:
            return False

    def send_cached_response(self, tcp_cli_sock, filename):
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            outputdata = f.readlines()
        tcp_cli_sock.send("HTTP/1.0 200 OK\r\n".encode(encoding="utf-8", errors="ignore"))
        tcp_cli_sock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
        for line in outputdata:
            tcp_cli_sock.send(line.encode(encoding="utf-8", errors="ignore"))
        print('Read from cache')

    def handle_get_request(self, tcp_cli_sock, path, filename):
        if self.file_exists(filename):
            self.send_cached_response(tcp_cli_sock, filename)
        else:
            self.fetch_and_cache_response(tcp_cli_sock, path, filename)

    def handle_post_request(self, tcp_cli_sock, path, filename, body):
        hostn = path.split('/')[0]
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            c.connect((hostn, 80))
            request = f"POST {path} HTTP/1.0\r\nHost: {hostn}\r\nContent-Length: {len(body)}\r\n\r\n{body}"
            c.sendall(request.encode(encoding="utf-8", errors="ignore"))

            buffer = b""
            while True:
                data = c.recv(4096)
                if not data:
                    break
                buffer += data

            if b"404 Not Found" in buffer.split(b"\r\n")[0]:
                self.send_error_response(tcp_cli_sock, "404 Not Found")
                return

            with open(filename, "wb") as tmpFile:
                tmpFile.write(buffer)
            
            tcp_cli_sock.send(buffer)
        
        except ConnectionError as e:
            print("Connection error:", e)
            self.send_error_response(tcp_cli_sock, "502 Bad Gateway")
        
        except Exception as e:
            print("Illegal request", e)
            self.send_error_response(tcp_cli_sock, "400 Bad Request")
        
        finally:
            c.close()

    def fetch_and_cache_response(self, tcp_cli_sock, filename, filetouse):
        hostn = filename.split('/')[0]
        path = '/' + '/'.join(filename.split('/')[1:])
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            c.connect((hostn, 80))
            request = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
            c.sendall(request.encode(encoding="utf-8", errors="ignore"))

            buffer = b""
            while True:
                data = c.recv(4096)
                if not data:
                    break
                buffer += data

            if b"404 Not Found" in buffer.split(b"\r\n")[0]:
                self.send_error_response(tcp_cli_sock, "404 Not Found")
                return

            with open(filetouse, "wb") as tmpFile:
                tmpFile.write(buffer)
            
            tcp_cli_sock.send(buffer)
        
        except ConnectionError as e:
            print("Connection error:", e)
            self.send_error_response(tcp_cli_sock, "502 Bad Gateway")
        
        except Exception as e:
            print("Illegal request", e)
            self.send_error_response(tcp_cli_sock, "400 Bad Request")
        
        finally:
            c.close()

    def send_error_response(self, tcp_cli_sock, message):
        tcp_cli_sock.send(f"HTTP/1.0 {message}\r\n".encode(encoding="utf-8", errors="ignore"))
        tcp_cli_sock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
        tcp_cli_sock.send("\r\n".encode(encoding="utf-8", errors="ignore"))
        tcp_cli_sock.send(f"<html><head></head><body><h1>{message}</h1></body></html>\r\n".encode(encoding="utf-8", errors="ignore"))

def main():
    server_ip = get_server_ip()
    proxy_server = ProxyServer(server_ip)
    proxy_server.start_server()
    proxy_server.serve_forever()

def get_server_ip():
    if len(sys.argv) <= 1:
        print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server]')
        sys.exit(2)
    return sys.argv[1]

if __name__ == "__main__":
    main()
