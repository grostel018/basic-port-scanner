- scanning technique : TCP Connect Scan
- inputs types : 
    
    **Target / Host Inputs**
    
    - Single IP address — `192.168.1.1`
    - Hostname — `example.com`
    - CIDR range — `192.168.1.0/24` (scans an entire subnet)
    - IP range — `192.168.1.1-50`
    - List of hosts from a file — `targets.txt`
    
    * * *
    
    **Port Inputs**
    
    - Single port — `80`
    - Comma-separated ports — `22,80,443`
    - Port range — `1-1024`
    - Named categories — `--top-ports 100` (well-known services)
    - All ports — `1-65535`
    - Protocol-specific — TCP only, UDP only, or both

&nbsp;

&nbsp;

- Loops types : 
    
    For iterating over ports, here are the loop types we can use:
    
    * * *
    
    **Simple For Loop** The most straightforward approach. You iterate over a range of port numbers sequentially, one by one. Easy to read and debug, but slow on large ranges since each port waits for the previous one to finish.
    
    * * *
    
    **While Loop** Useful when you want more manual control — for example, retrying a port a certain number of times before moving on, or dynamically adjusting which port to scan next based on results.
    
    * * *
    
    **For-Each Loop (iterating a collection)** Instead of a numeric range, you iterate over a pre-built list of ports (e.g., a list of well-known ports, or ports loaded from a file). Clean and flexible when your port list isn't a simple sequential range.
    
    * * *
    
    **Threaded Loop** You spawn a thread for each port (or batch of ports) so many connections happen simultaneously. This is the most important pattern for a real tool — scanning 1,000 ports sequentially might take minutes, while threaded scanning can do it in seconds. You typically pair this with a thread pool to cap concurrency.
    
    * * *
    
    **Async Loop** Instead of threads, you use async/await and an event loop to handle thousands of concurrent connections with very low overhead. More efficient than threading at scale, but slightly more complex to reason about.
    
    * * *
    
    **Queue-based Loop** You push all ports into a work queue, then multiple worker threads/processes pull from it. This gives you fine-grained control over concurrency and is the most robust pattern for a production-grade tool — workers naturally handle retries, and you avoid spawning thousands of threads at once.
    
    * * *
    
    **For a real tool**, the progression would be:
    
    1.  Start with a **simple for loop** to get the logic right
    2.  Upgrade to a **threaded loop with a thread pool** for real speed
    3.  Consider a **queue-based approach** if you need retry logic or want to scan multiple hosts

&nbsp;

&nbsp;

&nbsp;

&nbsp;

- Timeouts :

**Connection Timeout** The most essential one. How long to wait for a port to respond before marking it as closed/filtered. Too short (under 0.3s) and you'll get false negatives on slow networks. Too long (over 3s) and your scan crawls. A value between **0.5s – 1s** is the sweet spot for local/LAN scanning; bump it to **2–3s** for remote targets.

* * *

**Read/Banner Timeout** Separate from the connection timeout — this controls how long to wait *after* connecting for the service to send back data (for banner grabbing). Should generally be slightly longer than your connection timeout since some services are slow to respond after accepting a connection.

* * *

**Per-Host Timeout** A global cap on how long to spend on a single host total, regardless of individual port results. Useful when scanning multiple hosts — prevents one slow/unresponsive host from blocking the rest.

* * *

**Retry Timeout** If you retry failed ports, you can add a delay between attempts. This avoids hammering a port immediately after a failed attempt, which could trigger rate limiting or firewalls.

* * *

**Idle/Global Scan Timeout** A hard cap on the entire scan duration. If the scan hasn't finished in X minutes, stop and report what was found so far. Critical for large ranges like 1–65535.

* * *

**Adaptive Timeout** More advanced — you measure the average response time of the first few ports and dynamically adjust the timeout for the rest of the scan. This is how `nmap` handles it. Overkill for a first version, but worth knowing about.

* * *

**How they interact visually:**

```
[Connect attempt] --connection timeout--> [Connected]
                                               |
                                         --read timeout--> [Banner received]
```

* * *

**Practical recommendation for your tool:**

| Scenario | Connection Timeout |
| --- | --- |
| Local / LAN | 0.3s – 0.5s |
| Remote / internet | 1s – 2s |
| Unreliable network | 2s – 3s |

Start with a **hardcoded default** (e.g. 1s) and make it **configurable as a CLI input** so the user can tune it per situation. That's the standard approach in real tools.

&nbsp;

&nbsp;

&nbsp;

- Recording results and logs :

**What to Record Per Port** At minimum, capture:

- Port number
- Protocol (TCP/UDP)
- Status (open / closed / filtered)
- Timestamp of when it was scanned
- Banner/service info (if grabbed)
- Response time (useful for diagnostics)

* * *

**In-Memory Recording** The simplest approach — store results in a data structure as the scan runs. A list of objects/dicts works well. You build up the full result set in memory, then output it all at the end. Fine for small scans, but if the scan crashes midway you lose everything.

* * *

**Live/Streaming Recording** Write each result immediately as it's found rather than waiting for the scan to finish. This way, even if the scan is interrupted, you have partial results. Essential for large scans (e.g. full 65535 port range).

* * *

**Log Levels** Structure your logging with levels, just like any real application:

| Level | What it captures |
| --- | --- |
| DEBUG | Every attempt, every timeout, raw socket info |
| INFO | Open ports, scan start/end, summary |
| WARNING | Retries, unexpected responses |
| ERROR | Connection errors, host unreachable |

Let the user control the verbosity level via a CLI flag.

* * *

**Output Formats** Plan to support at least two:

- **Plain text** — human readable, one line per open port, easy to grep
- **JSON** — structured, machine-readable, easy to feed into other tools
- **CSV** — good for importing into spreadsheets or databases
- **XML** — if you want nmap-compatible output for tool interoperability

* * *

**File vs. Console Output**

- Always print to console by default (live feedback while scanning)
- Optionally write to a file simultaneously (via a flag like `--output results.txt`)
- For JSON/CSV, write to file only — printing raw JSON to terminal isn't useful

* * *

**Timestamping** Record at three levels:

- **Scan start/end time** — overall duration
- **Per-host start/end** — useful when scanning multiple hosts
- **Per-port timestamp** — useful for debugging and forensic-style logging

* * *

**Structured Log Entry Example (conceptually)** Each result record should look something like:

```
host: 192.168.1.1
port: 443
protocol: TCP
status: open
banner: "nginx/1.24.0"
response_time_ms: 42
scanned_at: 2026-05-17T10:23:01Z
```

* * *

**Summary Report** At the end of every scan, always emit a summary:

- Total ports scanned
- Number open / closed / filtered
- Scan duration
- Hosts that were unreachable

* * *

**The recommended stack:**

1.  **In-memory list** to collect results during the scan
2.  **Live console output** for open ports as they're found (don't make users wait)
3.  **JSON file output** as the save format — it's the most versatile
4.  **Summary block** printed at the end of every run

&nbsp;

![2320af1ed9df8ac56a8f2c62e3cf3101.png](../_resources/2320af1ed9df8ac56a8f2c62e3cf3101.png)