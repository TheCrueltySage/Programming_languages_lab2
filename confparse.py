#!/usr/bin/env python3

import sys
import json
import re
import struct
from socket import inet_aton

def getipset(filepath):
    ipreg = re.compile(r'(^(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)')
    with open(filepath,'r') as f:
        ipset = set()
        for line in f:
            temp = findmatch(ipreg,line)
            ipset = ipset|temp
        return ipset
    return None

def findmatch(regexp, cache):
    matchlist = regexp.findall(cache)
    matchset = frozenset(matchlist)
    return matchset

def ipsort(iplist):
    return sorted(iplist, key=lambda ip: struct.unpack("!L",inet_aton(ip))[0])

def ipgroup(iplist):
    ipdict = {}
    for i in iplist:
        group = i.rpartition('.')[0]
        if group not in ipdict:
            ipdict[group] = []
        ipdict[group].append(i)
    return ipdict

iplist = list(getipset("access.log"))
iplist = ipsort(iplist)
ipdict = ipgroup(iplist)
print(json.dumps(ipdict))
