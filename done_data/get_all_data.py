import socket

# Create a UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific port
udp_socket.bind(('192.168.95.54', 14550))  # Replace '127.0.0.1' with your IP address and 12345 with the desired port number

while True:
    # Receive data from the socket
    data, addr = udp_socket.recvfrom(2048)  # 1024 is the buffer size, you can adjust it as needed
    print(f"Received data from {addr}: {data}")  # Assuming the data is in UTF-8 format, adjust accordingly
