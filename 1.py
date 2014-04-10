#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import re

#Check for devices.txt and read into string
devices=[]
try:
    with open('devices.txt') as file:
        pass
except IOError as e:
    print("\ndevices.txt does not exist or unreadable, exiting now")
    exit()

f = open('devices.txt')
for line in f:
    devices.append(line.rstrip())
    
#Check if report.txt exists. If so, ask if we want to overwrite it    
try:
    with open('report.txt') as file:
        choice = input("\nreport.txt already exists. Do you want to overwrite it? [y/n]: ")
        while choice not in ["y","n"]:
            choice = input("Invalid choice! Do you want to overwrite report.txt? [y/n]: ")
        if choice == "n":
            print("\nExiting now")
            exit()
        else:
            print("\nreport.txt will be overwritten!")
            f = open('report.txt', 'w')
            f.close()
except IOError as e:
    pass


#Get username and password
user = input("\n\nEnter your username: ")
password = getpass.getpass(prompt="Enter your password: ")
enablepass = getpass.getpass(prompt="Enter your enable password: ")

#Log into host, run commands, echo output, write output to file
for device in devices:
    tn = telnetlib.Telnet(device,23,5)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"\n")
    en = (tn.read_some().decode('ascii'))
    if ">" in en:
        tn.write(b"enable\n")
        tn.write(enablepass.encode('ascii') + b"\n")
    print("Checking ",device)
    tn.write(b"terminal length 0\n")
    tn.write(b"show ver | include IOS\n")
    tn.write(b"show inventory\n")
    tn.write(b"show ip ospf interface\n")
    tn.write(b"exit\n")
    output=(tn.read_all().decode('ascii'))
    i = re.findall('(?:GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI)[0-9]{1,4}/?[0-9]{0,4}.?[0-9]{0,4}/?[0-9]{0,3}/?[0-9]{0,3}/?[0-9]{0,3}:?[0-9]{0,3}',output)
    ip = re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',output)
    A = re.findall(r'Area[\s]{0,3}[0-9]{1,5}',output)
    n = re.findall(r'Network Type[\s]{0,3}[a-zA-Z_]{0,20}',output)
    C = re.findall(r'Cost:[\s]{0,3}[0-9]{1,5}',output)
    h = re.findall(r'Hello[\s][0-9]{1,3}',output)
    D = re.findall(r'Dead[\s][0-9]{1,3}',output)
    for a,b,c,d,e,f,g in zip(i,ip,A,n,C,h,D):
        print("\n"+a)
        print(b)
        print(c)
        print(d)
        print(e)
        print(f)
        print(g)
