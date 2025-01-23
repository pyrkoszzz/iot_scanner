import telnetlib
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple, Dict, List

from src.modules.logging_service import logger


class Authenticator:
    @staticmethod
    def detect_open_telnet(
        ip: str, port: int, timeout: int = 3
    ) -> Tuple[str, int] | None:
        """Attempts to detect open Telnet servers without authentication.

        Args:
            ip (str): The target IP address.
            port (int): The target port number.
            timeout (int): The connection timeout.

        Returns:
            Tuple[str, int]: The IP address and port number if Telnet is open.
        """
        try:
            with telnetlib.Telnet(ip, port, timeout=timeout) as tn:
                tn.write(b"echo $?\n")
                response = tn.read_until(b"\n", timeout=timeout).decode("ascii")
                if response.strip():
                    logger.info(f"[+] Open Telnet detected on {ip}:{port}")
                    return ip, port
        except Exception:
            pass
        return None

    @staticmethod
    def attempt_telnet_auth(
        ip: str, port: int, username: str, password: str, timeout: int = 3
    ) -> Tuple[str, str, str] | None:
        """Attempts to authenticate to a Telnet server using provided credentials."""
        try:
            with telnetlib.Telnet(ip, port, timeout=timeout) as tn:
                tn.read_until(b"login: ", timeout=timeout)
                tn.write(username.encode("ascii") + b"\n")
                tn.read_until(b"Password: ", timeout=timeout)
                tn.write(password.encode("ascii") + b"\n")
                tn.write(b"echo $?\n")
                response = tn.read_until(b"\n", timeout=timeout).decode("ascii")
                if "0" in response.strip():
                    logger.info(
                        f"[+] Successful login on {ip} with {username}/{password}"
                    )
                    return ip, username, password
        except Exception as e:
            pass
        return None

    def telnet_open_scan(
        self, ip_list: Dict[str, int], max_threads: int = 50
    ) -> list[Tuple[str, int]]:
        """Scans a list of IPs for open Telnet servers.

        Args:
            ip_list (Dict[str, int]): A dictionary of IP addresses and port numbers.
            max_threads (int): The maximum number of threads to use.

        Returns:
            list[Tuple[str, int]]: A list of IP addresses and port numbers with open Telnet servers.
        """
        open_telnets = []
        with ThreadPoolExecutor(max_threads) as executor:
            futures = {
                executor.submit(self.detect_open_telnet, ip, port): (ip, port)
                for ip, port in ip_list.items()
            }
            for future in futures:
                result = future.result()
                if result:
                    open_telnets.append(result)
        return open_telnets

    def telnet_auth_scan(
        self,
        ip_list: Dict[str, int],
        credentials: List[List[str]],
        max_threads: int = 50,
    ) -> List[Tuple[str, str, str]]:
        """Attempts Telnet authentication on a list of IPs using given credentials.

        Args:
            ip_list (Dict[str, int]): A dictionary of IP addresses and port numbers.
            credentials (List[List[str]]): A list of username/password combinations.
            max_threads (int): The maximum number of threads to use.

        Returns:
            List[Tuple[str, str, str]]: A list of successful logins.
        """
        successful_logins = []
        with ThreadPoolExecutor(max_threads) as executor:
            futures = {
                executor.submit(
                    self.attempt_telnet_auth, ip, port, username, password
                ): (
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
