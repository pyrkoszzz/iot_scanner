# IoT Network Scanner Documentation

## Overview

This project is an IoT network scanner designed to scan IP ranges, identify open ports, perform authentication scans (specifically for Telnet services), enrich scan results using Shodan, and generate comprehensive scan reports. The tool can be run via the command line, where the user can specify various options to perform specific types of scans and enrich the results.


## 1. Functionality Breakdown:

1. **Argument Parsing** (`parser.parse_args()`):
   - Uses `CLIParser` to parse command-line arguments and decide which operations to perform.

2. **Credential Management** (`credential_manager.load_credentials()`):
   - If credentials are provided, loads the credentials using `CredentialManager`.

3. **IP Range Scan** (`handle_ip_scan()`):
   - Scans the specified IP range for open ports if the `--scan-ips` or `--scan-telnet-open` argument is provided.

4. **Telnet Open Scan** (`handle_telnet_open_scan()`):
   - Identifies devices with open Telnet services.

5. **Telnet Authentication Scan** (`handle_telnet_auth_scan()`):
   - Performs Telnet authentication using the loaded credentials.

6. **Shodan Enrichment** (`handle_shodan_enrichment()`):
   - Enriches scan results with Shodan data for each detected device.

7. **Report Generation** (`report_generator.generate_report()`):
   - Generates a JSON report of the scan results and saves it to the specified file.

8. **Logging**:
   - Logs each step of the process for debugging and informational purposes using the `LoggingService`.

---

## 2. **Example Usage**

Here are a few example command-line executions to demonstrate the functionality of the IoT Scanner:

### Example 1: Basic IP Scan for Open Ports

```bash
python main.py --scan-ips --ip-range 192.168.1.0/24 --ports 23 2323 --report-file results/scan_report.json
```

### Example 2: Scan for Open Telnet Devices and Perform Authentication

```bash
python main.py --scan-telnet-auth --ip-range 192.168.1.0/24 --ports 23 --credentials config/credentials.csv --report-file results/scan_report.json
```

### Example 3: Scan with Shodan Enrichment

```bash
python main.py --scan-telnet-open --ip-range 192.168.1.0/24 --ports 23 --shodan-enrichment --report-file results/scan_report.json
```

---
## 3. **Module Details**
### **CLI Interface** (`cli_parser.py`)

The `CLIParser` class handles parsing of command-line arguments, enabling the user to configure scanning operations.

#### Functions:

- **get_parser**:
  - Returns the argument parser with the following command-line options:
    - `--scan-ips`: Scans the specified IP range for open ports.
    - `--scan-telnet-open`: Scans for open Telnet devices.
    - `--scan-telnet-auth`: Performs Telnet authentication scans using credentials.
    - `--ports`: Specifies the list of ports to scan (default: 23, 2323).
    - `--ip-range`: Specifies the IP range to scan (e.g., `192.168.0.1/24`).
    - `--credentials`: Path to a CSV file containing credentials for authentication scans.
    - `--shodan-enrichment`: Enriches scan results with Shodan data.
    - `--report-file`: Specifies the path for saving the scan report (default: `reports/scan_report.json`).

---

### **Credential Management** (`credential_source.py`)

The `CredentialManager` class is responsible for managing credentials used for authentication scans.

#### Functions:

- **load_credentials**:
  - Loads credentials from a file (default: `config/credentials/default_creds.csv`).
  - Returns a list of credentials (username/password combinations).
  
- **_load_local_creds**:
  - Reads credentials from the local file and returns them as a list.

---

### **Handlers** (`handlers.py`)

The handler functions orchestrate various types of scans based on the user’s input.

#### Functions:

- **handle_ip_scan**:
  - Scans the specified IP range for open ports.
  - Returns a dictionary containing IP addresses and their open ports.

- **handle_telnet_open_scan**:
  - Identifies devices with open Telnet services by scanning the given list of open ports.
  - Returns a list of devices with open Telnet ports.

- **handle_telnet_auth_scan**:
  - Performs Telnet authentication attempts on devices with open Telnet ports using the provided credentials.
  - Returns a list of devices with successful authentication.

