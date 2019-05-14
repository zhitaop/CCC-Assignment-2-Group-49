#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=./myKey.pem remote.yaml 