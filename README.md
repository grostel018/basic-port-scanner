# basic-port-scanner
A port scanner project made to learn more about the subject

A port scanner works by attempting to establish connections to a range of ports on a target host and checking which ones respond. Here's the conceptual flow:

**1. Understand what a port is**
A port is a numbered endpoint (0–65535) on a machine. Services "listen" on specific ports — e.g., HTTP on 80, HTTPS on 443, SSH on 22.

**2. Choose a scanning technique**
The most common beginner approach is a **TCP connect scan**: try to complete a full TCP handshake with each port. If it succeeds, the port is open. If the connection is refused or times out, it's closed or filtered.

**3. Define your inputs**
You need two things: a target IP address or hostname, and a range of ports to scan (e.g., 1–1024 for well-known ports).

**4. Iterate over each port**
Loop through each port number in your range and attempt a socket connection to the target on that port.

**5. Set a timeout**
Without a timeout, a scan on filtered/firewalled ports will hang indefinitely. A short timeout (e.g., 0.5–1 second) keeps things practical.

**6. Record the result**
If the connection succeeds → mark the port as **open**. If it's refused or times out → mark it as **closed** or **filtered**.

**7. Report the findings**
After scanning, print or log which ports were open, optionally with the service name commonly associated with each port number.

**8. (Optional) Add speed with concurrency**
Scanning ports one by one is slow. Using threads or async I/O lets you scan many ports simultaneously, dramatically reducing total scan time.

---

**Key things to keep in mind:**
- Only scan systems you own or have explicit permission to scan. Unauthorized port scanning is illegal in many jurisdictions.
- Most languages have a built-in **socket** library that handles the low-level connection work.
- For more advanced scanning (SYN scans, OS fingerprinting, etc.), tools like `nmap` are the industry standard — they're worth studying even if you're building your own.