- **handle_shodan_enrichment**:
  - Enriches the scan results with Shodan data by retrieving information from the Shodan database for each detected device.
  - Returns a list of enriched devices with Shodan data.

---

### **IPv4 Scanner** (`ipv4_scanner.py`)

The `IPv4Scanner` class is responsible for scanning IP ranges for open ports.

#### Functions:

- **scan_ip**:
  - Scans a single IP address on a list of ports.
  - Returns a tuple with the IP address and an open port, or `None, None` if no open ports are found.

- **scan_range**:
  - Scans an entire range of IP addresses (IPv4 range) for open ports.
  - Uses multi-threading (`ThreadPoolExecutor`) for efficient scanning.
  - Returns a dictionary with IP addresses and their open ports.

---

### **Logging Service** (`logging_service.py`)

The `LoggingService` class provides centralized logging functionality, with file rotation and multiple log levels.

#### Functions:

- **__init__**:
  - Initializes the logging system with a file path, log level, file size limit, and backup count.
  
- **_configure_handlers**:
  - Configures the logging handlers (console and file) with a formatter.
  
- **get_logger**:
  - Returns the logger instance for use throughout the application.

- **_get_formatter**:
  - Returns a standard log formatter.

---

### **Report Generator** (`report_generator.py`)

The `ReportGenerator` class is responsible for generating a JSON report based on the scan results.

#### Functions:

- **generate_report**:
  - Generates a report of the devices found during the scan and saves it as a JSON file.
  - Accepts a dictionary of devices and writes it to the specified report file.

---

### **Shodan Client** (`shodan_client.py`)

The `ShodanClient` class interacts with the Shodan API to retrieve information about devices using their IP address.

#### Functions:

- **__init__**:
  - Initializes the Shodan client using an API key from the environment variable `SHODAN_API_KEY`.

- **get_device_info**:
  - Fetches information about a device using its IP address from the Shodan API.
  - Returns device information or `None` if an error occurs.

---

## 4. **Architecture**
The `Authenticator` module is responsible for:
1. **Detecting open Telnet servers** (without authentication).
2. **Attempting authentication on Telnet servers** using a list of credentials.
3. **Multi-threading for performance optimization** to speed up scanning.
4. **Logging** important events for debugging and tracking.

It integrates with:
- `ThreadPoolExecutor` for concurrent scanning.
- `telnetlib` for Telnet interactions.
- `logger` (from `logging_service`) for tracking results.

**Class and Method Overview**
- `detect_open_telnet(ip, port, timeout)`: Checks if a Telnet server is open on a given IP and port.
- `attempt_telnet_auth(ip, port, username, password, timeout)`: Tries logging in using credentials.
- `telnet_open_scan(ip_list, max_threads)`: Scans multiple IPs concurrently for open Telnet servers.
- `telnet_auth_scan(ip_list, credentials, max_threads)`: Attempts authentication on open Telnet servers.

---

## **Implementation Details**
### **Detecting Open Telnet Servers**
This method attempts to connect to a Telnet server and sends a basic command (`echo $?`). If a response is received, the server is considered open.

```python
@staticmethod
def detect_open_telnet(ip: str, port: int, timeout: int = 3) -> Tuple[str, int] | None:
    """Attempts to detect open Telnet servers without authentication."""
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
```
- **Input:** IP address and port.
- **Output:** The IP and port if Telnet is open.

### **Attempting Authentication**
This method interacts with the Telnet server, sending login credentials and checking if authentication is successful.

```python
@staticmethod
def attempt_telnet_auth(ip: str, port: int, username: str, password: str, timeout: int = 3) -> Tuple[str, str, str] | None:
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
                logger.info(f"[+] Successful login on {ip} with {username}/{password}")
                return ip, username, password
    except Exception:
        pass
    return None
```
- **Input:** IP, port, username, and password.
- **Output:** The IP and successful credentials if login is successful.

### **Scanning for Open Telnet Servers**
Uses threading to scan multiple IPs concurrently.

