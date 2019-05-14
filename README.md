# CCC-Assignment-2-Group-49

This is the repository for Assignment 2 of COMP90024 Cluster and Cloud Computing Assignment 2, group 49.

To deploy the system, follow the steps:
* Clone this repository and go to the deployment folder
*	Login to Unimelb Research Cloud, navigate to user => OpenStack RC File and download the file to the current folder. Rename the file to openrc.sh
*	Navigate to user => Settings => Reset Password, reset your password and save it into a file named “openstackkey” to the current folder
*	Navigate to Compute => Key Pairs, create a new key pair named “myKey”, save the generated myKey.pem file to the current folder.
*	By this point you should have the following additional files in the deployment folder: openrc.sh, openstackkey, myKey.pem
*	Run `./run_local.sh < openstackkey` on the command line to start creation of the instance. You may have to enter your Linux sudo password to continue.
*	After the first script finishes execution successfully, run `./run_remote.sh < openstackkey` to start deployment of the system. You may have to wait for a little while for the new instance to become available for access.  
