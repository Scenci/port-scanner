import socket
import concurrent.futures
import time
import sys
import argparse
from tqdm import tqdm

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

def threaded_scanner(addr, ports):
    open_ports = []
    ports_list = list(ports)  # Convert to list for length calculation
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures_to_port = {
            executor.submit(port_scan, addr, port): port
            for port in ports_list
        }
        
        # Progress bar with light blue color
        with tqdm(
            total=len(ports_list),
            desc="Scanning",
            unit="port",
            colour="#00BFFF",  # Light blue (Deep Sky Blue)
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        ) as pbar:
            for future in concurrent.futures.as_completed(futures_to_port):
                port = futures_to_port[future]
                try:
                    if future.result():
                        open_ports.append(port)
                except Exception:
                    pass
                pbar.update(1)
    
    return sorted(open_ports)

def main():
    # Disclaimer: Please only scan ports you have explicit permission to scan.

    parser = argparse.ArgumentParser(description="Usage: Scan PortStart to PortEnd on Host")
    
    parser.add_argument("-t","--top",action="store_true", help="scans top 100 ports")
    parser.add_argument("host", type=str, help="The Host you wish to scan")
    parser.add_argument("ps", nargs="?", type=int, help="port to start the scan from before incrementing to the next port")
    parser.add_argument("pe", nargs="?", type=int, help="port to end the scan at")
    
    args = parser.parse_args()

    futures_to_port={} # Used for tracking the port-to-future (thread) so we can see it on the other "end" of the concurrency.
    
    top_100_ports = [
    21,22,23,25,53,80,110,111,135,139,
    143,443,445,993,995,1723,3306,3389,
    5900,8080,8443,1433,1521,5432,6379,
    27017,9200,5601,11211,2049,5060,
    5901,8000,8008,8888,9000,9090,
    7001,7002,9443,6667,389,636,
    500,4500,20,69,123,161,162,179,389,427,4433,5000,
    5001,5061,5433,5600,6000,6001,6666,7000,
    7007,7100,7777,8001,8002,8009,8081,8088,
    8181,8880,8888,9001,9002,9042,9080,9091,
    9201,9418,9999,10000,27018,27019
    ]

    start_time = time.time()
    
    try:
        addr = resolve_host(args.host)
    except concurrent.futures.TimeoutError:
        print(f"DNS resolution timed out after {DNS_TIMEOUT}s")
        return
    except socket.gaierror:
        print("host does not resolve")
        return

    ports = top_100_ports if args.top else range(args.ps, args.pe + 1)
    
    print(f"\nScanning {args.host}...")
    print("-" * 40)
    
    open_ports = threaded_scanner(addr, ports)
    
    print("-" * 40)
    if open_ports:
        print(f"\nOpen ports found: {len(open_ports)}")
        for port in open_ports:
            print(f"  {port}/tcp  open")
    else:
        print("\nNo open ports found.")
    
    end_time=time.time()
    print(f"\nCompleted in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