```python
def telnet_open_scan(self, ip_list: Dict[str, int], max_threads: int = 50) -> list[Tuple[str, int]]:
    """Scans a list of IPs for open Telnet servers."""
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
```
- **Input:** Dictionary of IPs and ports.
- **Output:** List of open Telnet servers.

### **Performing Authentication Scans**
Tests multiple credentials against open Telnet servers.

```python
def telnet_auth_scan(self, ip_list: Dict[str, int], credentials: List[List[str]], max_threads: int = 50) -> List[Tuple[str, str, str]]:
    """Attempts Telnet authentication on a list of IPs using given credentials."""
    successful_logins = []
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {
            executor.submit(self.attempt_telnet_auth, ip, port, username, password): (ip, username, password)
            for ip, port in ip_list.items()
            for username, password in credentials
        }
        for future in futures:
            result = future.result()
            if result:
                successful_logins.append(result)
    return successful_logins
```
- **Input:** List of IPs, credentials.
- **Output:** List of successful logins.

---

### **How to Use**
1. **Import and Initialize**
```python
from src.iot_modules.authentication import Authenticator

authenticator = Authenticator()
```

2. **Scanning for Open Telnet Servers**
```python
ip_list = {"192.168.1.1": 23, "192.168.1.2": 23}
open_telnets = authenticator.telnet_open_scan(ip_list)
print(open_telnets)
```

3. **Attempting Authentication**
```python
credentials = [["admin", "admin"], ["root", "password"]]
successful_logins = authenticator.telnet_auth_scan(open_telnets, credentials)
print(successful_logins)
```

---

### **Credential Management**

The `CredentialManager` class is responsible for managing the loading of credentials that will be used for authentication scans. It provides functionality to load both default and locally stored credentials.

#### **Overview:**

- **Initialization:** The class is initialized with a directory where credential files are stored (default is `config/credentials`).
- **Loading Credentials:** The `load_credentials` method loads credentials from both the default and local files and returns them as a list.
- **Local Credential File:** The credentials are stored in a CSV file, and each line in the file corresponds to a set of credentials (username and password).

---

#### **Class Structure:**

```python
import csv
from src.iot_modules.logging_service import logger

class CredentialManager:
    """
    A class to manage credentials for the IoT scanner.
    """

    def __init__(self, creds_directory="config/credentials"):
        """
        Initializes the CredentialManager with a directory for credential files.
        """
        self.creds_directory = creds_directory

    def load_credentials(self):
        """
        Load credentials from the default file and the local file.

        Returns:
            list: A list of credentials in the form [["username", "password"], ...]
        """
        credentials = [["", ""]]  # Adding a default empty credential
        credentials += self._load_local_creds()
        logger.info(f"Loaded {len(credentials) - 1} credentials.")
        return credentials

    def _load_local_creds(self):
        """
        Load credentials from the local file.

        Returns:
            list: A list of credentials in the form [["username", "password"], ...]
        """
        logger.debug("Loading credentials from the local file.")
        filepath = f"{self.creds_directory}/default_creds.csv"
        with open(filepath, "r") as file:
            return [line for line in csv.reader(file)]
```

---

### **How it Works:**

1. **Initialization (`__init__`)**: 
   - This method takes an optional argument, `creds_directory`, which points to the folder where the credentials are stored. By default, this is set to `"config/credentials"`.

2. **Loading Credentials (`load_credentials`)**: 
   - This method is the main entry point for loading credentials. It first initializes the `credentials` list with a default empty credential (`["", ""]`).
   - Then, it calls the private method `_load_local_creds()` to load any additional credentials from a local CSV file.
   - It logs how many credentials were successfully loaded.

3. **Loading Local Credentials (`_load_local_creds`)**: 
   - This method attempts to read credentials from a local CSV file, `default_creds.csv`, located in the specified directory (`creds_directory`).
   - Each line in the file represents a set of credentials (e.g., `username,password`) and is returned as a list of lists.
   - The method logs the action of loading the credentials at a debug level for traceability.

---

### **Example Usage:**

