#import needed modules
import telnetlib
import getpass

#use a tuple to set list of devices to log into
devices=("vr1.wok1.hso.uk.com","cr1.263992.hso.uk.com")

#get username and password
user=input("Enter your username: ")
password=getpass.getpass(prompt="Enter your password: ")

#Log into host
for i in devices:
	tn = telnetlib.Telnet(i)
	tn.read_until(b"Username: ")
	tn.write(user.encode('ascii') + b"\n")
	tn.read_until(b"Password: ")
	tn.write(password.encode('ascii') + b"\n")
	tn.write(b"show ip ospf int brief\n")
	tn.write(b"exit\n")
	print(tn.read_all().decode('ascii'))

