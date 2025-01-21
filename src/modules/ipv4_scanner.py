import socket


class IPv4Scanner:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def scan(self, ip_ranges):
        open_ports = []
        for ip in ip_ranges:
            if self._is_port_open(ip, 23) or self._is_port_open(ip, 2323):
                open_ports.append(ip)
        return open_ports

    def _is_port_open(self, ip, port):
        try:
            with socket.create_connection((ip, port), timeout=self.timeout):
                return True
        except socket.error:
            return False
