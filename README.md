# PythonToPLC
Author: 
Hayden Isaac

About:
Using a Python with snap7 to communicate between the PLC and the MiR's API.
The PLC will send a mission to python, which will parse it and send the corresponding mission to the fleet with any additional options requested such as a specific robot to complete the task.
The python is also updating the PLC with the status of each mission and robot every few seconds.
Used in end of line processes where the robot moves the wrapped product to the storage area. This will reduce spillage caused by product falling off a forklift and the need for forklift drivers.

Usage:
- Ensure the correct packages and files are downloaded and installed.
- Turn on panel and fleet inside the panel
- Turn on robot/s
- Plug ethernet into the laptop and change to a valid static ip
- Locate the files and run main.py

