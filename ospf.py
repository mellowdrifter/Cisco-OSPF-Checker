#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import re
import sys



def interface(i):
    ospf_int = re.findall(r'(?:GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI)[0-9]{1,4}/?[0-9]{0,4}.?[0-9]{0,4}/?[0-9]{0,3}/?[0-9]{0,3}/?[0-9]{0,3}:?[0-9]{0,3}',i)
    if ospf_int:
        return ospf_int
    if not ospf_int:
        return None

def getip(i):
    ip = re.findall(r'Internet Address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',i)
    if not ip:
        ip = re.findall(r'Interface is unnumbered. Using address of [a-zA-Z]{1,10}[0-9]{1,5}/?[0-9]{0,5}.?[0-9]{0,5}',i)
    return ip

def getarea(i):
    area = re.findall(r'Area ([\s]{0,3}[0-9]{1,5})',i)
    return area

def gettype(i):
    net = re.findall(r'Network Type ([\s]{0,3}[a-zA-Z_]{0,20})',i)
    return net

def getcost(i):
    cost = re.findall(r'Cost: ([0-9]{1,5})',i)
    return cost

def gethello(i):
    hello = re.findall(r', Hello ([0-9]{1,3})',i)
    return hello

def getdead(i):
    dead = re.findall(r', Dead ([0-9]{1,3})',i)
    return dead


#Get out list of devices to check
devices=[]

if len(sys.argv) > 1:       #If any routers passed via cli, we check those instead
    for i in sys.argv[1:]:
        devices.append(i)
else:
    try:
        with open('devices.txt') as file:
            pass
    except IOError as e:
        print("\ndevices.txt does not exist or unreadable, exiting now")
        exit()

    f = open('devices.txt')
    for line in f:
        if line.isspace(): #Ignore any blank lines
            continue
        devices.append(line.strip())

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
    try:
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
        print("\n\nChecking ",device)
        f = open('report.txt', 'a')
        f.write("\n\nChecking "+device)
        tn.write(b"terminal length 0\n")
        tn.write(b"show ver | include IOS\n")
        tn.write(b"show inventory\n")
        tn.write(b"show ip ospf interface\n")
        tn.write(b"exit\n")
        output=(tn.read_all().decode('ascii'))
        ospf = re.split(r'[\n](?=GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI)',output)
        for i in ospf:
            intf = interface(i)
            if not intf:
                continue
            ip = getip(i)
            area = getarea(i)
            net = gettype(i)
            cost = getcost(i)
            hello = gethello(i)
            dead = getdead(i)
            print("\nInt:\t"+intf[0])
            f.write("\n\nInt:\t"+intf[0])
            print("IP:\t"+ip[0])
            f.write("\nIP:\t"+ip[0])
            print("Area:\t"+area[0])
            f.write("\nArea:\t"+area[0])
            print("Type:\t"+net[0])
            f.write("\nType:\t"+net[0])
            print("Cost\t"+cost[0])
            f.write("\nCost:\t"+cost[0])
            if hello:
                print("Hello:\t"+hello[0])
                f.write("\nHello:\t"+hello[0])
            if dead:
                print("Dead:\t"+dead[0])
                f.write("\nDead:\t"+dead[0])
    except:
        print("\n!*Unable to resolve or log into",device,"*!")
    f.close()            
