# Kawasaki experimental

## Contents

.as file containing kawasaki AS code
Python files to start the client

## Compatibility

Tested with simulated:
D controller (minor API changes)
D+ controller (minor API changes)
E controller

## How-to

Download K-roset from the kawasaki FTP-server
http://ftp.kawasakirobot.de/files/public/Software/K-Roset/

In K-roset:
- Start a new project
- Open easy builder
- add an E-controller robot

Make sure firewall is not blocking K-roset

Now run `telnet_admin.py` 

## To-do

| to Do                         |
|-------------------------------|
| `Implement state-machine`     |
| `Implement message protocol`  |
| `Error handling`              |