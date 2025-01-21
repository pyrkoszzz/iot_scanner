import telnetlib


class Authenticator:
    def authenticate(self, open_ports, credentials):
        vulnerable_devices = []
        for ip in open_ports:
            for username, password in credentials:
                if self._try_login(ip, username, password):
                    vulnerable_devices.append(
                        {"ip": ip, "username": username, "password": password}
                    )
                    break
        return vulnerable_devices

    @staticmethod
    def _try_login(ip, username, password):
        try:
            tn = telnetlib.Telnet(ip, timeout=5)
            tn.read_until(b"login:")
            tn.write(username.encode("ascii") + b"\n")
            tn.read_until(b"Password:")
            tn.write(password.encode("ascii") + b"\n")
            tn.close()
            return True
        except:
            return False
