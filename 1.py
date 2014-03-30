#import needed modules
import telnetlib
import getpass

#get hostname, username, and password
host=input("Please enter a host name: ")
user=input("Enter your username: ")
password=getpass.getpass(prompt="Enter your password: ")

#Log into host
tn = telnetlib.Telnet(host)
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")

#get required information, then exit from host
tn.write(b"show ip ospf int brief\n")
tn.write(b"show run | sec router ospf\n")
tn.write(b"exit\n")

#display collected information
print(tn.read_all().decode('ascii'))
