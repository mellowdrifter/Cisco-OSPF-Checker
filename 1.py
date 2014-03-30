import telnetlib
import getpass

host=input("Please enter a host name: ")
user=input("Enter your username: ")
password=getpass.getpass(prompt="Enter your password: ")

tn = telnetlib.Telnet(host)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")


tn.write(b"show ip ospf int brief\n")
tn.write(b"show run | sec router ospf\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
