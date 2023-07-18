# Simple svm list

# 1. Importing libraries
from netapp_ontap import HostConnection
from netapp_ontap import config
from netapp_ontap import NetAppRestError
from netapp_ontap import error

from netapp_ontap.resources import Svm

# 2. Defining variables
USERNAME = "admin"
PASSWORD = "Netapp1!"
CLUSTER_IP = "192.168.0.102"

# 3. Connect to the ONTAP cluster
conn = HostConnection(CLUSTER_IP, USERNAME, PASSWORD, verify=False)
config.CONNECTION = conn

# 4. List the SVMs using a function
def list_svms():2
    '''Function that lists the SVMs in an ONTAP Cluster'''
    try:
        svm = Svm.get_collection()
        #print(list(svm))
        for i in svm:
            print(f"SVM name {i.name}")
            print(f"SVM uuid {i.uuid}")
    except NetAppRestError:
        print("Error:- " % error.http_err_response.http_response.text)
        print("Exception caught :" + str(error))
    return

# 5. Executing the function
list_svms()