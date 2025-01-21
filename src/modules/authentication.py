import telnetlib


class Authenticator:
    def authenticate(self, open_ports, credentials):
        vulnerable_devices = []
        for ip in open_ports:
            if self._check_if_authenticated(ip):
                vulnerable_devices.append({"ip": ip, "username": "", "password": ""})
                continue
            for username, password in credentials:
                if self._try_login(ip, username, password):
                    vulnerable_devices.append(
                        {"ip": ip, "username": username, "password": password}
                    )
                    break
        return vulnerable_devices

    def _try_login(self, ip, username, password):
        try:
            tn = telnetlib.Telnet(ip, timeout=5)
            prompt = tn.read_until(b"login:", timeout=5)
            if b"login:" not in prompt:
                tn.close()
                return False
            tn.write(username.encode("ascii") + b"\n")
            prompt = tn.read_until(b"Password:", timeout=5)
            if b"Password:" not in prompt:
                tn.close()
                return False
            tn.write(password.encode("ascii") + b"\n")
            tn.write(b"echo $?\n")
            prompt = tn.read_until(b"$", timeout=5)
            if b"0" in prompt:
                return True
        except Exception:
            return False

    @staticmethod
    def _check_if_authenticated(ip):
        try:
            tn = telnetlib.Telnet(ip, timeout=5)
            tn.write(b"echo $?\n")
            response = tn.read_until(b"\n", timeout=5)
            return b"0" in response
        except Exception:
            return False
