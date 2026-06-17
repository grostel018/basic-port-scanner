# Multi-Threaded TCP Port Scanner

## Overview

This project is a multi-threaded TCP port scanner developed in Python.

The scanner attempts to establish TCP connections to a target host and identifies which ports are open. To improve performance, the application uses multiple worker threads operating on a shared queue of ports.

The project was created to gain practical experience with:

* Socket programming
* TCP/IP networking
* Multithreading
* Thread-safe queues
* Python project organization
* Basic cybersecurity reconnaissance techniques

---

## Features

* TCP port scanning
* Multi-threaded architecture
* Configurable target host
* Configurable port range
* Thread-safe task distribution
* Automatic sorting of scan results
* Modular code structure
* No third-party dependencies

---

## Project Structure

```text
project/
│
├── portScanner.py
├── README.md
└── DOCUMENTATION.md
```

### Internal Architecture

```text
Configuration
│
├── Port Scanning Functions
│   ├── port_scan()
│   └── worker()
│
├── Queue Management
│   └── populate_queue()
│
├── Thread Management
│   ├── create_threads()
│   └── wait_for_threads()
│
└── main()
```

This structure separates responsibilities and improves maintainability.

---

## Requirements

* Python 3.8+
* Network connectivity to the target host

No external libraries are required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/python-port-scanner.git
cd python-port-scanner
```

Verify Python installation:

```bash
python --version
```

---

## Configuration

Edit the configuration section:

```python
TARGET = "192.168.1.106"
START_PORT = 1
END_PORT = 1024
NUM_THREADS = 100
```

### Parameters

| Variable    | Description                   |
| ----------- | ----------------------------- |
| TARGET      | IP address to scan            |
| START_PORT  | First port to scan            |
| END_PORT    | Last port to scan (exclusive) |
| NUM_THREADS | Number of worker threads      |

Example:

```python
TARGET = "127.0.0.1"
START_PORT = 20
END_PORT = 1025
NUM_THREADS = 50
```

---

## Usage

Run the scanner:

```bash
python portScanner.py
```

Example output:

```text
Scanning 192.168.1.106...
Ports: 1-1023

Port 135 is open
Port 139 is open
Port 445 is open

Scan complete.
Open ports: [135, 139, 445]
```

---

## Testing

### Test 1: Scan Localhost

Set:

```python
TARGET = "127.0.0.1"
```

Run the scanner and verify local services are detected.

---

### Test 2: Temporary HTTP Server

Start a temporary server:

```bash
python -m http.server 8080
```

Then scan:

```python
START_PORT = 8000
END_PORT = 8100
```

Expected result:

```text
Port 8080 is open
```

---

### Test 3: Android Device

Connect your phone to the same Wi-Fi network.

Run:

```bash
python -m http.server 8080
```

inside Termux or another mobile server application.

Update:

```python
TARGET = "PHONE_IP_ADDRESS"
```

Verify the scanner detects port 8080.

---

### Test 4: Invalid Host

Configure an unreachable address and verify that the program handles failures gracefully.

---

## Educational Purpose

This project is intended for learning and authorized testing environments.

Only scan:

* Systems you own
* Laboratory environments
* Networks where you have explicit permission

---

## Future Improvements

The current implementation focuses on TCP port discovery and multithreaded scanning. Several features could be added to bring the project closer to professional network reconnaissance tools.

### 1. Command-Line Arguments

Allow users to specify scan parameters without modifying the source code.

Example:

```bash
python portScanner.py 192.168.1.10 1 1024
```

Potential implementation:

* argparse module
* Custom thread count
* Configurable timeout values

---

### 2. Service Detection

Identify common services running behind discovered ports.

Example:

```text
80/tcp open HTTP
22/tcp open SSH
443/tcp open HTTPS
```

This would provide more meaningful information than port numbers alone.

---

### 3. Banner Grabbing

Retrieve service banners after connecting to an open port.

Example:

```text
22/tcp open OpenSSH_9.2
```

This can help identify software versions and configurations.

---

### 4. Host Discovery

Determine whether a host is alive before beginning a scan.

Possible techniques:

* ICMP Echo Requests
* ARP Requests
* TCP Probes

Benefits:

* Faster scans
* Reduced unnecessary connection attempts

---

### 5. UDP Port Scanning

Extend support beyond TCP.

Common UDP services include:

| Port | Service |
| ---- | ------- |
| 53   | DNS     |
| 67   | DHCP    |
| 123  | NTP     |
| 161  | SNMP    |

---

### 6. Result Export

Export scan results to files.

Possible formats:

* CSV
* JSON
* TXT

Example:

```csv
IP,Port,State
192.168.1.10,80,Open
192.168.1.10,443,Open
```

---

### 7. Logging System

Record scan activity and errors.

Benefits:

* Easier debugging
* Historical scan records
* Improved maintainability

---

### 8. Operating System Detection

Attempt to infer the operating system of the target host through network fingerprinting.

Example:

```text
Windows 11
Ubuntu Linux
FreeBSD
```

---

### 9. Multi-Host Scanning

Scan an entire subnet.

Example:

```text
192.168.1.1
192.168.1.2
192.168.1.3
...
```

Useful for network inventory and administration.

---

### 10. Graphical User Interface (GUI)

Develop a desktop application allowing users to:

* Enter targets
* Configure scans
* View results visually
* Export reports

Possible technologies:

* Tkinter
* PyQt
* CustomTkinter

---

### Long-Term Goal

A long-term objective would be to evolve this project into a simplified educational alternative to professional tools such as Nmap, while continuing to learn networking, cybersecurity, and software engineering concepts.

