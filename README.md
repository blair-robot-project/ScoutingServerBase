# ScoutingServer
FRC Team 449 The Blair Robot Project: Server for scouting app (Python and Bluetooth)

Sever for scouting app for the FIRST Robotics Competition.

Developed by FRC Team 449: The Blair Robot Project.

### Usage

To run this server, run server.py with Python3 on a Linux computer with Bluetooth enabled, and follow the printed instructions.

Make sure to change the MAC address in socketctl to be the MAC address of your Bluetooth adapter. Also, devices must be paired (but not necessarily connected) before use.

For automatic removable drive detection and copying, you must enable NOPASSWD for sudo usage. You can do this by adding "username ALL=(ALL) NOPASSWD: ALL" to the end of your /etc/sudoers file. Be aware that this poses a major security risk, your password is no longer required to use sudo.  

### Related Repositories/Documents

Scouting App: https://github.com/carter-wilson/DeepSpaceScoutingApp

Strategy app to retrieve data from bluetooth server: https://github.com/carter-wilson/StrategyApp

Document explaining the fields for data analysis: https://docs.google.com/document/d/e/2PACX-1vSp7j7vCPgH-OLdPKhMAEnKDSYsi99BufqXZlAtQ5-3uarYPo0ePbIv9WJOP2oC02fvnjt30iEE5z3C/pub
