import socket
from datetime import datetime

def scan(h, p): 
    """
    sets up a socket and tries to connect to host h's port p
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket init
    s.settimeout(5) #timeout to throw an exception if the socket is hanging
    
    try: # t/e/f block connecting to the port
        s.connect((h,p))
        status = "open" # upon a succesfull connection set status to open
    
    except:
        status = "closed"

    finally:
        s.close()
    
    
    print(f"Port {p} is {status}") #lets print the output

def main():

    ip = input("Enter a target to scan: ")
    print("Enter the range of ports you would like to scan on the target")
    s = input("Enter a start port: ")
    e = input("Enter a end port: ")

    print(f"Scanning started at: {datetime.now().time()}") # datetime lib for the timestamp

    for i in range(int(s),int(e)+1): #loop thru the port ranges and call scan
        scan(ip, i) 
    print("Port scanning completed")
if __name__ == "__main__":
    main()
