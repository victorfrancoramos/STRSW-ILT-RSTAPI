# Simple Volume list

# 1. Importing libraries
from netapp_ontap import HostConnection
from netapp_ontap import config
from netapp_ontap import NetAppRestError
from netapp_ontap import error

from netapp_ontap.resources import Volume

# 2. Defining variables
USERNAME = "admin"
PASSWORD = "Netapp1!"
CLUSTER_IP = "192.168.0.102"

# 3. Connect to the ONTAP cluster
conn = HostConnection(CLUSTER_IP, USERNAME, PASSWORD, verify=False)
config.CONNECTION = conn

# 4. List the SVMs
try:
    volume = Volume.get_collection()
    #print(list(svm))
    for i in volume:
        print(f"Volume name {i.name}")
        print(f"volume uuid {i.uuid}")
#        print(f"volume size {i.size}")
except NetAppRestError:
    print("Error:- " % error.http_err_response.http_response.text)
    print("Exception caught :" + str(error))