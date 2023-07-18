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

# 4. List the SVMs
try:
    # create empty lists with Table Headers for volume names and uuids
    volume_names = ["VOLUME NAME"]
    volume_uuids = ["VOLUME UUID"]
    volume_size = ["VOLUME SIZE(GB)"]
    volume = Volume.get_collection()
    for i in volume:
        #print(f"Volume name {i.name}")
        volume_names.append(i.name)
        #print(f"volume uuid {i.uuid}")
        volume_uuids.append(i.uuid)
        # Get additional details for the volume
        volume_details = Volume.find(name=i.name)
        # Test print just to get the available fields
        #print(volume_details)
        volume_size_in_gb = volume_details.size / (1024 * 1024 * 1024)
        #print(f"Volume size: {volume_size_in_gb} GB")
        volume_size.append(volume_size_in_gb)
    print(f"List of volume names {volume_names}")
    print(f"List of volume uuids {volume_uuids}")
    print(f"List of volume sizes in GB {volume_size}")
    numpy.savetxt('volumes2.csv', [p for p in zip(volume_names, volume_uuids, volume_size)], delimiter=',', fmt='%s')
except NetAppRestError:
    print("Error:- " % error.http_err_response.http_response.text)
    print("Exception caught :" + str(error))