import re
import sys

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
        if not ip:
            ip = re.search(r'Interface is unnumbered. Using address of [a-zA-Z]{1,10}[0-9]{1,5}/?[0-9]{0,5}.?[0-9]{0,5}',o)
            properties['IP'] = ip.group()
        else:
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

if __name__ == "__main__":
    f = open(sys.argv[1])
    info = f.read()
    f.close()
    ospf = ospf_information(info)
    print("This device contains "+str(len(ospf))+" ospf enabled interfaces")
    print(ospf)
