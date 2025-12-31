import socket
import concurrent.futures
import time
import sys
import argparse

def port_scan(host, port):
    s = socket.socket()
    try: 
        s.settimeout(2)
        s.connect((host,port))
        return True
    except(OSError, socket.timeout):
        return False
    finally:
        s.close()

def main():
    parser = argparse.ArgumentParser(description="Usage: Scan PortStart to PortEnd on Host")

    parser.add_argument("host", type=str, help="The Host you wish to scan")
    parser.add_argument("ps", type=int, help="port to start the scan from before incrementing to the next port")
    parser.add_argument("pe", type=int, help="port to end the scan at")

    args = parser.parse_args()

    futures_to_port={} # Used for tracking the port-to-future (thread) so we can see it on the other "end" of the concurrency.
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:   
        futures_to_port = {
            executor.submit(port_scan,args.host,port): port 
            for port in range(args.ps, args.pe + 1)
        }

        for future in concurrent.futures.as_completed(futures_to_port):
            port = futures_to_port[future]
            if future.result():
                print(f"{port} Port is Open")

    end_time=time.time()
    print(f"Checked All Ports in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