Below is an example of how the `CredentialManager` class might be used to load and retrieve credentials for an authentication scan:

```python
from src.iot_modules.authentication import Authenticator
from src.iot_modules.credential_manager import CredentialManager

# Initialize the CredentialManager
cred_manager = CredentialManager()

# Load credentials
credentials = cred_manager.load_credentials()

# Initialize the Authenticator
authenticator = Authenticator()

# Perform Telnet authentication scan using loaded credentials
open_telnets = [("192.168.1.1", 23), ("192.168.1.2", 23)]  # Example list of open Telnet servers
successful_logins = authenticator.telnet_auth_scan(open_telnets, credentials)

print(f"Successful logins: {successful_logins}")
```

### **How to Customize Credential Storage:**

- **Adding Custom Credentials:** 
   - To add additional credentials, the user simply needs to place them in the `default_creds.csv` file or any other CSV format file specified using the `--credentials` argument in the CLI.

- **Credential Format:** 
   - Each credential should be stored as a pair of `username,password` on each line.

---

### **IPv4 Network Scanning for Open Ports**

The `IPv4Scanner` class is designed to scan IPv4 addresses for open ports by leveraging socket connections. It scans a range of IP addresses for activity on specified ports and provides functionality to conduct these scans concurrently using threads.

#### **Class Overview:**

- **Initialization (`__init__`)**: The class is initialized with a default `timeout` of 1 second and `max_threads` of 100 to handle concurrent scanning.
- **Single IP Scan (`scan_ip`)**: This method attempts to scan a specific IP address across a list of ports, returning the IP and open port if successful.
- **Range Scan (`scan_range`)**: This method scans a given IP range for open ports, returning a dictionary of IP addresses and their open ports.

---

#### **Class Structure:**

```python
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple
from src.iot_modules.logging_service import logger

class IPv4Scanner:
    """A class to scan IPv4 addresses for open ports."""

    def __init__(self):
        """Initialize the scanner with default settings."""
        self.timeout = 1  # Timeout in seconds for each connection attempt
        self.max_threads = 100  # Maximum number of concurrent threads

    def scan_ip(self, ip: str, ports: List[int]) -> Tuple[str, int] | Tuple[None, None]:
        """
        Scans a single IP address on a list of ports.

        Args:
            ip (str): The IP address to scan.
            ports (list): A list of ports to scan.

        Returns:
            tuple: A tuple containing the IP address and open port, or None.
        """
        for port in ports:
            try:
                # Attempt to connect to the given IP and port
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    logger.debug(f"Scanning {ip}:{port}")
                    s.settimeout(self.timeout)
                    s.connect((ip, port))
                    return ip, port  # Return the open IP and port
            except (socket.timeout, socket.error):
                pass  # Ignore errors, continue scanning other ports
        return None, None  # Return None if no open ports found

    def scan_range(self, ip_range: str, ports: List[int]) -> dict:
        """
        Scans a range of IP addresses for activity on a list of ports.

        Args:
            ip_range (str): The IP range to scan (e.g., '192.168.1.0/24').
            ports (list): A list of ports to scan.

        Returns:
            dict: A dictionary containing the IP addresses and open ports.
        """
        results = {}  # Dictionary to store the results of the scan
        with ThreadPoolExecutor(self.max_threads) as executor:
            # Submit scan tasks for each IP in the specified range
            futures = {
                executor.submit(self.scan_ip, str(ip), ports): ip
                for ip in ipaddress.IPv4Network(ip_range, strict=False)
            }
            for future in futures:
                ip = futures[future]
                try:
                    result_ip, open_ports = future.result()  # Get the scan result
                    if open_ports:
                        results[result_ip] = open_ports  # Add result if port is open
                        logger.info(f"[+] Active IP found: {result_ip} with open ports: {open_ports}")
                except Exception as e:
                    logger.error(f"[-] Error scanning IP {ip}: {e}")
        return results  # Return a dictionary of results
```

---

### **Explanation of Key Methods:**

