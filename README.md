# Port Scanner

A Python-based TCP port scanner built as a learning project to explore networking fundamentals and concurrency.

## Overview

This project contains two implementations of a port scanner:

- **mono-port-scanner.py** — Sequential, single-threaded scanner
- **port-scanner.py** — Concurrent, multi-threaded scanner using `ThreadPoolExecutor`

The concurrent version achieves approximately **10x faster performance** by scanning multiple ports simultaneously.

## How It Works

The scanner uses TCP connect scanning, which performs a full TCP three-way handshake (SYN → SYN-ACK → ACK) to determine port status:

| Response | Port Status |
|----------|-------------|
| SYN-ACK received | Open |
| RST received | Closed |
| Timeout (no response) | Filtered |

## Requirements

- Python 3.8+
- No external dependencies (uses standard library only)

## Usage

### Sequential Scanner
```bash
python mono-port-scanner.py
```

### Concurrent Scanner
```bash
python port-scanner.py
```

## Example Output
```
22 Port is Open
53 Port is Open
80 Port is Open
Checked All Ports in 0.38 seconds
```

## Performance Comparison

Scanning ports 20-100 on `scanme.nmap.org`:

| Version | Time |
|---------|------|
| Sequential | ~4.0 seconds |
| Concurrent | ~0.4 seconds |

## Legal Disclaimer

Port scanning without permission may be illegal in your jurisdiction. Only scan systems you own or have explicit authorization to test. This tool was developed for educational purposes using [scanme.nmap.org](http://scanme.nmap.org), which permits scanning.

## Future Improvements

- [ ] Command-line argument parsing (target, port range, thread count)
- [ ] Service/banner detection
- [ ] Common ports mode
- [ ] Output formatting options (JSON, CSV)

## License

MIT
