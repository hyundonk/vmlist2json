#!/usr/bin/python

import sys
import pandas as pd
from itertools import groupby 
from collections import OrderedDict
from ast import literal_eval

import json    

if len(sys.argv) != 2 :
  print("usage: ", sys.argv[0], "[csv_filename]")
  exit(0)

filename = sys.argv[1]

df = pd.read_csv(filename, dtype={
        "servicename" : str,
        "vm_size" : str,
        "subnet" : str,
        "subnet_ip_offset" : str,
        "vm_offer" : str,
        "os_disk_size" : str,
        "dns_servers" : str,
        "name" : str,
        "ipaddress" : str,
        "image_id" : str,
        "zone" : str
    })

results = []
finalList = []
finalDict = {}

grouped = df.groupby(['servicename'])

for key, value in grouped:
  dictionary = {}
  j = grouped.get_group(key).reset_index(drop = True)
  dictionary['servicename']       = j.at[0, 'servicename']
  dictionary['vm_size']           = j.at[0, 'vm_size']
  dictionary['subnet']            = j.at[0, 'subnet']
  dictionary['subnet_ip_offset']  = j.at[0, 'subnet_ip_offset']
  dictionary['os_disk_size']      = j.at[0, 'os_disk_size']
  dictionary['dns_servers']       = literal_eval(j.at[0, 'dns_servers'])
  dictionary['vm_offer']          = j.at[0, 'vm_offer']

  dictList = []
  for i in j.index:
    anotherDict = {}
    anotherDict['name']       = j.at[i, 'name']
    anotherDict['ipaddress']  = j.at[i, 'ipaddress']
    anotherDict['image_id']   = j.at[i, 'image_id']
    anotherDict['zone']   = j.at[i, 'zone']
    dictList.append(anotherDict)

  print(dictList)  
  dictionary['vm'] = dictList
  finalList.append(dictionary)

#json.dumps(finalList)
#print(json.dumps(finalList))

with open("./output.json", 'w') as outfile:
  json.dump(finalList, outfile, indent=4)
