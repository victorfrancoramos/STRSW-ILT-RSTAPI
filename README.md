# STRSW-ILT-RSTAPI
COURSE OUTLINE 

Module 1 : ONTAP REST API Overview 
Module Duration : 60 minutes 
Module Objectives: 
Understand the REST API concepts 
Details of ONTAP REST API 
Examine the set of tools and resources available 
Module Topics: 
Introduction to ONTAP REST API 
REST API Categories and Error Codes 
REST API / Swagger Interface and JSON (understanding the actual models and interpreting required/optional JSON settings) 
Resources available to developers 

Module 2: REST API Use Cases – Python Programming 
Module Duration : 60 minutes 
Exercise Duration : 45 minutes 
Module Objectives : 
Describe some of the popular use cases of REST API 
Demonstrate those use cases by means of Python programs 
Module Topics: 
Describe how to create an aggregate, an SVM and a volume 
Describe how to list all the volumes in an SVM 
Create a QTree; set quota for a QTree and define rules for the quota 
Set permission to provide user the access – VServer file security file/directory 
Create a QOS policy and assign it to a volume 
Manage volume snapshots – schedules, policies and clones 
Manage volume and QTree quota – set and update quota 
Move, resize and delete volumes 
CLI examples: ONTAP commands / Curl Utility 
Python program examples 
Lab Exercises : 
Configure services, network ports, roles and users 
Verify security  

Module 3: REST API Use Cases – PowerShell Scripts 
Module Duration : 60 minutes 
Exercise Duration : 45 minutes 
Module Objectives : 
Describe some of the popular use cases of REST API 
Demonstrate those use cases by means PowerShell scripts 
Module Topics: 
Demonstrate PowerShell scripts for the same use cases as described in Module 2 above 
Show the PowerShell functions (that invoke Rest method) alongside the Python code 
In future, we will have a native PowerShell module that will hide the details of the REST calls and operate on strongly typed objects – To Be Done Later 
Lab Exercises : 
Configure services, network ports, roles and users 
Verify security  

Module 4: Automation Using Ansible 
Module Duration: 60 minutes 
Exercise Duration: 60 minutes 
Module Objectives : 
Understand the Ansible infrastructure that is used in automation 
Understand Ansible Playbooks 
Understand Ansible Conditionals, Handlers, and Loops 
Module Topics: 
Ansible Infrastructure 
Ansible Playbooks 
Ansible Conditionals, Handlers and Loops 
Ansible na_ontap_* modules (not specifically REST) 
Create all of topics in Module 2 (REST API Use Cases) using Ansible URI module 
Lab Exercise : 
Write Ansible Playbook to execute ONTAP Ansible modules 

Module 5: CIFS Configuration 
Module Duration : 60 minutes 
Exercise Duration : 60 minutes 
Module Objectives : 
Review all the steps required to configure CIFS 
Module Topics: 
Create a new NAS-enabled SVM for CIFS 
Create an interface for the Data LIF 
Create a route 
Create DNS servers 
Create a CIFS server 
Create a CIFS share and map a network drive 
Provision storage for NAS - CIFS 
Lab Exercise : 
Configure CIFS by writing Ansible Playbook to execute ONTAP Ansible modules 

Module 6: NFS Configuration 
Module Duration: 60 minutes 
Exercise Duration: 45 minutes 
Module Objectives: 
Learn about the configuration of NFS 
Module Topics: 
Creating a new NFS-enabled SVM 
Creating a new SVM with an NFS volume and export 
Opening the export policy of the SVM root volume 
Configuring LDAP 
Configuring and verifying NFS client access 
Provision Storage for NAS - NFS 
Lab Exercise : 
Configure NFS by writing Ansible Playbook to execute ONTAP Command modules 

Module 7: SAN Configuration 
Module Duration: 60 minutes 
Exercise Duration: 45 minutes 
Module Objectives : 
Learn about the configuration of SAN with iSCSI protocol and Linux/Windows OS host 
Module Topics: 
iSCSI Protocol 
Create an aggregate and SVM 
Provision a volume for SAN - iSCSI 
Create a LUN 
Verify host can access multipath device 
Lab Exercise : 
Configure SAN by writing Ansible Playbook to execute ONTAP PowerShell modules 

Module 8: Performance Monitoring 
Module Duration: 30 minutes 
Exercise Duration: 30 minutes 
Module Objectives : 
Collect performance metrics for volumes and LUNs 
Collect protocol metrics for NFS and CIFS 
Module Topics: 
Performance Metrics 
Protocol Metrics 
Lab Exercise : 
Monitor performance by writing Ansible Playbook to execute ONTAP Command modules 
