import socket
import sys
from datetime import datetime

# Target-ne define cheyyuka (e.g., localhost or scanme.nmap.org)
target = input("Enter the target IP or Domain to scan: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("\n[-] Hostname could not be resolved. Exiting.")
    sys.exit()

print("-" * 50)
print(f"Scanning Target: {target_ip}")
print(f"Time Started: {str(datetime.now())}")
print("-" * 50)

# Ethoke ports scan cheynom ennu thirumanikkuka (e.g., Common Ports: 21, 22, 23, 25, 80, 443)
ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]

try:
    for port in ports:
        # socket.AF_INET = IPv4, socket.SOCK_STREAM = TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0) # Connection time-out settings
        
        # Port open aano ennu check cheyyunnu
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            print(f"[+] Port {port}: OPEN")
            
            # --- Banner Grabbing Section ---
            try:
                # Chila services connection kittiyathum banner tharum
                banner = s.recv(1024).decode().strip()
                if banner:
                    print(f"    --> Banner: {banner}")
            except:
                # Banner kittiyillengil, request aychu nokkaam (mainly for HTTP 80/443)
                try:
                    s.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
                    banner = s.recv(1024).decode().strip()
                    # Just printing the first line of the response header
                    print(f"    --> Banner/Header: {banner.splitlines()[0]}")
                except:
                    print("    --> Banner: Could not grab banner.")
                    
        s.close()

except KeyboardInterrupt:
    print("\n[-] Exiting script.")
    sys.exit()
except socket.error:
    print("\n[-] Could not connect to server.")
    sys.exit()
