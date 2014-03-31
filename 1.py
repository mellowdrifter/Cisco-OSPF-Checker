#!/usr/bin/python3

'''Simple script to log into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import os

devices=("cr1.263992.hso.uk.com","cr1.303953.hso.uk.com")

#get username and password
user=input("Enter your username: ")
password=getpass.getpass(prompt="Enter your password: ")
enablepass=getpass.getpass(prompt="Enter your enable password: ")

#Log into host
for i in devices:
    tn = telnetlib.Telnet(i,23,5)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"\n")
    en=(tn.read_some().decode('ascii'))
    if ">" in en:
        tn.write(b"enable\n")
        tn.write(enablepass.encode('ascii') + b"\n")
    tn.write(b"terminal length 0\n")  
    tn.write(b"show ver | include IOS\n")
    tn.write(b"show ip ospf int brief\n")
    tn.write(b"sh ip ospf neighbor\n")
    tn.write(b"exit\n")
    output=(tn.read_all().decode('ascii'))
    f=open('report.txt', 'w')
    f.write(output)
    f.close
