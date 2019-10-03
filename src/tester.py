import os
import subprocess
import time
import datetime
from classInfo import Encrypt

def testing(value):
    journalMeasure = ["stat", "/var/log/journal/f5298e06c9e74d7093fc818f09b1bca7/ >> "]
    logMeasure = ["stat", "/home/main/PycharmProjects/CryptoCrumple/logs/log.bin"]
    file = "values.txt"
    endTime = time.time() + (3600 * int(value))
    os.chdir("../logs/")
    obj = Encrypt()
    os.system("sudo journalctl --rotate | sudo journalctl --vacuum-time=1s")
    while time.time() < endTime:
        outfile = open(file, 'a')
        os.system("sudo journalctl -o verbose >> /home/main/PycharmProjects/CryptoCrumple/logs/journaltext.txt "
                  "&& stat /home/main/PycharmProjects/CryptoCrumple/logs/journaltext.txt >> /home/main/PycharmProjects/CryptoCrumple/logs/journalsize.txt")
        #outfile.write(str(return_code))
        outfile.write('\n')
        obj.load_in()
        obj.hide_values()
        obj.write_out()
        obj.dataList.clear()
        os.system("stat /home/main/PycharmProjects/CryptoCrumple/logs/log.bin >> /home/main/PycharmProjects/CryptoCrumple/logs/logsize.txt")
        #outfile.write(str(return_code))
        outfile.write('\n')
        outfile.close()
        time.sleep(10)
        os.system("sudo journalctl --rotate | sudo journalctl --vacuum-time=1s")
    obj.destructor()
    return

testing(10)