1. **Initialization (`__init__`)**:
   - This method initializes two key attributes: `timeout` (the time to wait for a connection attempt) and `max_threads` (the number of threads for concurrent scanning).
   
2. **Scanning a Single IP (`scan_ip`)**:
   - This method takes an IP address and a list of ports. It attempts to connect to each port in the list using a socket connection.
   - If the connection is successful, the method returns the IP and port. If no connection is made (due to timeout or error), it returns `None, None`.

3. **Scanning an IP Range (`scan_range`)**:
   - The `scan_range` method scans an entire range of IP addresses (specified as a CIDR block) for open ports.
   - It uses `ThreadPoolExecutor` to scan multiple IP addresses concurrently, improving the speed of the scan.
   - For each IP address in the range, it calls the `scan_ip` method to check for open ports and stores the results in a dictionary. If an open port is found, the method logs the result and adds it to the dictionary.

---

### **Example Usage:**

Here’s an example of how the `IPv4Scanner` class might be used in a script to scan an IP range for open Telnet ports (typically port 23):

```python
from src.iot_modules.ipv4_scanner import IPv4Scanner

# Initialize the IPv4 scanner
scanner = IPv4Scanner()

# Define the IP range and ports to scan
ip_range = '192.168.1.0/24'  # Example IP range
ports = [23, 2323]  # Telnet ports

# Perform the scan
scan_results = scanner.scan_range(ip_range, ports)

# Print the results
for ip, open_port in scan_results.items():
    print(f"IP {ip} has an open port {open_port}")
```

This will output a list of IP addresses with their respective open Telnet ports, if any.

---

### **Logging Service**

The `LoggingService` class is designed to centralize the logging functionality for the IoT scanner. It manages logging to both console and file outputs, handles log rotation, and allows for configurable logging levels.

#### **Class Overview:**

- **Initialization (`__init__`)**: Initializes logging settings, including log file path, log level, maximum file size for rotation, and backup count.
- **Log Handlers (`_configure_handlers`)**: Configures handlers for logging to both a rotating log file and the console.
- **Formatter (`_get_formatter`)**: Provides a standard log format for both handlers.
- **Logger Retrieval (`get_logger`)**: Returns the configured logger instance for use throughout the application.

---

#### **Class Structure:**

```python
import logging
from logging.handlers import RotatingFileHandler
import os

class LoggingService:
    """
    A centralized logging service for the IoT scanner.
    Provides logging utilities for various iot_modules and handles
    file rotation, formatting, and log level configuration.
    """

    def __init__(
        self,
        log_file="logs/scan_logs.log",
        log_level=logging.INFO,
        max_bytes=5 * 1024 * 1024,
        backup_count=3,
    ):
        """
        Initializes the logging service.

        Args:
            log_file (str): The path to the log file.
            log_level (int): The logging level.
            max_bytes (int): The maximum size of the log file in bytes.
            backup_count (int): The number of backup logs to keep.
        """
        self.log_file = log_file
        self.log_level = log_level
        self.max_bytes = max_bytes
        self.backup_count = backup_count

        # Ensure the directory for the log file exists
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

        # Create the logger instance
        self.logger = logging.getLogger("IoTScanner")
        self.logger.setLevel(self.log_level)

        # Only configure handlers if they haven't been configured already
        if not self.logger.hasHandlers():
            self._configure_handlers()

    def _configure_handlers(self):
        """
        Configure the logging handlers and formatters.
        This includes handlers for both the file and console outputs.
        """
        # File handler with rotation
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(self._get_formatter())

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(self._get_formatter())

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    @staticmethod
    def _get_formatter():
        """
        Returns a standard log formatter.

        Returns:
            A logging formatter instance.
        """
        return logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def get_logger(self):
        """
        Returns the configured logger instance.

        Returns:
            A logger instance.
        """
        return self.logger

# Initialize the logger instance
logger = LoggingService().get_logger()
```

---

### **Explanation of Key Methods:**

