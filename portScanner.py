import socket
import sys
# TODO: add concurrent.futures and datetime when you get to the thread pool and summary steps



# Step 2 — CLI inputs
# grab the host and port range from the command line e.g. python scanner.py 192.168.1.1 1-1024
host = sys.argv[1]
start_port, end_port = sys.argv[2].split("-")  # split "1-1024" into "1" and "1024"
start_port = int(start_port)  # convert from string to integer
end_port = int(end_port)      # convert from string to integer

# Step 3 — scan_port(host, port) function goes here
def scan_port(host, port):
    sock = socket.socket()          # create a socket
    sock.settimeout(1)              # give up after 1 second
    result = sock.connect_ex((host, port))  # try to connect, returns 0 if open
    sock.close()                    # always close the socket after
    if result == 0:
        return "open"
    return "closed"


# TODO: Step 4 — thread pool loop goes here

# TODO: Step 5 — summary (total scanned, open count, elapsed time) goes here


