#!/bin/bash

while true;
do
    CURRENTDATE=`date +"%Y-%m-%d %T"`
    echo "Checking logs for " ${CURRENTDATE}
    sudo python3.5 /home/main/PycharmProjects/Crypto/crumpleService.py
    sleep 1d
done