1. **Initialization (`__init__`)**:
   - Initializes the logging system with configurable parameters:
     - `log_file`: Path to the log file (default is `logs/scan_logs.log`).
     - `log_level`: The level of logging (default is `INFO`).
     - `max_bytes`: Maximum size for log rotation (default is 5 MB).
     - `backup_count`: Number of backup log files to retain (default is 3).
   - Ensures that the directory for the log file exists before logging begins.

2. **Configuring Handlers (`_configure_handlers`)**:
   - Sets up two logging handlers:
     - **RotatingFileHandler**: Writes logs to a file, rotating when the file exceeds `max_bytes`. It retains up to `backup_count` backup log files.
     - **StreamHandler**: Outputs logs to the console.
   - Both handlers use the same log formatter, which includes the timestamp, logger name, log level, and log message.

3. **Log Formatter (`_get_formatter`)**:
   - Provides a standard log format, ensuring consistency across all log outputs.

4. **Getting the Logger (`get_logger`)**:
   - Returns the logger instance that is configured with the specified handlers and formatter.

---

### **Example Usage:**

The `LoggingService` class is designed to be used throughout the IoT scanner for logging various events (such as errors, successes, and debug information). Here's an example of how to use the logger in your code:

```python
from src.iot_modules.logging_service import logger

# Example of logging an informational message
logger.info("This is an informational message.")

# Example of logging a warning message
logger.warning("This is a warning message.")

# Example of logging an error message
logger.error("This is an error message.")

# Example of logging a debug message (will only appear if the log level is set to DEBUG or lower)
logger.debug("This is a debug message.")
```

In this example, you would see the log messages appear both in the console and in the log file (`logs/scan_logs.log`). The log file will rotate if it exceeds the specified size limit (`5MB`), and backup logs will be created.

---

### **Log Rotation and File Management:**

The `RotatingFileHandler` ensures that log files don't grow indefinitely. When the log file reaches the specified size (`max_bytes`), it will rotate. The most recent logs will be written to a new file, and older logs will be archived as backup files. The system will keep up to `backup_count` archived log files.

- For example, with `max_bytes=5MB` and `backup_count=3`, the log file will rotate after it reaches 5MB. The last three rotated files will be kept as backups, and new log entries will continue to be written to the primary log file.

---

### **Report Generator**

The `ReportGenerator` class is designed to create a JSON-based report of the devices discovered during a network scan. The generated report includes detailed information about each device found in the network scan and is saved in a specified file.

#### **Class Overview:**

- **Initialization (`__init__`)**: Initializes the report file path where the scan results will be saved (default is `reports/scan_report.json`).
- **Generating the Report (`generate_report`)**: Takes a dictionary of devices and generates a well-structured JSON report containing the device data.

---

#### **Class Structure:**

```python
import json
from typing import Dict, Any

class ReportGenerator:
    """Class to generate a report of the devices found in the network scan"""

    def __init__(self, report_file="reports/scan_report.json"):
        self.report_file = report_file

    def generate_report(self, devices: Dict[str, Any]):
        """
        Generates a report of the devices found in the network scan.

        Args:
            devices (dict): A dictionary of devices found in the network scan.
        """
        with open(self.report_file, "w") as file:
            json.dump(devices, file, indent=4)
```

---

### **Explanation of Key Methods:**

1. **Initialization (`__init__`)**:
   - The `__init__` method takes an optional parameter `report_file`, which specifies the path where the generated report will be saved. By default, it is set to `reports/scan_report.json`.
   
2. **Generating the Report (`generate_report`)**:
   - The `generate_report` method takes a dictionary of `devices`, which is expected to contain information about the devices found during the network scan.
   - It uses Python's `json` module to write the devices' data to a JSON file with indentation for readability.

   - **Input**: A dictionary where each key is typically an identifier (like an IP address or device name), and the value contains details about the device.
   - **Output**: A JSON file saved at the specified `report_file` path.

---

### **Example Usage:**

In practice, after scanning the network and identifying devices, you can use the `ReportGenerator` class to save the scan results in a JSON format. Here's an example:

