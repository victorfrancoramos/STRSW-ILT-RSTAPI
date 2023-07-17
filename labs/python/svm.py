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
print(list(Svm.get_collection()))

# To get details
print("To get details:")
for x in Svm.get_collection():
 x.get()
 print(x)
 print("Svm name:")
 print(x.name)
 print("Svm uuid:")
 print(x.uuid)
 print("Svm type:")
 print(x, type(x))

