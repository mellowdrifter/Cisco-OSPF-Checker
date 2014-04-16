This is a simple app to list the ospf interfaces and properties on Cisco routers

-Currently outputs to a file called reports.txt in the same location. App will ask you what to do is reports.txt already exists

v0.05
=====
-You can now pass a router name as an argument
-If there is not argument, then device.txt is looked at

v0.04
=====
-Now captures OSPF items in list
-Prints and saves output to report.txt


v0.03
=====
-App can now read list of devices from file
-Exits app if devices.txt cannot be found
-write output to a text file

v0.02
=====
-Devices are now listed inside a tuple. Previously only one router at a time could be run


TO-DO
=====
-Make far better output
-Include SSH support

