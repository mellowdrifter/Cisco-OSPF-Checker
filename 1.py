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
    f = open('report.txt', 'a')
    f.write("\nChecking "+device)
    tn.write(b"terminal length 0\n")
    tn.write(b"show ver | include IOS\n")
    tn.write(b"show inventory\n")
    tn.write(b"show ip ospf interface\n")
    tn.write(b"exit\n")
    output=(tn.read_all().decode('ascii'))
    new = re.split(r'[\n](?=GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI)',output)
    for i in new:
        interface = re.findall(r'(?:GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI)[0-9]{1,4}/?[0-9]{0,4}.?[0-9]{0,4}/?[0-9]{0,3}/?[0-9]{0,3}/?[0-9]{0,3}:?[0-9]{0,3}',i)
        ip = re.findall(r'Internet Address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',i)
        area = re.findall(r'Area ([\s]{0,3}[0-9]{1,5})',i)
        net = re.findall(r'Network Type ([\s]{0,3}[a-zA-Z_]{0,20})',i)
        cost = re.findall(r'Cost: ([0-9]{1,5})',i)
        hello = re.findall(r', Hello ([0-9]{1,3})',i)
        dead = re.findall(r', Dead ([0-9]{1,3})',i)
        if not interface:
            continue
        print("\nInterface",interface)
        f.write("\n\nInterface: "+str(interface))
        print("IP:",ip)
        f.write("\nIP: "+str(ip))
        print("Area:",area)
        f.write("\nArea: "+str(area))
        print("Type:",net)
        f.write("\nType: "+str(net))
        print("Cost",cost)
        f.write("\nCost: "+str(cost))
        if hello:
            print("Hello:",hello)
            f.write("\nHello: "+str(hello))
        if dead:
            print("Dead:",dead)
            f.write("\nDead: "+str(dead))
    f.close()
            
