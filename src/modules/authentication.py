import telnetlib
from concurrent.futures import ThreadPoolExecutor


class Authenticator:
    def attempt_telnet_auth(self, ip, port, username, password, timeout=3):
        """Attempts to authenticate to a Telnet server using provided credentials."""
        try:
            with telnetlib.Telnet(ip, port, timeout=timeout) as tn:
                tn.read_until(b"login: ", timeout=timeout)
                tn.write(username.encode('ascii') + b"\n")
                tn.read_until(b"Password: ", timeout=timeout)
                tn.write(password.encode('ascii') + b"\n")
                tn.write(b"echo $?\n")
                response = tn.read_until(b"\n", timeout=timeout).decode('ascii')
                if "0" in response.strip():
                    print(f"[+] Successful login on {ip} with {username}/{password}")
                    return ip, username, password
        except Exception as e:
            pass  # Handle errors silently for simplicity
        return None

    def telnet_auth_scan(self, ip_list, credentials, max_threads=50):
        """Attempts Telnet authentication on a list of IPs using given credentials."""
        successful_logins = []
        with ThreadPoolExecutor(max_threads) as executor:
            futures = {
                executor.submit(self.attempt_telnet_auth, ip, port, username, password): (
                    ip,
                    username,
                    password,
                )
                for ip, port in ip_list.items()
                for username, password in credentials
            }
            for future in futures:
                result = future.result()
                if result:
                    successful_logins.append(result)
        return successful_logins
