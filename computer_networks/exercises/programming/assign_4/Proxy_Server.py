#!/usr/bin/python3

from socket import *
from collections import OrderedDict
from threading import Thread
import sys

class ProxyServer:
    def __init__(self, server_ip: str, port:int = 12000, cache_size:int = 5):
        """
        Initializes the ProxyServer with the given server IP, part and cache size.

        Parameter(s)
        ------------
        server_ip: str 
            IP address of the proxy server.
        port: int  
            Port number to bind the proxy server.
        cache_size: int
            Maximum nuber of cache entries.

        Returns
        -------
        None
        """ 
        self.server_ip = server_ip
        self.port = port
        self.cache_size = cache_size
        self.cache = OrderedDict # This is to maintain the order of access for LRU policy
        self.server_socket = self.create_server_socket()
       

    def create_server_socket(self) -> socket:
        """
        Creates and binds the server socket to the specified IP and port.

        Return
        ------
        socket:
            The created server socket
        """
        try:
            server_socket = socket(AF_INET, SOCK_STREAM) # Create a new socket object for server.
            server_socket.bind((self.server_ip, self.port))
            server_socket.listen(5)
            print("[*] Server is ready to accept requests...")
            return server_socket
        except Exception as e:
            print(f"Error creating server socket: {e}")
            sys.exit(1)
   
    def send_all(self, sock: socket, data: bytes) -> None:
        """
        Send all data through a socket

        The function ensures that all data is sent through the socket by
        repeatedly calling the `send` method until all data has been transmitted.

        Parameters
        ----------
        sock : socket.socket
            socket object representing the network connection
        data : bytes
            The data to be sent through the socket.

        Returns
        -------
        None

        Raises
        ------
        RuntimeError: If the socket is broken and no data is sent.
        """
        total_sent = 0
        while total_sent < len(data):
            sent_size = sock.send(data[total_sent:])
            if sent_size == 0:
                raise RuntimeError("Socket connection broken")
            total_sent += sent_size

    def recv_all(self, sock: socket, buffer_size: int = 1024) -> str:
        """
        Receive all data from a socket.

        This function reads data from the socket by repeatedly calling the `recv` method until
        all data has been received. The function expects to receive data in chunks of a specified size.

        Parameters
        ----------
        sock : (socket.socket)
            The socket object representing the network connection.
        buffer_size : (int, optional)
            The maximum amount of data to be received at once. Defaults to 1024.

        Returns
        -------
        str: 
            The data received from the socket.
        """
        data = b""
        while True:
            part = sock.recv(buffer_size)
            data += part
            if len(part) < buffer_size:
                break
        return data.decode()

    def handle_client(self, client_socket: socket) -> None:
        """
        Handles the client's request and forwards it to the appropriate handler
        based on the http method.

        Parameter(s)
        ------------
        client_socket: socket
            The client socket

        Returns
        -------
        None
        """
        
        try:
            # ----- Fill in start
            message = self.recv_all(client_socket) # message is of type str.
            # ----- Fill in end
            
            headers = message.split("\r\n")
            #print(type(headers))
            request_line = headers[0]
            print(request_line)
            method, file_path, _ = request_line.split()
            filename = file_path.partition("/")[2]
            print(filename)


            # Check for GET request
            if method == "GET":
                print(f"TEST ----{filename} ")
                self.handle_get_request(client_socket, filename, headers)
                print("HEPPO")
                
            elif method == "POST":
                #self.handle_post_request(client_socket, filename, headers, message)
                pass

            #self.send_all(client_socket, request_line.upper().encode())
        except Exception as e:
            print(f"Error handling client request")
            print(f"Error: {e}")

    def handle_get_request(self, client_socket: socket, filename: str, headers: list)-> None:
        """
        Handles HTTP GET requests by checking the cache or fetching from the web server.

        Parameter(s)
        ------------
        client_socket: socket
            The client socket
        filename: str
            The requested file
        headers: list
            The HTTP headers from the client request.

        Returns
        -------
        None
        """
        print(f"Come---------{filename} ")
        # Check if requested file is in cache (the ordered dictionary self.cache)
        try:
            self.cache
        except Exception as e:
            print(f"wwwwwwwwww ----- {e}")
        if filename in self.cache:
            print("bbbooo")
           # self.send_from_cache(client_socket, filename)
        else:
            print("AKWAABA")
            #self.fetch_from_web(client_socket, filename, headers, method, body)
        
    def handle_post_request(self, client_socket: socket, filename: str, headers: list, message: str) -> None:
        """
        Handles HTTP POST requests by forwarding the request body the web server.

        Parameter(s)
        ------------
        client_socket: socket
            The client socket
        filename: str
            The requested file
        headers: list
            The HTTP headers from the client request.
        message: str

        Returns
        -------
        None
        """
        pass

    def send_from_cache(self, cleint_socket: socket, filename: str) -> None:
        """
        Sends the cached response to the client.

        Parameter(s)
        ------------
        client_socket: socket
            The client socket
        filename: str
            The caches filename

        Returns
        -------
        None
        """
        pass

    def fetch_from_web(self, client_socket: socket, filename: str, headers: list, method: str, body: str=None)-> None:
        """
        Fetches the requested content from the web and updates the cache.

        client_socket: socket
            The client socket 
        filename: str 
            The requested filename
        headers: str
            The HTTP headers from the client request
        method: str 
            The HTTP method (GET or POST)
        body: str
            The request body for the POST requests.
        
        Returns
        -------
        None
        """
        """
        # Create a socket on the proxyserver
        # ---- Fill in start
        web_socket = socket(AF_INET, SOCK_STREAM)
        # ---- Fill in end
        hostname = filename.replace("www.", "", 1)
        print(hostname)
        try:
            #Connect to port 80
            #----- Fill in start
            wec_socket.connect((hostname, 80))
            #---- Fill in end

            if method == "GET":
                request = f"GET /{filename} HTTP/1.0\r\nHost: {hostname}\r\n\r\n"
            elif method == "POST":
                #request = f"POST /{filename} HTTP/1.0\r\nHost: {hostname}\r\n" + \
                #"\r\n".join(headers[1:]) + "\r\n\r\n" + body
                pass
            self.send_all(web_socket, request.encode())
            response = recv_all(web_socket)
            print(response)
        except Exception as e:
            print(e)
            """

    def update_cache(self, filename: str, response: str) -> None:
        """
        Updates the cache by writing the response to disk and maintaining the cache 
        size using LRU policy.

        Parameter(s)
        ------------
        filename: str 
            The requested filename
        response: str
            The request data to be cached.

        Returns
        -------
        None
        """

    def start(self) -> None:
        """
        Starts the Proxy server to accept client connections.
        """
        print(f"[*] Proxy Server {self.server_ip} listening on port {self.port}")
        try:
            while True:
                client_socket, client_addr = self.server_socket.accept()
                print(f"[*] Connection received from {client_addr}")
                client_thread = Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
        except Exception as e:
            print(f"Error in server loop: {e}")
        finally:
            self.server_socket.close()

            



if __name__ == "__main__":
    proxy_server = ProxyServer("10.0.2.15")
    proxy_server.start()








