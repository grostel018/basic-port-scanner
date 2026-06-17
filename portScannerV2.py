import socket
import threading
from queue import Queue, Empty

# =========================
# Configuration
# =========================

TARGET = "192.168.1.106"
START_PORT = 1
END_PORT = 1024
NUM_THREADS = 100

queue = Queue()
open_ports = []


# =========================
# Port Scanning Functions
# =========================

def port_scan(port):
    """Returns True if the port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            sock.connect((TARGET, port))
            return True
    except:
        return False


def worker():
    """Thread worker that scans ports from the queue."""
    while True:
        try:
            port = queue.get_nowait()
        except Empty:
            break

        if port_scan(port):
            print(f"Port {port} is open")
            open_ports.append(port)

        queue.task_done()


# =========================
# Queue Management
# =========================

def populate_queue():
    """Adds ports to the queue."""
    for port in range(START_PORT, END_PORT):
        queue.put(port)


# =========================
# Thread Management
# =========================

def create_threads():
    """Creates and starts worker threads."""
    threads = []

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    return threads


def wait_for_threads(threads):
    """Waits for all threads to finish."""
    for thread in threads:
        thread.join()


# =========================
# Main Program
# =========================

def main():
    print(f"Scanning {TARGET}...")
    print(f"Ports: {START_PORT}-{END_PORT - 1}\n")

    populate_queue()

    threads = create_threads()

    wait_for_threads(threads)

    open_ports.sort()

    print("\nScan complete.")
    print("Open ports:", open_ports)


if __name__ == "__main__":
    main()