#! /usr/local/bin/env python3
"""
ONTAP 9.10 REST API Python Client Library Scripts: This script performs the following:
        - Create a qtree (or quota tree)
        - Create a quota policy rule
        - Create a QoS (Quality of Service) policy on an existing SVM
usage: python3 qtree.py [-h] -c cluster -v VOLUME_NAME -vs VSERVER_NAME -q QTREE_NAME
       -qos QOS_POLICY_NAME -sh SPACE_HARD -fh FILE_HARD -un USER_NAME [-u API_USER] [-p API_PASS]
"""

import argparse
from getpass import getpass
import logging

from netapp_ontap import config, HostConnection, NetAppRestError
from netapp_ontap.resources import Qtree, QuotaRule, QosPolicy

def parse_args() -> argparse.Namespace:
    """Parse the command line arguments from the user"""

    parser = argparse.ArgumentParser(
        description="This script will create a new qtree."
    )
    parser.add_argument(
        "-c", "--cluster", required=True, help="API server IP:port details"
    )
    parser.add_argument(
        "-v", "--volume_name", required=True, help="Volume name to create qtree from"
    )
    parser.add_argument(
        "-vs", "--vserver_name", required=True, help="SVM to create the volume from"
    )
    parser.add_argument(
        "-q", "--qtree_name", required=True, help="QTree to create the qutoa tree"
    )
    parser.add_argument(
        "-qos", "--qos_policy_name", required=True, help="QoS Policy to create on the SVM"
    )
    parser.add_argument(
        "-sh", "--space_hard", required=True, help="Hard limit on space in bytese"
    )
    parser.add_argument(
        "-fh", "--file_hard", required=True, help="hard limit on files in bytes"
    )
    parser.add_argument(
        "-un", "--user_name", required=True, help="User name who can access the qtree"
    )
    parser.add_argument("-u", "--api_user", default="admin", help="API Username")
    parser.add_argument("-p", "--api_pass", help="API Password")
    parsed_args = parser.parse_args()

    # collect the password without echo if not already provided
    if not parsed_args.api_pass:
        parsed_args.api_pass = getpass()

    return parsed_args

def create_qtree(volume_name: str, vserver_name: str, qtree_name: str) -> None:
    data = {
        'name': qtree_name,
        'volume': {'name': volume_name},
        'svm': {'name': vserver_name},
        'security_style': 'unix',
        'unix_permissions': 744,
        'export_policy_name': 'default',
        'qos_policy': {'max_throughput_ops': 1000}
    }
    qtree = Qtree(**data)
    try:
        qtree.post()
        print("Qtree %s created successfully" % qtree.name)
    except NetAppRestError as err:
        print("Error: QTree was not created: %s" % err)
    return

def create_policy_rule(volume_name: str, vserver_name: str, qtree_name: str, user_name: str,
space_hard: int, file_hard: int) -> None:
'''
    resource.svm = {"name": "svm1"}
    resource.volume = {"name": "vol1"}
    resource.type = "user"
    resource.users = [{"name": "jsmith"}]
    resource.qtree = {"name": "qt1"}
    resource.user_mapping = "on"
    resource.space = {"hard_limit": 8192, "soft_limit": 1024}
    resource.files = {"hard_limit": 20, "soft_limit": 10}

Required properties:
    svm.uuid or svm.name - Existing SVM in which to create the qtree.
    volume.uuid or volume.name - Existing volume in which to create the qtree.
    type - Quota type for the rule. This type can be user, group, or tree.
    users.name or user.id - If the quota type is user, this property takes the user name or user ID. For default user quota rules, the user name must be specified as "".
    group.name or group.id - If the quota type is group, this property takes the group name or group ID.
     For default group quota rules, the group name must be specified as "".
    qtree.name - Qtree for which to create the rule. For default tree rules, the qtree name must be specified as "".
Recommended optional properties:
    space.hard_limit - Specifies the space hard limit, in bytes. If less than 1024 bytes, the value is rounded up to 1024 bytes.
    space.soft_limit - Specifies the space soft limit, in bytes. If less than 1024 bytes, the value is rounded up to 1024 bytes.
    files.hard_limit - Specifies the hard limit for files.
    files.soft_limit - Specifies the soft limit for files.
    user_mapping - Specifies the user_mapping. This property is valid only for quota policy rules of type user.
'''
    data = {
        'svm': {'name': vserver_name},
        'volume': {'name': volume_name},
        'type': 'user',
        'users': {'name': user_name},
        'qtree': {'name': qtree_name},
        'user_mapping': 'on',
        'space': {'hard_limit': space_hard, 'soft_limit': 100},
        'files': {'hard_limit': file_hard, 'soft_limit': 100},
    }
    quotarule = QuotaRule(**data)
    try:
        quotarule.post()
        print("Rule 'tree' created successfully for %s" % qtree_name)
    except NetAppRestError as err:
        print("Error: Rule was not created: %s" % err)
    return

def create_qos_policy(vserver_name: str, qos_policy_name: str) -> None:
    data = {
        'name': qos_policy_name,
        'svm': {'name': vserver_name},
        'adaptive': {'expected_iops': 5000, 'peak_iops': 6000, 'absolute_min_iops': 1000}
    }
    qospolicy = QosPolicy(**data)
    try:
        qospolicy.post()
        print("QoS Policy %s created successfully" % qos_policy_name)
    except NetAppRestError as err:
        print("Error: Policy was not created: %s" % err)
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)5s] [%(module)s:%(lineno)s] %(message)s")
    args = parse_args()
    config.CONNECTION = HostConnection(args.cluster, username=args.api_user, password=args.api_pass,
                                       verify=False)
    # Create a quota tree and a policy rule for the qtree
    create_qtree(args.volume_name, args.vserver_name, args.qtree_name)
    create_policy_rule(args.volume_name, args.vserver_name, args.qtree_name,
                            args.user_name,args.space_hard, args.file_hard)
    create_qos_policy(args.vserver_name, args.qos_policy_name)

