#!/usr/bin/python3

'''Simple script to telnet into a number of devices
and check certain OSPF properties'''

import telnetlib
import getpass
import re
import sys


def ospf_information(i):
    ospf_int = re.search(r'(GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI|Vlan|Virtual-Access)[0-9]{1,4}/?[0-9]{0,4}.?[0-9]{0,4}/?[0-9]{0,3}/?[0-9]{0,3}/?[0-9]{0,3}:?[0-9]{0,3}',i)
    if not ospf_int:
        return None
    ospf_int = ospf_int.group()
    ip = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2})',i)
    ip = ip.group()
    if not ip:
        ip = re.search(r'Interface is unnumbered. Using address of [a-zA-Z]{1,10}[0-9]{1,5}/?[0-9]{0,5}.?[0-9]{0,5}',i)
        ip = ip.group()
    a = re.search(r'Area ([\s]{0,3}[0-9]{1,5})',i)
    area = a.group(1)
    n = re.search(r'Network Type ([\s]{0,3}[a-zA-Z_]{0,20})',i)
    net = n.group(1)
    c = re.search(r'Cost: ([0-9]{1,5})',i)
    cost = c.group(1)
    ne = re.search(r'(?:Neighbor Count is )([0-9]{1,3})',i)
    if not ne:
        p = re.search(r'Passive',i)
        if not p:
            neighbour = "N/A"
        else:
            neighbour = p.group()
    else:
        neighbour = ne.group(1)
    ad = re.search(r'(?:Adjacent neighbor count is )([0-9]{1,3})',i)
    if not ad:
        adjacency = "N/A"
    else:
        adjacency = ad.group(1)
    h = re.search(r'Hello ([0-9]{1,3})',i)
    if not h:
        hello = "N/A"
    else:
        hello = h.group(1)
    d = re.search(r'Dead ([0-9]{1,3})',i)
    if not d:
        dead = "N/A"
    else:
        dead = d.group(1)
    return (ospf_int,ip,area,net,cost,neighbour,adjacency,hello,dead)

def login(i):
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

#Log into host, run commands, echo output, write output to file
for device in devices:
    print("\n\nChecking ",device)
    f = open('report.txt', 'a')
    f.write("\n\n\nChecking "+device)
    output=login(device)
    if output:
        if raw:
            raw_out+=output
        ospf = re.split(r'[\n](?=GigabitEthernet|FastEthernet|Serial|Tunnel|Loopback|Dialer|BVI|Vlan|Virtual-Access)',output)
        for o in ospf:
            data = ospf_information(o)
            if not data:
                continue
            print("\nInt:\t{}\nIP:\t{}\nArea:\t{}\nType:\t{}\nCost:\t{}".format(data[0],data[1],data[2],data[3],data[4]))
            if "N/A" not in data[5]:
                print("Neigh:\t{}".format(data[5]))
            if "N/A" not in data[6]:
                print("Adj:\t{}".format(data[6]))
            if "N/A" not in data[7]:
                print("Hello:\t{}".format(data[7]))
            if "N/A" not in data[8]:
                print("Dead:\t{}".format(data[8]))
    else:
        print("\n!*Unable to resolve or log into",device,"*!")

f.close()            

if raw:
    print("\n\nWriting raw output to raw.txt")
    g = open('raw.txt','w')
    g.write(raw_out)
    g.close()

