from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from systemd import journal
from pprint import pprint
import Crypto.Random
import os
import datetime
import pickle
import gc



class Encrypt:
    dataList = []
    headers = []
    sysTime = bytes(str(datetime.date.today().year), 'UTF-8')

    def __init__(self):
        nonce = b''
        cipher = ''

    def destructor(self):
        headerLength = len(Encrypt.headers)
        for i in range(headerLength):
            del Encrypt.headers[0]
            headerLength -= 1
        Encrypt.dataList.clear()
        del Encrypt.headers
        del Encrypt.dataList
        gc.collect()
        return

    def abrasion(crumpled, raw, nonce): # Move to crumple.py
        k1 = Encrypt.sysTime + crumpled
        e_cipher = AES.new(k1[0:32], AES.MODE_CFB)
        raw = bytes(str(raw), 'UTF-8')
        ciphertext = e_cipher.encrypt(raw)
        del k1
        del e_cipher
        del raw
        gc.collect()
        return ciphertext

    def crumple(raw, padding, nonce): # Move to crumple.py
        seed = nonce + padding
        k0 = SHA256.new(seed) # Generate a new SHA256 'key' with nonce
        hash = nonce + k0.digest() # Pad on the nonce as the check post brute force
        k1 = Encrypt.abrasion(hash, raw, nonce)
        del seed
        del k0
        del hash
        gc.collect()
        return k1

    def gen_nonce(difficulty):
        difficulty = int(difficulty)
        random = Crypto.Random.get_random_bytes(difficulty)
        del difficulty
        gc.collect()
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
        print("Starting for loop")
        for i in range(index):
            for key in Encrypt.dataList[i]:
                if key in keywords:
                    data = Encrypt.dataList[i].get(key)
                    nonce = Encrypt.dataList[i].get('nonce')
                    padding = Crypto.Random.get_random_bytes(16)
                    Encrypt.dataList[i][key] = Encrypt.crumple(data, padding, nonce)
            del padding
            del nonce
            del data
        del index
        del keywords
        gc.collect()
        return

    def write_out(self):
        file = "/home/main/PycharmProjects/Crypto/log.bin"
        with open(file, 'ab') as outfile:
            for i in range(len(Encrypt.dataList)):
                pickle.dump(Encrypt.dataList[i], outfile, protocol=pickle.HIGHEST_PROTOCOL)
        del file
        del outfile
        gc.collect()
        return

    def load_in_from_file(self):
        file = "/home/main/PycharmProjects/Crypto/log.bin"
        with open(file, 'rb') as infile:
            infile.seek(0)
            while True:
                try:
                    Encrypt.dataList.append(pickle.load(infile))
                except EOFError:
                    print("Reached end of file")
                    break
        del file
        gc.collect()
        return

    def load_in(self): # Move sections to crumple.py
        index = 0
        j = journal.Reader()
        j.seek_head()
        time = ['_SOURCE_MONOTONIC_TIMESTAMP', 'TIMESTAMP_MONOTONIC','_SOURCE_REALTIME_TIMESTAMP','TIMESTAMP_BOOTTIME']
        for line in j:
            unsorted = []
            dictionary = {}
            enum = str(j.enumerate_fields()).replace("{", '').replace("}",'').replace("'",'')
            fields = [x.strip() for x in enum.split(',')]
            for i in range(len(fields)):
                dictionary[fields[i]] = line.get(fields[i])
            for key in dictionary:
                if key in time and str(dictionary.get(key)).strip().lower() != 'none':
                    timestamp = dictionary.get(key)
                    dictionary[key] = str(timestamp)
                if key not in unsorted:
                    unsorted.append(key)
            dictionary['index'] = index
            dictionary['nonce'] = Encrypt.gen_nonce(20)
            Encrypt.dataList.append(dictionary)
            Encrypt.headers = sorted(unsorted)
            del unsorted
            del dictionary
            index += 1
        j.seek_tail()
        os.system("sudo journalctl --rotate | sudo journalctl --vacuum-time=1s")
        j.close()
        del j
        del time
        gc.collect()
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
        del counter
        del word
        del index
        gc.collect()
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
                        print(key, ": ", Encrypt.dataList[i][key])
        del logIndex
        del headerIndex
        del searchNonce
        del choice
        gc.collect()
        return


    def search_index(self):
        logIndex = len(Encrypt.dataList)
        print("Total records: ", logIndex)
        index = input("Enter index number: ")
        index = int(index)
        for i in range(logIndex):
            if index == Encrypt.dataList[i]['index']:
                pprint(Encrypt.dataList[i])
        del logIndex
        del index
        gc.collect()
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
        del logIndex
        del headerIndex
        del counter
        del pos
        del choice
        gc.collect()
        return

    def print_values(self):
        index = len(Encrypt.dataList)
        for i in range(index):
            pprint(Encrypt.dataList[i])
        del index
        gc.collect()
        return