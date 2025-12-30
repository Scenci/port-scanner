import socket
import concurrent.futures
import time

def port_scan(host, port):
    
    s = socket.socket()

    try: 
        s.settimeout(2)
        s.connect((host,port))
        return True
    except:
        return False
    finally:
        s.close()

def main():
    futures_to_port={} # Used for tracking the port-to-future (thread) so we can see it on the other "end" of the concurrency.
    start_time = time.time()
    targetHost="scanme.nmap.org"
    with concurrent.futures.ThreadPoolExecutor() as executor:   
        futures_to_port = {executor.submit(port_scan,targetHost,port): port for port in range(20,101)}
        for future in concurrent.futures.as_completed(futures_to_port):
            port = futures_to_port[future]
            if future.result():
                print(f"{port} Port is Open")

    end_time=time.time()
    print(f"Checked All Ports in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
