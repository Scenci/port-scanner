import socket                                                                                                                                                                                                                                          
import time
def port_scan(host, port):                                                                                                                                                                                                                              
    s = socket.socket()                                                                                                                                                                                                                                 
    try:                                                                                                                                                                                                                                                
        s.settimeout(2)                                                                                                                                                                                                                                 
        s.connect((host,port))                                                                                                                                                                                                                          
        return True                                                                                                                                                                                                                                     
    except(OSError, socket.timeout, ConnectionRefusedError):                                                                                                                                                                                                    return False                                                                                                                                                                                                                                    
    finally:                                                                                                                                                                                                                                            
        s.close()                                                                                                                                                                                                                                       

ST=time.time()
for i in range(0,500):                                                                                                                                                                                                                                 
    if(port_scan("trashhosttester",i) == True):                                                                                                                                                                                                         
        print(f"{i}: Port is Open")
ET=time.time()
print(f"Checked All Ports in {ET - ST:.2f} seconds")
