import socket
import argparse
import sys

# Predefined mapping of common ports to their services
PORTS_SERVICES = {
    20: "FTP Data Transfer",
    21: "FTP Control",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP Alternate",
}

def scan_port(target, port):
    """Attempt to connect to a given port on the target."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)  # Set a timeout for the connection attempt
        result = sock.connect_ex((target, port))  # Returns 0 if successful
        return result == 0

def main(target, start_port, end_port):
    """Scan the specified range of ports on the target."""
    print(f"Scanning {target} from port {start_port} to {end_port}...")
    for port in range(start_port, end_port + 1):
        if scan_port(target, port):
            service = PORTS_SERVICES.get(port, "unknown service")
            print(f"Port {port}: open ({service})")
        else:
            print(f"Port {port}: closed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Port Scanner')
    parser.add_argument('-t', '--target', required=True, help='Target IP address or domain')
    parser.add_argument('-p', '--ports', required=True, help='Port range (e.g., 20-100)')
    
    args = parser.parse_args()

    # Parse the port range
    try:
        start_port, end_port = map(int, args.ports.split('-'))
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError("Invalid port range.")
    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)

    main(args.target, start_port, end_port)
