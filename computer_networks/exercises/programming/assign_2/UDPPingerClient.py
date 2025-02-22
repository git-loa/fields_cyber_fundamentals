from socket import *
import time

def udp_client(serverName: int, serverPort: int = 12000) -> None:
    rtts = []
    lost_packets = 0
    
    clientSocket = socket(AF_INET, SOCK_DGRAM) # Create client socket object
    clientSocket.settimeout(1) # Set a time out.

    # Send 10 packets to server using a for loop
    total_packets = 0
    for i in range(1, 11):
        # Send message to the server
        start_time = time.time()
        clientMessage = f"Ping seq:{1} time:{start_time}" # client message to send

        try:
            clientSocket.sendto(clientMessage.encode('utf-8'), (serverName, serverPort)) 
            
            serverResponse, serverAddress = clientSocket.recvfrom(2048) # Response from the server
            rtt = time.time() - start_time # Compute the RTT
            rtts.append(rtt) # Append rtt to list
            
            # Print server response if any
            if serverResponse:
                print(f"\nResponse from server: {serverResponse}")
            print(f"Round Trip Time (RTT): {rtt:.3f} seconds\n")
        except timeout:
            lost_packets += 1
            print("Request time out")
        total_packets += 1
    clientSocket.close()

    # Compute RTT statistics
    if rtts:
        max_rtt = max(rtts)
        min_rtt = min(rtts)
        avg_rtt = sum(rtts)/len(rtts)
    else:
        max_rtt = min_rtt = avg_rtt = 0
        
    packet_loss_rate = (lost_packets/total_packets)*100 # Compute loss rate
    
    print("\n----- Ping statistics -----")
    print(f"Transmited packets ----------- {total_packets}")
    print(f"Received ------------ {total_packets - lost_packets}")
    print(f"Loss rate ------------- {packet_loss_rate}%")
   
    print(f"RTT min / avg / max -------  {min_rtt:.3f} / {avg_rtt:.3f} / {max_rtt:.3f} seconds")

if __name__ == "__main__":
    server_name = "127.0.0.1"
    server_port = 12000
    udp_client(server_name, server_port)
