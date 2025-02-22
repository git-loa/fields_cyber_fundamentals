from socket import *
import sys

# Get the server IP from the command line arguments, default to localhost if not provided
if len(sys.argv) <= 1:
    print('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

server_ip = sys.argv[1]

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((server_ip, 8888))  # Bind to the provided server IP (or localhost) and port 8888
tcpSerSock.listen(5)  # Listen for up to 5 connections
try:
    while 1:
        # Start receiving data from the client
        print('Ready to serve...')
        try:
            tcpCliSock, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)
        except OSError as e:
            print("Error accepting connection:", e)
            continue

        try:
            message = tcpCliSock.recv(1024).decode(encoding="utf-8", errors="ignore")  # Receive client message
            print(message)
            
            # Ensure that the message is not empty and has enough parts after splitting 
            if not message: 
                raise ValueError("Received an empty message.") 
            parts = message.split() 
            if len(parts) < 2: 
                raise ValueError("Invalid message format.")
            
            # Extract the filename from the given message
            filename = message.split()[1][1:]
            print(filename)
            fileExist = "false"
            filetouse = filename.replace('/', '_')
            print(filetouse)

            try:
                # Check whether the file exists in the cache
                f = open(filetouse, "r", encoding="utf-8", errors="ignore")
                outputdata = f.readlines()
                fileExist = "true"
                # ProxyServer finds a cache hit and generates a response message
                tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode(encoding="utf-8", errors="ignore"))
                tcpCliSock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
                # Send the content of the requested file to the client
                for line in outputdata:
                    tcpCliSock.send(line.encode(encoding="utf-8", errors="ignore"))
                print('Read from cache')

            # Error handling for file not found in cache
            except IOError:
                if fileExist == "false":
                    # Create a socket on the proxy server
                    c = socket(AF_INET, SOCK_STREAM)
                    hostn = filename.split('/')[0]
                    path = '/' + '/'.join(filename.split('/')[1:])
                    print(hostn, path)

                    try:
                        # Connect to the socket to port 80
                        c.connect((hostn, 80))
                        # Send the GET request
                        request = f"GET {path} HTTP/1.0\r\nHost: {hostn}\r\n\r\n"
                        c.sendall(request.encode(encoding="utf-8", errors="ignore"))

                        # Read the response into buffer
                        buffer = b""
                        while True:
                            data = c.recv(4096)
                            if not data:
                                break
                            buffer += data

                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        tmpFile = open(filetouse, "wb")
                        tmpFile.write(buffer)
                        tmpFile.close()
                        tcpCliSock.send(buffer)

                    except ConnectionError as e:
                        print("Connection error:", e)
                        tcpCliSock.send("HTTP/1.0 502 Bad Gateway\r\n".encode(encoding="utf-8", errors="ignore"))
                        tcpCliSock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
                        tcpCliSock.send("\r\n".encode())
                        tcpCliSock.send("<html><head></head><body><h1>502 Bad Gateway</h1></body></html>\r\n".encode(encoding="utf-8", errors="ignore"))

                    except Exception as e:
                        print("Illegal request", e)
                        tcpCliSock.send("HTTP/1.0 400 Bad Request\r\n".encode(encoding="utf-8", errors="ignore"))
                        tcpCliSock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
                        tcpCliSock.send("\r\n".encode())
                        tcpCliSock.send("<html><head></head><body><h1>400 Bad Request</h1></body></html>\r\n".encode(encoding="utf-8", errors="ignore"))

                else:
                    # HTTP response message for file not found
                    tcpCliSock.send("HTTP/1.0 404 Not Found\r\n".encode(encoding="utf-8", errors="ignore"))
                    tcpCliSock.send("Content-Type:text/html\r\n".encode(encoding="utf-8", errors="ignore"))
                    tcpCliSock.send("\r\n".encode(encoding="utf-8", errors="ignore"))
                    tcpCliSock.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode(encoding="utf-8", errors="ignore"))

        except OSError as e:
            print("Error receiving message:", e)
        finally:
            # Close the client and the server sockets
            tcpCliSock.close()
            if 'c' in locals():
                c.close()
except KeyboardInterrupt: 
    print("\nShutting down the proxy server.") 
finally:
    tcpSerSock.close()