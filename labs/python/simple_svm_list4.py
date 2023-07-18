"""
Simple svm list
This script performs the following:
        - List all SVMs

usage: python sample_svm_list4.py [-h] [-u USERNAME] -p PASSWORD]
The following arguments are required: -p/--password
The following arguments are optional: -u/--username (default is admin)
"""

# 1. Importing libraries
from netapp_ontap import HostConnection
from netapp_ontap import config
from netapp_ontap import NetAppRestError
from netapp_ontap import error

import argparse
from getpass import getpass

from netapp_ontap.resources import Svm

# 2A. Defining variables
CLUSTER_IP = "192.168.0.102"

# 2B. Parse variables from the command line
def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""
    parser = argparse.ArgumentParser(
        description="This script will list all SVMs."
    )
    parser.add_argument("-u", "--username", default="admin", help="Cluster Username")
    parser.add_argument("-p", "--password", help="Cluster Username Password")
    parsed_args = parser.parse_args()
    # collect the password without echo if not already provided
    if not parsed_args.password:
        parsed_args.password = getpass()
    return parsed_args

args = parse_args()
USERNAME = args.username
PASSWORD = args.password

# 3. Connect to the ONTAP cluster
conn = HostConnection(CLUSTER_IP, USERNAME, PASSWORD, verify=False)
config.CONNECTION = conn

# 4. List the SVMs using a function
def list_svms():
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

# 5. Executing the function. Also called the main code
if __name__ == "__main__":
    list_svms()