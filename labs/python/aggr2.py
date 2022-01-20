#! /usr/bin/env python3.7
from netapp_ontap import config
from netapp_ontap import HostConnection
from netapp_ontap.resources import Aggregate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn1 = HostConnection("192.168.0.101", username = "admin", password = "Netapp1!", verify = False)
conn2 = HostConnection("192.168.0.102", username = "admin", password = "Netapp1!", verify = False)

'''
config.CONNECTION = conn1
aggr = Aggregate()
aggr.get()
print("Aggregates for cluster1:")
print(aggr)

config.CONNECTION = conn2
aggr = Aggregate()
aggr.get()
print("Aggregates for cluster2:")
print(aggr)
'''

config.CONNECTION = conn1
print("Aggregates for cluster1:")
print(list(Aggregate.get_collection()))

config.CONNECTION = conn2
print("Aggregates for cluster2:")
print(list(Aggregate.get_collection()))

# Get details
config.CONNECTION = conn2
print("To get details:")
for x in Aggregate.get_collection():
 x.get()
 print("Collection elements:")
 print(x)
 print("Aggregate name:")
 print(x.name)
 print("Aggregate uuid:")
 print(x.uuid)
