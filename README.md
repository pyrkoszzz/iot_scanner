# IPv4 scanner for vulnerable IoT devices

The goal of the project is to develop an IPv4 address space scanner similar to ZMap and use
it to identify vulnerable IoT devices (CCTV, camera, DVR etc.) similarly to Mirai that try to
discover new devices to infect. First, Mirai scans for Telnet services on ports 23 and 2323. Once
a host running a Telnet service has been found, Mirai tries to log in using a random choice out
of a list of known default usernames and passwords. A project report describes the technique for
detecting compromised IoT devices. Shodan can provide some information on the detected IoT devices

