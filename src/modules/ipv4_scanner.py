import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple

from src.modules.logging_service import logger


class IPv4Scanner:
    def __init__(self):
        self.timeout = 1
        self.max_threads = 100

    def scan_ip(self, ip: str, ports: List[int]) -> Tuple[str, int] | Tuple[None, None]:
        """Scans a single IP address on a list of ports.

        Args:
            ip (str): The IP address to scan.
            ports (list): A list of ports to scan.

        Returns:
            tuple: A tuple containing the IP address and open port, or None.
        """
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(self.timeout)
                    s.connect((ip, port))
                    return ip, port
            except (socket.timeout, socket.error):
                pass
        return None, None

    def scan_range(self, ip_range: str, ports):
        """Scans a range of IP addresses for activity on a list of ports."""
        results = {}
        with ThreadPoolExecutor(self.max_threads) as executor:
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
                        logger.info(
                            f"[+] Active IP found: {result_ip} with open ports: {open_ports}"
                        )
                except Exception as e:
                    logger.error(f"[-] Error scanning IP {ip}: {e}")
        return results
