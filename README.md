# HTTP Reverse Shell Server
This script creates a simple HTTP server that listens for specific requests and serves pre-configured Python scripts when certain URLs are accessed. It is intended for use in penetration testing or security demonstrations.

## Features:
The server listens on a specified port for incoming HTTP requests.

If a request is made for /revshell.py, the server will respond with a Python script that attempts to open a reverse shell to the specified listener port.

For all other requests, the server will respond with a 404 "Not Found" message.

Once the server is running, you can request the reverse shell script by navigating to the following URL in a web browser or using curl: http://<local_ip>:<http_port>/revshell.py.
This will trigger the server to send the reverse shell script, which will attempt to connect back to your machine on the listener port.
