#!/usr/bin/python3

from socket import *
from ssl import *
import base64


#Define the SMTP server and PORT

#-------- Fill in start
#mailserver = "smtp.office365.com"
mailserver = "smtp.gmail.com"
port = 587
#-------- FIll in end

# Define the sender and recipient 
sender = "sender.mail.com" 
recipient = "receipient.email.com" 
username = "sender_username" 
password = "sender_password" 
subject = "Test Email" 
msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

message = f"Subject: {subject}\r\n" \
    f"Content-Type: text/plain;\r\n" \
    f"Content-Transfer-Encoding: 7bit\r\n" \
    f"\r\n{msg}"

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
        sent = sock.send(data[total_sent:]) #send returns int
        if sent == 0:
            raise RuntimeError("Socket connection broken")
        total_sent += sent
        print(f"Sent {total_sent} bytes out of {len(data)}")

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
    str: The data received from the socket, decoded as a UTF-8 string.
    """
    data = b""
    while True:
        part = sock.recv(buffer_size)
        data += part
        if len(part) < buffer_size:
            break
    return data.decode()

def helo_command(sock: socket) -> None:
    helloCommand = 'HELO Alicer\n'
    send_all(sock, helloCommand.encode()) # Send the HELO command using the send_all functions.
    response = recv_all(sock)
    print(f"'HELO'response: {response}")

    if response[:3] != '250':
        print('250 reply not received from server.')
        raise RuntimeError('250 reply not received from server.')
    
def tls_command(sock: socket) -> None:
    tlsCommand = 'STARTTLS\r\n'
    send_all(sock, tlsCommand.encode())
    response = recv_all(sock)
    print(f"'STARTTLS' reponse: {response}")

def auth_login(secure_socket: socket, username: str, password: str)-> None:
    authLogin = 'AUTH LOGIN\r\n'
    send_all(secure_socket, authLogin.encode())
    response = recv_all(secure_socket)
    print(f"'AUTH LOGIN' response: {response}")
    

    # Encode the username and password 
    username_b64 = base64.b64encode(username.encode()).decode() 
    password_b64 = base64.b64encode(password.encode()).decode()

    send_all(secure_socket, (username_b64 + "\r\n").encode())
    response = recv_all(secure_socket)
    print(f"Username reponse: {response}")

    send_all(secure_socket, (password_b64 + "\r\n").encode())
    response = recv_all(secure_socket)
    print(f"Password response: {response}")

    # Check for authentication failure 
    if response[:3] == '535': 
        raise RuntimeError('Authentication failed: Invalid username or password.')

def mail_from(secure_socket: socket, sender: str) -> None:
    mailFrom = f"MAIL FROM:<{sender}>\r\n"
    send_all(secure_socket, mailFrom.encode())
    response = recv_all(secure_socket)
    print(f"'MAIL FROM' response: {response}")

def rcpt_to(secure_socket: socket, recipient: str)->None:
    mailTo = f"RCPT TO:<{recipient}>\r\n"
    send_all(secure_socket, mailTo.encode())
    response = recv_all(secure_socket)
    print(f"'RCPT TO' response: {response}")

def data_command(secure_socket: socket)->None:
    dataCommand = f"DATA\r\n"
    send_all(secure_socket, dataCommand.encode())
    response = recv_all(secure_socket)
    print(f"'DATA' response: {response}")

def send_message(secure_socket: socket, msg: str)-> None:
    send_all(secure_socket, (msg + "\r\n.\r\n").encode())
    response = recv_all(secure_socket)
    print(f"'Send message' response: {response}")

def quit_mail(secure_socket: socket) -> None:
    quitCommand = f"QUIT\r\n"
    send_all(secure_socket, quitCommand.encode())
    response = recv_all(secure_socket)
    print(f"'QUIT' response: {response}")



if __name__ == '__main__':
    # Create socket called clientSocket and establish a TCP connection with mailserver

    #Fill in start
    with socket(AF_INET, SOCK_STREAM) as clientSocket: # cleint socket object
        clientSocket.connect((mailserver, port))
        # Receive the server's initial greeting
        serverResponse = recv_all(clientSocket)
        print(f'Initial server response: {serverResponse}')

        # Ckeck if a 220 reply not received from server.
        if serverResponse[:3] != '220':
            print('220 reply not received from server.')
            raise RuntimeError('220 reply not received from server.')
        
    #Fill in end

        # Send HELO command and print server response
        helo_command(clientSocket)
        
        ###### Start Optional Exercises #######

        #Send STARTTLS command and upgrade to TLS connection
        tls_command(clientSocket)
        tls_context = create_default_context()
        with tls_context.wrap_socket(clientSocket, server_hostname=mailserver) as secure_clientServer:
            # After TLS connection, send another HELO command
            helo_command(secure_clientServer)
            auth_login(secure_clientServer, username, password)
        ###### End Optional Exercises #######

            # Send MAIL FROM command and print server response.
            # Fill in start
            mail_from(secure_clientServer, sender)
            # Fill in end

            # Send RCPT TO command and print server response.
            # Fill in start
            rcpt_to(secure_clientServer, recipient)
            # Fill in end

            # Send DATA command and print server response.
            # Fill in start
            data_command(secure_clientServer)
            # Fill in end

            # Send message data.
            # Fill in start
            print("Sending message...")
            send_message(secure_clientServer, message)
            print("Message sent")
            # Fill in end

            # Send QUIT command and get server response.
            # Fill in start
            quit_mail(secure_clientServer)
            # Fill in end

