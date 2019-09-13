
from Crypto.Hash import SHA256
from systemd import journal
from pprint import pprint
import Crypto.Random
import os
import uuid
import datetime

class Encrypt:

    dataList = []
    headers = []

    def __init__(self):
        nonce = ''
        cipher = ''

    def destructor(self):
        headerLength = len(Encrypt.headers)
        dataLength = len(Encrypt.dataList)
        for i in range(headerLength):
            del Encrypt.headers[0]
            headerLength -= 1

        for i in range(dataLength):
            del Encrypt.dataList[0]
            dataLength -= 1

        del Encrypt.headers
        del Encrypt.dataList
        return

    def abrasion(crumpled):
        sysTime = str(datetime.date.today().year) + hex(uuid.getnode())  # Clocktime for implementation
        k1 = SHA256.new(bytes(crumpled, 'UTF-8') + bytes(sysTime, 'UTF-8'))
        return k1.hexdigest()

    def crumple(raw, padding, nonce):
        nonce = bytes(nonce, 'UTF-8')
        k0 = SHA256.new(nonce) # Generate a new SHA256 'key' with nonce
        k0.update(bytes(str(raw), 'UTF-8') + bytes(str(padding), 'UTF-*8')) # Add in random data and padding
        hash = str(k0.hexdigest()) + str(nonce) # Pad on the nonce as the check post brute force
        k1 = Encrypt.abrasion(hash)

        return k1

    def write_out(self):
        #j = journal.Reader()
        #j.close()

        file = open("/home/main/PycharmProjects/Crypto/log.bin", 'a')
        length = len(Encrypt.dataList)
        for i in range(length):
            data = str(Encrypt.dataList[i]) + "\n"
            file.write(data)
        file.close()
        return

    def load_in(self):
        #file = open("/home/main/PycharmProjects/Crypto/log.json", "r")
        index = 0
        nonce = ''
        j = journal.Reader()
        j.seek_head()
        time = ['_SOURCE_MONOTONIC_TIMESTAMP', 'TIMESTAMP_MONOTONIC','_SOURCE_REALTIME_TIMESTAMP','TIMESTAMP_BOOTTIME']

        for line in j:
            unsorted = []
            dictionary = {}
            test = str(j.enumerate_fields()).replace("{", '').replace("}",'').replace("'",'')
            fields = [x.strip() for x in test.split(',')]
            for i in range(len(fields)):
                dictionary[fields[i]] = line.get(fields[i])
            for key in dictionary:
                if key in time and str(dictionary.get(key)).strip().lower() != 'none':
                    timestamp = dictionary.get(key)
                    dictionary[key] = str(timestamp)
                if key not in unsorted:
                    unsorted.append(key)
            dictionary['index'] = index
            nonce = Encrypt.gen_nonce(4)
            dictionary['nonce'] = nonce
            Encrypt.dataList.append(dictionary)
            Encrypt.headers = sorted(unsorted)
            del unsorted
            del dictionary
            nonce = ''
            index += 1

        j.seek_tail()
        os.system("sudo journalctl --rotate --since '2019-09-11 21:00:00' | sudo journalctl --vacuum-time=1s")
        j.close()
        return

    def search_keyword(self):
        index = len(Encrypt.dataList)
        word = input("Enter keyword to search for: ")
        counter = 0

        for i in range(index):
            if word in Encrypt.dataList[i].values():
                counter += 1
                for key, item in Encrypt.dataList[i].items():
                    if item == word:
                        print("Found in ", key)
                        pprint(Encrypt.dataList[i])

        print("\n\n######")
        return

    def search_nonce(self):
        logIndex = len(Encrypt.dataList)
        headerIndex = len(Encrypt.headers)

        searchNonce = input(r"Enter nonce to search for: ")
        for i in range(headerIndex):
            print(str(i), ": ", Encrypt.headers[i])

        choice = input("Enter header for return value: ")

        for i in range(logIndex):
            for key in Encrypt.dataList[i]:
                if key == Encrypt.headers[int(choice)]:
                    if str(Encrypt.dataList[i]['nonce']).strip() == searchNonce:
                        #pprint(Encrypt.dataList[i])
                        print(key, ": ", Encrypt.dataList[i][key])
        return


    def search_index(self):
        logIndex = len(Encrypt.dataList)
        print("Total records: ", logIndex)
        index = input("Enter index number: ")
        index = int(index)

        for i in range(logIndex):
            if index == Encrypt.dataList[i]['index']:
                pprint(Encrypt.dataList[i])

        return

    def search_header(self):
        logIndex = len(Encrypt.dataList)
        headerIndex = len(Encrypt.headers)
        records = []
        recordsDict = {}
        counter = 0
        pos = 0

        print("Select search term from " + str(logIndex) + " records: ")
        for i in range(headerIndex):
            print(str(i), ": ", Encrypt.headers[i])

        choice = input("Enter choice: ")

        for i in range(logIndex):
            for key in Encrypt.dataList[i]:
                if key == Encrypt.headers[int(choice)]:
                    pos += 1
                    if str(Encrypt.dataList[i][key]).strip() != 'None':
                        recordsDict = Encrypt.dataList[i].copy()
                        records.append(recordsDict)
                        del recordsDict
                        counter += 1
        print("pos = ", pos)
        print("Total records found: ", counter)
        choice = input("Print all? (Y/N): ")
        if choice.lower().strip() == 'y':
            for i in range(len(records)):
                pprint(records[i])
                print("\n\n")
        else:
            print("Returning to main menu...")

        del records
        return

    def gen_nonce(difficulty):
        difficulty = int(difficulty)
        random = Crypto.Random.get_random_bytes(difficulty)
        random = random.hex()
        return random

    def hide_values(self):
        keywords = ['SYSLOG_PID',
                    '_PID',
                    '_EXE',
                    '_MACHINE_ID',
                    'MESSAGE',
                    '_CMDLINE',
                    '_BOOT_ID',
                    '_HOSTNAME',
                    '__CURSOR',
                    'SYSLOG_IDENTIFIER',
                    '_COMM',
                    '_SYSTEMD_UNIT']
        index = len(Encrypt.dataList)

        for i in range(index):
            for key in Encrypt.dataList[i]:
                if key in keywords:
                    data = Encrypt.dataList[i].get(key)
                    nonce = Encrypt.dataList[i].get('nonce')
                    if key == '_SOURCE_REALTIME_TIMESTAMP':
                        padding = Encrypt.dataList[i]['_SOURCE_REALTIME_TIMESTAMP']
                    else:
                        padding = Crypto.Random.get_random_bytes(16)
                    Encrypt.dataList[i][key] = Encrypt.crumple(data, padding, nonce)
        return

    def print_values(self):
        index = len(Encrypt.dataList)

        for i in range(index):
            pprint(Encrypt.dataList[i])

def menu():
    choice = '0'

    print("Loading log file...\n")
    obj = Encrypt()
    obj.load_in()
    obj.hide_values()
    print('###Encryption menu###\nSelect from menu below\n')
    while(choice.lower() != 'q'):
        print("\n\nTotal records: ", str(len(Encrypt.dataList)))
        print("1: Search by header value")
        print("\t Returns all values with the given header.")
        print("2: Search by keyword")
        print("\t Returns all records with the given keyword")
        print("3: Search by nonce")
        print("\t Returns log with the provided nonce")
        print("4: Search by index number")
        print("\t Returns log with the given index number")
        print("5: Print all records")
        print("\t Returns all logs that were captured")
        print("Q: Quit program")
        print("########################")
        choice = input("Enter choice: ")
        if choice == '1':
            obj.search_header()
        elif choice == '2':
            obj.search_keyword()
        elif choice == '3':
            obj.search_nonce()
        elif choice == '4':
            obj.search_index()
        elif choice == '5':
            obj.print_values()
        elif choice.lower() == 'q':
            print("Quitting program.")
            break
        else:
            print("Unknown option, quitting program.")
            break
    obj.write_out()
    obj.destructor()
    del obj

    return


def main():
    menu()

    return 0

##########################

main()
