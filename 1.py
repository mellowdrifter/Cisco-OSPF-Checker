#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import sys

#Check for devices.txt and read into string
devices=[]
try:
    with open('devices.txt') as file:
        pass
except IOError as e:
    print("\ndevices.txt does not exist or unreadable, exiting now")
    sys.exit()

f = open('devices.txt')
for line in f:
    devices.append(line.rstrip())
    
try:
    with open('report.txt') as file:
        choice = input("\nreport.txt already exists, do you want to overwrite it? [Yes/No] (Yes is default): ")
        lchoice = choice.lower()
        if lchoice[0] == "n":
            print("\nExiting now")
            sys.exit()
        else:
            print("\nreport.txt will be overwritten!")
            f = open('report.txt', 'w')
            f.close
except IOError as e:
    pass


#Get username and password
user = input("\n\nEnter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
enablepass = getpass.getpass(prompt="Enter your enable password: ")

#Log into host
for i in devices:
    tn = telnetlib.Telnet(i,23,5)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"\n")
    en = (tn.read_some().decode('ascii'))
    if ">" in en:
        tn.write(b"enable\n")
        tn.write(enablepass.encode('ascii') + b"\n")
    print("Checking ",i)
    tn.write(b"terminal length 0\n")  
    tn.write(b"show ver | include IOS\n")
    tn.write(b"show inventory\n")
    tn.write(b"dir\n")
    tn.write(b"exit\n")
    output=(tn.read_all().decode('ascii'))
    f = open('report.txt', 'a')
    f.write(output.rstrip())
    print(output.rstrip())
    f.close
