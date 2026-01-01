# Port Scanner

A fast, multi-threaded TCP port scanner written in Python. Built as a learning project to explore networking fundamentals, socket programming, and concurrency.

## Features

- **Multi-threaded scanning** — Uses `ThreadPoolExecutor` for concurrent port scanning (up to 100 threads)
- **IPv4 and IPv6 support** — Automatically handles both address families
- **DNS resolution with timeout** — Graceful handling of unresolvable hosts
- **Top 100 common ports mode** — Quick scan of the most frequently open ports
- **Custom port ranges** — Specify any start and end port
- **Progress bar** — Visual feedback with colored progress indicator
- **Clean output** — Sorted results with scan timing

## Requirements

- Python 3.8+
- tqdm

## Installation

```bash
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner
pip install -r requirements.txt
```

Or install dependencies manually:

```bash
pip install tqdm
```

## Usage

### Basic Syntax

```bash
python port-scanner.py [OPTIONS] HOST [PORT_START] [PORT_END]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `HOST` | Yes | Target hostname or IP address |
| `PORT_START` | No* | First port in range to scan |
| `PORT_END` | No* | Last port in range to scan |

*Required unless using `-t` flag

### Options

| Option | Description |
|--------|-------------|
| `-t`, `--top` | Scan top 100 common ports instead of a range |
| `-h`, `--help` | Show help message |

### Examples

Scan a custom port range:
```bash
python port-scanner.py scanme.nmap.org 1 1000
```

Scan top 100 common ports:
```bash
python port-scanner.py -t scanme.nmap.org
```

Scan localhost:
```bash
python port-scanner.py 127.0.0.1 20 100
```

Scan specific small range:
```bash
python port-scanner.py 192.168.1.1 80 443
```

## Example Output

```
Scanning scanme.nmap.org...
----------------------------------------
Scanning: 100%|████████████████| 100/100 [00:02<00:00]
----------------------------------------

Open ports found: 3
  22/tcp  open
  53/tcp  open
  80/tcp  open

Completed in 2.34 seconds
```

## How It Works

The scanner uses **TCP connect scanning**, performing a full three-way handshake to determine port status:

| Response | Meaning |
|----------|---------|
| SYN-ACK | Port is open (service listening) |
| RST | Port is closed (no service) |
| Timeout | Port is filtered (firewall blocking) |

### Architecture

1. **DNS Resolution** — Hostname resolved with configurable timeout
2. **Thread Pool** — Up to 100 concurrent workers scan ports simultaneously  
3. **Result Collection** — Futures tracked via dictionary mapping for port identification
4. **Progress Display** — Real-time progress bar updates as scans complete

## Configuration

Default values can be modified at the top of `port-scanner.py`:

```python
DNS_TIMEOUT = 2      # Seconds to wait for DNS resolution
CONNECT_TIMEOUT = 2  # Seconds to wait for port connection
MAX_WORKERS = 100    # Maximum concurrent threads
```

## Top 100 Ports List

The `-t` flag scans these commonly open ports:

| Category | Ports |
|----------|-------|
| Remote Access | 21, 22, 23, 3389, 5900, 5901 |
| Web | 80, 443, 8080, 8443, 8000, 8008, 8888 |
| Email | 25, 110, 143, 993, 995 |
| Database | 1433, 1521, 3306, 5432, 6379, 9200, 27017 |
| File Sharing | 20, 69, 111, 135, 139, 445, 2049 |
| DNS/Network | 53, 123, 161, 162, 179, 389, 636 |

## Performance

Benchmarks scanning `scanme.nmap.org`:

| Port Range | Time |
|------------|------|
| 80 ports (sequential) | ~4.0s |
| 80 ports (threaded) | ~0.4s |
| Top 100 ports | ~2.5s |
| 1000 ports | ~25s |

## Legal Disclaimer

**⚠️ Only scan systems you own or have explicit permission to test.**

Port scanning without authorization may be illegal in your jurisdiction and typically violates terms of service. This tool was developed for educational purposes using [scanme.nmap.org](http://scanme.nmap.org), a server specifically provided by the Nmap project for testing.

## Project Structure

```
port-scanner/
├── port-scanner.py       # Main concurrent scanner
├── mono-port-scanner.py  # Sequential version (for comparison)
├── requirements.txt      # Python dependencies
├── README.md
└── .gitignore
```

## What I Learned

Building this project covered:

- **TCP/IP fundamentals** — Three-way handshake, port states, timeouts
- **Socket programming** — Python's `socket` module, address families
- **Concurrency** — `ThreadPoolExecutor`, futures, dictionary comprehensions
- **CLI design** — `argparse` for professional command-line interfaces
- **Error handling** — Graceful failures for DNS, connections, timeouts

## Future Improvements

- [ ] Banner grabbing (service identification)
- [ ] UDP scanning
- [ ] Output formats (JSON, CSV)
- [ ] Verbose mode with per-port timing
- [ ] Rate limiting options

## License

MIT
