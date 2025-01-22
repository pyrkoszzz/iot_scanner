import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor


class IPv4Scanner:
    def __init__(self, timeout=2):
        self.timeout = timeout

    def scan_ip(self, ip, ports):
        """Scans a single IP address on a list of ports."""
        open_ports = []
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)  # Set timeout to 1 second
                    s.connect((ip, port))
                    open_ports.append(port)
            except (socket.timeout, socket.error):
                pass
        return ip, open_ports

    def scan_range(self, ip_range, ports, max_threads=100):
        """Scans a range of IP addresses for activity on a list of ports."""
        results = {}
        with ThreadPoolExecutor(max_threads) as executor:
            futures = {
                executor.submit(self.scan_ip, str(ip), ports): ip
                for ip in ipaddress.IPv4Network(ip_range, strict=False)
            }
            for future in futures:
                ip = futures[future]
                try:
                    result_ip, open_ports = future.result()
                    if open_ports:
                        results[result_ip] = open_ports
                        print(
                            f"[+] Active IP found: {result_ip} with open ports: {open_ports}"
                        )
                except Exception as e:
                    print(f"[-] Error scanning IP {ip}: {e}")
        return results
