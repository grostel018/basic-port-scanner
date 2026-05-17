# Port Scanner v1

Single file, no external dependencies, standard library only.

## Goal

A minimal TCP port scanner that runs from the command line, prints open ports live, and shows a summary at the end.

## Usage

```
python scanner.py <host> <port-range>
python scanner.py 192.168.1.1 1-1024
```

## What's in v1

| Step | What it does |
|------|-------------|
| CLI inputs | Accepts host and port range via `sys.argv` |
| `scan_port()` | Tries to connect to a port, returns `"open"` or `"closed"` |
| Thread pool | ~100 workers via `concurrent.futures.ThreadPoolExecutor` |
| Live output | Prints open ports as they are found using `as_completed()` |
| Summary | Total scanned, open count, elapsed time |

## Standard library used

- `socket` — makes the TCP connection
- `concurrent.futures` — thread pool
- `datetime` — timing
- `sys` — CLI arguments

## What's intentionally left out (v2)

- Error handling / bad input validation
- Banner grabbing
- File output / JSON
- UDP scanning
- Multiple hosts / CIDR ranges
