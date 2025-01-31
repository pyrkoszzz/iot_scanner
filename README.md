# IPv4 scanner for vulnerable IoT devices

The goal of the project is to develop an IPv4 address space scanner similar to ZMap and use
it to identify vulnerable IoT devices (CCTV, camera, DVR etc.) similarly to Mirai that try to
discover new devices to infect. First, Mirai scans for Telnet services on ports 23 and 2323. Once
a host running a Telnet service has been found, Mirai tries to log in using a random choice out
of a list of known default usernames and passwords. A project report describes the technique for
detecting compromised IoT devices. Shodan can provide some information on the detected IoT devices

# Project Documentation

## Overview
This project is an IoT scanner that scans specified IP ranges for open ports, attempts Telnet authentication, fetches additional information from the Shodan API, and generates a report of the scan results. The project is implemented in Python and consists of several modules, each responsible for a specific functionality.

## Modules

### CLIParser
Parses command-line arguments to configure the scanning process.

### CredentialManager
Manages credentials for Telnet authentication.

### LoggingService
Provides centralized logging utilities for various modules, including file rotation and log level configuration.

### IPScanner
Scans specified IP ranges for open ports.

### TelnetScanner
Scans for open Telnet ports and attempts authentication using provided credentials.

### ShodanClient
Fetches additional information from the Shodan API for the scanned devices.

### ReportGenerator
Generates a report of the scan results in JSON format.

## Final Functionalities
1. **Command-Line Interface (CLI) Parsing**: Parses command-line arguments to configure the scanning process.
2. **Credential Management**: Loads credentials for Telnet authentication if specified.
3. **IP Range Scanning**: Scans specified IP ranges for open ports.
4. **Telnet Open Port Scanning**: Scans for open Telnet ports on the specified IP ranges.
5. **Telnet Authentication Scanning**: Attempts to authenticate to Telnet servers using provided credentials.
6. **Shodan Enrichment**: Fetches additional information from the Shodan API for the scanned devices.
7. **Report Generation**: Generates a report of the scan results in JSON format.
8. **Logging**: Provides centralized logging for various modules, including file rotation and log level configuration.

## Intermediary Steps
1. **Initial Setup**: Set up the project structure and initialize the repository.
2. **CLI Parsing**: Implemented the `CLIParser` module to handle command-line arguments.
3. **Credential Management**: Developed the `CredentialManager` module to load and manage credentials.
4. **Logging Service**: Created the `LoggingService` module to provide centralized logging.
5. **IP Scanning**: Implemented the `IPScanner` module to scan IP ranges for open ports.
6. **Telnet Scanning**: Developed the `TelnetScanner` module to scan for open Telnet ports and attempt authentication.
7. **Shodan Integration**: Integrated the `ShodanClient` module to fetch additional information from the Shodan API.
8. **Report Generation**: Implemented the `ReportGenerator` module to generate a report of the scan results.
9. **Testing**: Wrote unit tests for each module to ensure functionality and handle edge cases.

## Libraries Used
### `telnetlib`
- **Purpose**: Used for Telnet communication.
- **Usage**: Directly reused for detecting open Telnet servers and attempting Telnet authentication.

### `concurrent.futures`
- **Purpose**: Provides a high-level interface for asynchronously executing callables.
- **Usage**: Used for parallelizing the scanning process to improve performance.

### `shodan`
- **Purpose**: Python library for interacting with the Shodan API.
- **Usage**: Used to fetch additional information about devices from the Shodan API.

### `logging`
- **Purpose**: Provides a flexible framework for emitting log messages from Python programs.
- **Usage**: Used for centralized logging across various modules.

### `json`
- **Purpose**: Provides methods for parsing JSON and converting Python objects to JSON.
- **Usage**: Used for generating the scan report in JSON format.
