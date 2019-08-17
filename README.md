# ScoutingServer
Server for scouting app for the FIRST Robotics Competition.

Runs with Python3 on Linux, uses Bluetooth for data transfer.

Developed by FRC Team 449: The Blair Robot Project.

### Usage

To run this server, run server.py with Python3 on a Linux computer with Bluetooth enabled, and follow the printed instructions.

Devices must be paired (but not necessarily connected) before use.

For automatic removable drive detection and copying, you must enable NOPASSWD for sudo usage. You can do this by adding `username ALL=(ALL) NOPASSWD: ALL` to the end of your `/etc/sudoers` file (do this with `sudo visudo`). Be aware that this poses a major security risk, your password is no longer required to use sudo. 
You also need an empty media directory to mount to.

### Related Repositories/Documents

Scouting App: https://github.com/carter-wilson/ScoutingAppBase

Document with instructions for troubleshooting: https://docs.google.com/document/d/e/2PACX-1vQee5Sqv6SeAFb2fKwDNr9rSXkZXnjioS3S4TC8sNpsfiSedAvtZzxlJ8ffhN09tpQuTQDwXQFh2eT-/pub


### Copyright and License
Copyright (C) 2019 FRC Team 449: The Blair Robot Project

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
