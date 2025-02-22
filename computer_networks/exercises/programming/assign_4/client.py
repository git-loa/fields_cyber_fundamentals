#!usr/bin/python3

from socket import *

def send_all(sock: socket, data: bytes) -> None:
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

def recv_all(sock: socket, buffer_size: int = 1024) -> str:
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


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(("127.0.0.1", 12000))
message = input("Enter a message in lowercase: ")
send_all(client_socket, message.encode())
response = recv_all(client_socket)
print(response)
client_socket.close()