```python
from src.iot_modules.report_generator import ReportGenerator

# Sample data representing devices found in a network scan
devices_found = {
    "192.168.1.1": {"device_name": "Router", "open_ports": [22, 80, 443]},
    "192.168.1.2": {"device_name": "Smart Light", "open_ports": [8080]},
    "192.168.1.3": {"device_name": "Security Camera", "open_ports": [443, 8000]},
}

# Initialize the ReportGenerator
report_generator = ReportGenerator()

# Generate the report
report_generator.generate_report(devices_found)

print("Report generated successfully!")
```

In this example, the dictionary `devices_found` contains the devices found during a network scan. When `generate_report` is called, it creates a file `scan_report.json` with the following content:

```json
{
    "192.168.1.1": {
        "device_name": "Router",
        "open_ports": [22, 80, 443]
    },
    "192.168.1.2": {
        "device_name": "Smart Light",
        "open_ports": [8080]
    },
    "192.168.1.3": {
        "device_name": "Security Camera",
        "open_ports": [443, 8000]
    }
}
```

---

### **Handling Errors and File Overwrites:**

- If the file already exists, the `generate_report` method will overwrite the existing file. If you want to append data or handle the file differently, you could modify the method to check for the file’s existence or use different file modes (like `a` for append).
- The report is generated as a JSON file with proper indentation, making it easy to read for both humans and machines.

---
### **Shodan Client Integration**

The `ShodanClient` class interacts with the Shodan API to retrieve information about devices on the internet using their IP addresses. Shodan is a search engine for internet-connected devices, and this class allows querying Shodan for specific device details, like open ports, services, and device information.

---

#### **Class Overview:**

- **Initialization (`__init__`)**: Initializes the Shodan client using the Shodan API key, which should be set in the environment variables as `SHODAN_API_KEY`.
- **Fetching Device Information (`get_device_info`)**: Fetches information about a device based on its IP address from the Shodan database.

---

#### **Class Structure:**

```python
import os
from typing import Dict, Any
import shodan

from src.iot_modules.logging_service import logger


class ShodanClient:
    def __init__(self):
        """Initializes the Shodan client with the given API key."""
        self.client = shodan.Shodan(os.environ.get("SHODAN_API_KEY"))

    def get_device_info(self, ip_address: str) -> Dict[str, Any] | None:
        """Fetches information about a device from Shodan by its IP address.

        Args:
            ip_address (str): The IP address of the device.
        """
        try:
            logger.info(f"[+] Fetching information for IP: {ip_address}")
            device_info = self.client.host(ip_address)
            return device_info
        except shodan.APIError as e:
            logger.error(f"[-] Error fetching data for {ip_address}: {e}")
            return None
```

---

### **Explanation of Key Methods:**

1. **Initialization (`__init__`)**:
   - The constructor initializes the `ShodanClient` by fetching the Shodan API key from the environment variable `SHODAN_API_KEY`.
   - It uses the `shodan.Shodan` client to communicate with the Shodan API.
   - **Input**: The Shodan API key, fetched from the environment variable.
   - **Output**: A Shodan client object (`self.client`) that is ready to make requests.

2. **Fetching Device Information (`get_device_info`)**:
   - The `get_device_info` method fetches details about a device by its IP address from Shodan's database.
   - If successful, it returns a dictionary with the device information, which may include details like open ports, services, and metadata about the device.
   - If there is an error (e.g., the IP address does not exist in the Shodan database or the API request fails), it logs the error and returns `None`.
   
   - **Input**: The IP address of the device to look up in Shodan.
   - **Output**: A dictionary containing the device information from Shodan or `None` if an error occurred.

---

### **Example Usage:**

In practice, you might use the `ShodanClient` class to fetch additional information about a device discovered during a network scan. For example:

```python
from src.iot_modules.shodan_client import ShodanClient

# Sample IP address of a device found during a scan
device_ip = "8.8.8.8"

# Initialize the ShodanClient
shodan_client = ShodanClient()

# Fetch information about the device
device_info = shodan_client.get_device_info(device_ip)

if device_info:
    print(f"Device Info for {device_ip}:")
    print(device_info)
else:
    print(f"Could not retrieve information for {device_ip}")
```

