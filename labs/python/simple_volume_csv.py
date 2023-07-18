# Simple Volume list to CSV
# Save results to csv file with Python - https://stackoverflow.com/questions/3345336/save-results-to-csv-file-with-python

# 1. Importing libraries
from netapp_ontap import HostConnection
from netapp_ontap import config
from netapp_ontap import NetAppRestError
from netapp_ontap import error

from netapp_ontap.resources import Volume

import numpy

# 2. Defining variables
USERNAME = "admin"
PASSWORD = "Netapp1!"
CLUSTER_IP = "192.168.0.102"

# 3. Connect to the ONTAP cluster
conn = HostConnection(CLUSTER_IP, USERNAME, PASSWORD, verify=False)
config.CONNECTION = conn

# 4. List the Volumes
try:
    # create empty lists with volume names and uuids
    volume_names = []
    volume_uuids = []
    volume = Volume.get_collection()
    for i in volume:
        print(f"Volume name: {i.name}")
        volume_names.append(i.name)
        print(f"Volume uuid: {i.uuid}")
        volume_uuids.append(i.uuid)
    print(f"List of volume names {volume_names}")
    print(f"List of volume uuids {volume_uuids}")
    numpy.savetxt('volumes.csv', [p for p in zip(volume_names, volume_uuids)], delimiter=',', fmt='%s')
except NetAppRestError:
    print("Error:- " % error.http_err_response.http_response.text)
    print("Exception caught :" + str(error))