import subprocess

systemCheck = {
    "python3.5 -c \"import Crypto\"": 0,
    "python3.5 -c \"import systemd\"": 0,
    "python3.5 -c \"import csv\"": 0,
    "python3.5 -c \"import pprint\"": 0,
    "python3.5 -c \"import pickle\"": 0,
    "python3.5 -c \"import gc\"": 0,
    "python3.5 -c \"import progressbar\"": 0,
    "dpkg-query -l | grep systemd >> /dev/null": 0}

def checkup():
    checkValue = 0
    for key in systemCheck:
        checker = subprocess.call(key, shell=True)
        if checker == 0:
            systemCheck[key] = checker
        else:
            systemCheck[key] == 1

    for key in systemCheck:
        if systemCheck[key] > 0:
            print("Error in checkup\n", key)
            checkValue = 1

    del checker
    return checkValue