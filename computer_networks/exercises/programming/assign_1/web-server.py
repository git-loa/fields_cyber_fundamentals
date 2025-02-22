#!/usr/bin/python3

# Import the socket module
from socket import *
import sys #In order to terminate the program


# create a socket object
serverSocket = socket(AF_INET, SOCK_STREAM)


#Prepare a server socket

# ------- Fill in start -----------------

#using bind() and listen

HOST = "10.0.2.15"  # IP address
PORT = 12000 # Port to listen 
ADDRESS = (HOST, PORT) # HOST, PORT pair

#Bind the socket to the address
serverSocket.bind(ADDRESS)

#Listen for incomming connections
serverSocket.listen() 
print(f'Server listening on {HOST}:{PORT}')

# -------- Fill in end -------------------


while True:
	#Establish the connection
	print(f'Ready to serve...')

	# ------- Fill in start -----------------
	connectionSocket, client_addr = serverSocket.accept()
	# -------- Fill in end -------------------

	try:
		# ------- Fill in start -----------------
		message = connectionSocket.recv(1024).decode('utf-8', errors='replace')
		# -------- Fill in end -------------------

		# Parse the message (the HTTP request) to get the file name.
		filename = message.split(' ')[1]


		#Open the requested html file using context manager and its content. 
		with open(filename[1:], 'r', encoding='utf-8', errors='replace') as file:
			response_body = file.read()
		

		# Create an http response message
		# ------- Fill in start -----------------
		outputdata = \
		f"""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length {len(response_body)}

{response_body}
"""
		# -------- Fill in end -------------------


		# Send the content of the requested file to the client
		for i in range(0, len(outputdata)):
			connectionSocket.send(outputdata[i].encode('utf-8', errors='replace'))
		connectionSocket.send("\r\n".encode('utf-8', errors='replace'))
		connectionSocket.close()

	except IOError:
		# Send response message for file not found

		# ------- Fill in start -----------------

		# Return a 404 response
		response_body = \
			f"""
<!DOCTYPE html>
<html>
<head>
<title>Hello World</title>
</head>
<body>

<h1>404 Not Found</h1>


</body>
</html> 
			"""
		response_404 = \
			f"""
HTTP/1.1 404 Not Found 
Content-Type: text/html 
Content-Length: {len(response_body)} 
			
{response_body} 
"""
		
		for i in range(0, len(response_404)):
			connectionSocket.send(response_404[i].encode('utf-8', errors='replace'))
		connectionSocket.send("\r\n".encode('utf-8', errors='replace'))

		# -------- Fill in end -------------------

		# Close client connection
		connectionSocket.close()


serverSocket.close() # Close server connection
sys.exit() #Terminate the program after sending the corresponding data


