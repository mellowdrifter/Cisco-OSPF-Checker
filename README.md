##OSPF Checker
This is a simple app to list the ospf interfaces and properties on Cisco routers
Uses ospfios.py - A module that will take router output and return a dictionary
of interfaces and OSPF values

If run with no arguments, the app will attempt to find devices.txt in the local
directory. This should be a list of devices to log into. If run with arguments,
the app will log into those devices passed as arguments.

Example:<br>
`./ospf.py router1.com router2.com`<br>
This will log into router1.com and router2.com, and ignore devices.txt

If no arguments are passed and devices.txt does not exist, the app will exit


