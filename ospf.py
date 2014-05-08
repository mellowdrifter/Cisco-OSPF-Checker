#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import re
import sys
import collections

def login(i): #Log into device and get output
        try:
            tn = telnetlib.Telnet(device,23,5)
            tn.read_until(b"Username: ")
            tn.write(user.encode('ascii') + b"\n")
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
            tn.write(b"\n")
            tn.write(b"terminal length 0\n")
            tn.write(b"show ver | include IOS\n")
            tn.write(b"show ip ospf interface\n")
            tn.write(b"exit\n")
            output=(tn.read_all().decode('ascii'))
            return output
        except:
            return None

def ospf_information(i):
    int_list = {}
    ospf = re.split(r'[\n](?=GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI|Vlan|Virtual-Access)',i)
    for o in ospf:
        properties = {}
        interface =  re.search(r'(GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI|Vlan|Virtual-Access)[0-9]{1,4}/?[0-9]{0,4}.?[0-9]{0,4}/?[0-9]{0,3}/?[0-9]{0,3}/?[0-9]{0,3}:?[0-9]{0,3}',o)
        if not interface:
            continue
        interface = interface.group()
        ip = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})',o)
        properties['IP'] = ip.group()
        if not ip:
            ip = re.search(r'Interface is unnumbered. Using address of [a-zA-Z]{1,10}[0-9]{1,5}/?[0-9]{0,5}.?[0-9]{0,5}',o)
            properties['IP'] = ip.group()
        a = re.search(r'Area ([\s]{0,3}[0-9]{1,5})',o)
        properties['Area'] = a.group(1)
        n = re.search(r'Network Type ([\s]{0,3}[a-zA-Z_]{0,20})',o)
        properties['Net'] = n.group(1)
        c = re.search(r'Cost: ([0-9]{1,5})',o)
        properties['Cost'] = c.group(1)
        s = re.search(r'line protocol is[\s]([a-zA-Z]{1,4})',o)
        properties['Status'] = s.group(1)
        p = re.search(r'Passive',o)
        if p:
            properties['Neigh'] = "Passive Interface"
            properties['Adj'] = None
        else:
            ne = re.search(r'(?:Neighbor Count is )([0-9]{1,3})',o)
            if not ne:
                properties['Neigh'] = None
            else:
                properties['Neigh'] = ne.group(1)
            ad = re.search(r'(?:Adjacent neighbor count is )([0-9]{1,3})',o)
            if not ad:
                properties['Adj'] = None
            else:
                properties['Adj'] = ad.group(1)
        h = re.search(r'Hello ([0-9]{1,3})',o)
        if not h:
            properties['Hello'] = None
        else:
            properties['Hello'] = h.group(1)
        d = re.search(r'Dead ([0-9]{1,3})',o)
        if not d:
            properties['Dead'] = None
        else:
            properties['Dead'] = d.group(1)
        int_list[interface]=properties
    return int_list
        


#Get list of devices to check
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

#Check if report.txt exists. If so, ask if we want to overwrite it. Also ask if you want to write raw output at the end
r = ""
while r not in ["y","n"]:
    r = input("\n\n\nWould you like to write the raw cli output to raw.txt? [y/n]: ")
    if r.lower() == "y":
        raw = 1
        raw_out=""
    else:
        raw = 0

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

#Log into each device, get required information, output
for device in devices:
    print("\n\nChecking ",device)
    f = open('report.txt', 'a')
    f.write("\n\n\nChecking "+device)
    output=login(device)
    if output:
        if raw:
            raw_out+=output
    ospf_int = ospf_information(output)
    print("\n"+device,"has",len(ospf_int),"ospf enabled interfaces!")
    for o in ospf_int:
        ip,area,net,cost,status = ospf_int[o]['IP'],ospf_int[o]['Area'],ospf_int[o]['Net'],ospf_int[o]['Cost'],ospf_int[o]['Status']
        neigh,adj,hello,dead = ospf_int[o]['Neigh'],ospf_int[o]['Adj'],ospf_int[o]['Hello'],ospf_int[o]['Dead']
        print("\n\nInt:\t"+o)
        print("IP:\t{}\nArea:\t{}\nType:\t{}\nCost:\t{}\nStat:\t{}".format(ip,area,net,cost,status))
        if neigh:
            print("Neigh:\t"+neigh)
        if adj:
            print("Adj:\t"+adj)
        if hello:
            print("Hello:\t"+hello)
        if dead:
            print("Dead:\t"+dead)


f.close()            

if raw:
    print("\n\nWriting raw output to raw.txt")
    g = open('raw.txt','w')
    g.write(raw_out)
    g.close()

