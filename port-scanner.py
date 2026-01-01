import socket
import concurrent.futures
import time
import sys
import argparse


DNS_TIMEOUT = 2
CONNECT_TIMEOUT = 2
MAX_WORKERS = 100

def resolve_host(host, timeout=DNS_TIMEOUT):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(socket.getaddrinfo, host, None, type=socket.SOCK_STREAM)
        infos = future.result(timeout=timeout)
        if not infos:
            raise socket.gaierror("no addresses returned")
        return infos[0]  # (family, socktype, proto, canonname, sockaddr)


def port_scan(addrinfo, port):
    try:
        family, socktype, proto, _, sockaddr = addrinfo

        with socket.socket(family, socktype, proto) as s:
            s.settimeout(CONNECT_TIMEOUT)

            # Replace the port inside sockaddr (IPv4 is 2-tuple, IPv6 is 4-tuple)
            if family == socket.AF_INET:
                target = (sockaddr[0], port)
            else:
                target = (sockaddr[0], port, sockaddr[2], sockaddr[3])

            s.connect(target)
            return True

    except (OSError, ConnectionRefusedError, socket.gaierror, socket.timeout):
        return False


def main():
    parser = argparse.ArgumentParser(description="Usage: Scan PortStart to PortEnd on Host")

    parser.add_argument("host", type=str, help="The Host you wish to scan")
    parser.add_argument("ps", type=int, help="port to start the scan from before incrementing to the next port")
    parser.add_argument("pe", type=int, help="port to end the scan at")

    args = parser.parse_args()

    futures_to_port={} # Used for tracking the port-to-future (thread) so we can see it on the other "end" of the concurrency.

    start_time = time.time()

    try:
        addr = resolve_host(args.host)
    except concurrent.futures.TimeoutError:
        print(f"DNS resolution timed out after {DNS_TIMEOUT}s")
        return
    except socket.gaierror:
        print("host does not resolve")
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures_to_port = {
            executor.submit(port_scan, addr, port): port
            for port in range(args.ps, args.pe + 1)
        }

        for future in concurrent.futures.as_completed(futures_to_port):
            port = futures_to_port[future]
            try:
                if future.result():
                    print(f"{port} Port is Open")
            except Exception:
                pass

    end_time=time.time()
    print(f"Checked All Ports in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