This will return detailed information from Shodan about the device at IP `8.8.8.8`, such as its open ports, services, and any metadata available from Shodan.

---

### **Handling Errors:**

- The `get_device_info` method catches `shodan.APIError` exceptions, which are raised when the Shodan API encounters issues, such as invalid IPs, network errors, or quota limits being exceeded.
- The error is logged using the `logger` from the `LoggingService` class, ensuring that users are informed of issues without interrupting the program flow.
  
---

### **Shodan API Key:**

- To use the Shodan API, you need to set an API key in your environment. The Shodan API key can be obtained from the Shodan website after signing up.
  
  Example of setting the Shodan API key:
  ```bash
  export SHODAN_API_KEY="your_api_key_here"
  ```

---

## **Tests**

### **Overview**

This section outlines the testing framework used for the IoT scanning tool, the structure of the tests, and how to run them. The tool uses **pytest** for unit tests and test coverage is measured using **pytest-cov**. You can view the coverage report to ensure the application is well-tested.

### **Test Structure**

The tests for the IoT scanning tool are organized into separate files, each corresponding to a specific module of the project. Below is an example directory structure:

```
tests/
├── test_authenticator.py        # Tests for the Authenticator module
├── test_ipv4_scanner.py         # Tests for the IPv4Scanner module
├── test_cli_parser.py         # Tests for the CLIParser module
├── test_logging_service.py      # Tests for the LoggingService module
├── test_shodan_client.py        # Tests for the ShodanClient module
├── test_report_generator.py     # Tests for the ReportGenerator module
└── test_credential_source.py   # Tests for the CredentialManager module
└── test_handlers.py   # Tests for the Handlers module
```

### **Running Tests**

To run the tests, you can use **pytest**, which will automatically discover and run all test files that start with `test_` or end with `_test.py`. To get started:

1. Install the dependencies (if you haven’t already):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   pytest
   ```

3. Optionally, you can generate a coverage report while running the tests by adding the `--cov` flag:
   ```bash
   pytest --cov=src --cov-report=term-missing
   ```

   This command will run the tests and generate a coverage report, indicating the code coverage percentage and which lines of code are covered or missed.

### **Test Coverage**

We use **pytest-cov** to measure the code coverage during the test execution. It helps ensure that the critical components of the application are being adequately tested. The coverage report shows which lines of the code were executed and which were not.

#### **Interpreting the Coverage Report**

After running the tests with coverage, you'll see an output similar to the following:

```
---------- coverage: platform win32, python 3.12.1-final-0 -----------
Name                                   Stmts   Miss  Cover
----------------------------------------------------------
src\iot_modules\authentication.py         51      9    82%
src\iot_modules\cli_parser.py             14      0   100%
src\iot_modules\credential_source.py      15      0   100%
src\iot_modules\handlers.py               27      0   100%
src\iot_modules\ipv4_scanner.py           34      5    85%
src\iot_modules\logging_service.py        29     10    66%
src\iot_modules\report_generator.py        8      0   100%
src\iot_modules\shodan_client.py          15      0   100%
----------------------------------------------------------
TOTAL                                    193     24    88%

```

- **Stmts**: Total number of statements in the file.
- **Miss**: Number of statements that were not executed during the tests.
- **Cover**: The percentage of statements that were executed.

---

## **Conclusion**

This IoT scanner tool provides a comprehensive solution for detecting open Telnet servers, performing authentication scans, and enriching scan results using Shodan. It leverages modular components, making it easy to extend or adapt for future needs. 

The core components of the tool were developed by **Patryk**, who implemented the main functionalities, including detecting open Telnet servers, attempting authentication, scanning IP ranges, and generating reports.

The testing framework and test coverage were prepared by **Alicja**, ensuring that the tool is robust and well-tested. The tests cover the main features of the application, and the coverage report provides insights into areas that may need further attention.

With both development and testing rigorously handled, this tool is ready for deployment and can be further extended to accommodate new features or handle more specific scanning requirements.

--- 

