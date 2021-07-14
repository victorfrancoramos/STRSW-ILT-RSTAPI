#! /usr/bin/env python3.7
from netapp_ontap import config, HostConnection
from netapp_ontap.resources import Aggregate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn = HostConnection("192.168.0.101", username = "admin", password = "Netapp1!", verify = False)
config.CONNECTION = conn
# Simple option
aggr = Aggregate()
aggr.get()
print(aggr)

# To get details
for x in Aggregate.get_collection():
 x.get()
 print(x)
 print(x.name)
 print(x, type(x))

# Other option
print(list(Aggregate.get_collection()))

