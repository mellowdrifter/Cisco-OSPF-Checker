#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import sys
import ios

def login(i,c): #Log into device and get output
    try:
        tn = telnetlib.Telnet(device,23,5)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
        tn.write(b"\n")
        tn.write(b"terminal length 0\n")
        if c == 0:
            tn.write(b"show ver | include IOS\n")
        elif c == 1:
            tn.write(b"show ip ospf\n")
        elif c == 2:
            tn.write(b"show ip ospf interface\n")
        tn.write(b"exit\n")
        output=(tn.read_all().decode('ascii'))
        return output
    except:
        return None

def yes_no(q): #Ask yes or no question
    answer = input(q).lower()
    while answer not in ["y","n"]:
        print("\nInvalid response!\n")
        answer = input(q).lower()
    if "y" in answer:
        return 1
    else:
        return 0

#Get list of devices to check
devices=[]
if len(sys.argv) > 1: #If any routers passed via cli, we check those instead
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

#Check if report.txt exists. If so, ask if we want to overwrite it. Also ask if you want to write raw output at the end
report = yes_no("Would you like to write the raw cli output to raw.txt? [y/n]: ")
if report:
    raw = 1
    raw_out = ""
else:
    raw = 0
try:
    with open('report.txt') as file:
        choice = yes_no("\nreport.txt already exists. Do you want to overwrite it? [y/n]: ")
        if not choice:
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

#Log into each device, get required information, output
for device in devices:
    print("\n\nChecking ",device)
    f = open('report.txt', 'a')
    f.write("\n\n\nChecking "+device)
    for x in range(0,3):
        output=login(device,x)
        if output:
            if raw:
                raw_out+=output
        if x == 0:
            version = ios.version(output)
            print("\nRunning IOS",version[0])
            f.write("\nRunning IOS "+version[0]+"\n")
        if x == 1:
            overview = ios.overview(output)
            rid = overview['RID']
            print("Router ID:",rid)
            f.write("Router ID: "+rid+"\n")
            run = overview['RUN']
            print("OSPF running for:",run)
            f.write("OSPF running for: "+run+"\n")
            spf_last = overview['SPF']
            print("SPF last run:",spf_last)
            f.write("SPF last run: "+spf_last+"\n")
            exc = overview['EXC']
            print("SPF run",exc,"times")
            f.write("SPF run "+exc+" times")
        if x == 2:
            ospf_int = ios.ospf_interface(output)
            if len(ospf_int) == 1:
                print("\nIt has 1 OSPF enabled interface")
            else:
                print("\nIt has",len(ospf_int),"OSPF enabled interfaces")
            for o in ospf_int:
                ip,area,net,cost,status = ospf_int[o]['IP'],ospf_int[o]['Area'],ospf_int[o]['Net'],ospf_int[o]['Cost'],ospf_int[o]['Status']
                neigh,adj,hello,dead = ospf_int[o]['Neigh'],ospf_int[o]['Adj'],ospf_int[o]['Hello'],ospf_int[o]['Dead']
                print("\n\nInt:\t"+o)
                f.write("\n\nInt:\t"+o+"\n")
                print("IP:\t{}\nArea:\t{}\nType:\t{}\nCost:\t{}\nStat:\t{}".format(ip,area,net,cost,status))
                f.write("IP:\t{}\nArea:\t{}\nType:\t{}\nCost:\t{}\nStat:\t{}\n".format(ip,area,net,cost,status))
                if neigh:
                    print("Neigh:\t"+neigh)
                    f.write("Neigh:\t"+neigh+"\n")
                if adj:
                    print("Adj:\t"+adj)
                    f.write("Adj:\t"+adj+"\n")
                if hello:
                    print("Hello:\t"+hello)
                    f.write("Hello:\t"+hello+"\n")
                if dead:
                    print("Dead:\t"+dead)
                    f.write("Dead:\t"+dead+"\n")
f.close()
if raw:
    print("\n\nWriting raw output to raw.txt")
    g = open('raw.txt','w')
    g.write(raw_out)
    g.close()
