##OSPF Checker

This is a simple app to list the ospf interfaces and properties on Cisco IOS
routers. Uses ios.py - A module that will take router output and return a 
dictionary of OSPF overview and interface data.

###Running
If run with no arguments, the app will attempt to find _devices.txt_ in the local
directory. This should be a list of devices to log into. If run with arguments,
the app will log into those devices passed as arguments.

Example:<br>
`./ospf.py router1.com router2.com`<br>
This will log into router1.com and router2.com, and ignore _devices.txt_

If no arguments are passed and devices.txt does not exist, the app will exit

###Reports
Once run, the app will ask you if you would like to output the raw router output
to a file named raw.txt - The app will also output cleaned up output into report.txt






