#! /usr/bin/env python3.7
from netapp_ontap import config, HostConnection
from netapp_ontap.resources import Svm
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
conn = HostConnection("192.168.0.102", username = "admin", password = "Netapp1!", verify = False)
config.CONNECTION = conn
# Simple option
svm = Svm()
svm.get()
print("Simple option:")
print(svm)

# Other option
print("Other option:")
print(list(Aggregate.get_collection()))

# To get details
print("To get details:")
for x in Aggregate.get_collection():
 x.get()
 print(x)
 print("Aggregate name:")
 print(x.name)
 print("Aggregate uuid:")
 print(x.uuid)
 print("Aggregate type:")
 print(x, type(x))

