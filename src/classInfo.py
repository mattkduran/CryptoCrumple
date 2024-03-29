from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from systemd import journal
from pprint import pprint
import Crypto.Random
import os
import datetime
import pickle
import gc
import progressbar


# classInfo contains the Encrypt class for the CryptoCrumple program.
# The Encrypt class consists of functions which allow the program to
# append journald entries into a dictionary in an array. Certain entries
# are passed to two functions which hash and encrypt the message contents,
# obscuring the information. Further descriptions of the functions and their
# operations are below.

class Encrypt:
    dataList = [] # Houses the journald entires
    headers = [] # Houses the different types of messages for search functions
    sysTime = bytes(str(datetime.date.today().year), 'UTF-8') # Used for key

# Initialization function, creates a bytestring for the nonce 
    def __init__(self):
        nonce = b''

# destructor takes only itself as a parameter, is used during 
# the quitting process. Clears each entry in the headers array
# as well as all the contents of the dataList dictionary.
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

# abrasion takes three parameters defined as follows:
#	crumpled: The hashed key passed from the crumple function. Bytes
#	raw: The raw message contents to be encrypted. String
#	nonce: The nonce to be prepended to the key. Bytes
# The abrasion function takes the contents sent from the crumple function
# to create an AES key and encrypt the message content. This key is currently
# set to be 32 bytes long but can be adjusted in the cipher declaration. 
# They first 32 bytes are used to create the AES key and the remaining bytes
# are discarded. The variable ciphertext is returned back to crumple to be 
# added to the dataList dictionary.
    def abrasion(crumpled, raw, nonce):
        k1 = Encrypt.sysTime + crumpled
        e_cipher = AES.new(k1[0:32], AES.MODE_CFB)
        raw = bytes(str(raw), 'UTF-8')
        ciphertext = e_cipher.encrypt(raw)
        del k1
        del e_cipher
        del raw
        gc.collect()
        return ciphertext

# crumple takes three parameters defined as follows:
#	raw: raw message contents to be encrypted. String
#	padding: random bytes generated and/or random content to be concatenated
#		with nonce in order to increase difficulty. Bytes
#	nonce: random bytes generated which are also saved in dataList under the 
#		key 'nonce' to confirm a correct value during decryption. Bytes
# crumple hashes the nonce and padded content to provide a portion of a key for
# the abrasion function. The raw text is unmodified and passed to the abrasion function
# in order to be encrypted. This is passed back as k1 which is returnedand appended to 
# the dataList dictionary.
    def crumple(raw, padding, nonce):
        seed = nonce + padding
        k0 = SHA256.new(seed)
        hash = nonce + k0.digest()
        k1 = Encrypt.abrasion(hash, raw, nonce)
        del seed
        del k0
        del hash
        gc.collect()
        return k1
# gen_nonce takes one parameter defined as follows:
#	difficulty: the number of bytes to generate for the nonce. Integer
    def gen_nonce(difficulty):
        difficulty = int(difficulty)
        random = Crypto.Random.get_random_bytes(difficulty)
        del difficulty
        gc.collect()
        return random

# hide_values only takes itself as a parameter.
# hide_values parses through dataList in order to find certain keys which are to be encrypted.
# These keys are defined in the keywords array and are all values in journald entries.
# If one of the below keywords are found in the for loop, these are passed to the crumple function.
# The padding passed to the crumple function is also created here -- currently hardcoded as 16 
# random bytes.
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
        bar = progressbar.ProgressBar(max_value=index)
        for i in range(index):
            for key in Encrypt.dataList[i]:
                if key in keywords:
                    data = Encrypt.dataList[i].get(key)
                    nonce = Encrypt.dataList[i].get('nonce')
                    padding = Crypto.Random.get_random_bytes(16)
                    Encrypt.dataList[i][key] = Encrypt.crumple(data, padding, nonce)
            bar.update(i)
            del padding
            del nonce
            del data
        del index
        del keywords
        del bar
        gc.collect()
        return
# write_out only takes itself as a parameter.
# write_out uses the pickle function in order to append dataList to the log.bin file.
# log.bin is located in the logs folder, all data is written in binary format. write_out 
# is called after all necessary data is encrypted.
    def write_out(self):
        file = "log.bin"
        os.chdir("../logs/")
        try:
            with open(file, 'ab') as outfile:
                for i in range(len(Encrypt.dataList)):
                    pickle.dump(Encrypt.dataList[i], outfile, protocol=pickle.HIGHEST_PROTOCOL)
        except IOError:
            print("log.bin not found")
        del file
        gc.collect()
        os.chdir("../src/")
        return

# load_in_from_file only takes itself as a parameter.
# load_in_from_file uses the pickle function in order to read in the data stored in log.bin.
# log.bin is located in the logs folder, all data is written in binary format. All data stored 
# in log.bin is appended to dataList with the pickle function. 
    def load_in_from_file(self):
        file = "log.bin"
        unsorted = []
        count = 0
        os.chdir("../logs/")
        bar = progressbar.ProgressBar(redirect_stdout=True,
                                      max_value=progressbar.UnknownLength)
        try:
            with open(file, 'rb') as infile:
                infile.seek(0)
                while True:
                    Encrypt.dataList.append(pickle.load(infile))
                    count += 1
                    bar.update(count)
                    for key in Encrypt.dataList:
                        if key not in unsorted:
                            unsorted.append(key)
        except IOError:
            print("log.bin not found")
        except EOFError:
            print("Expected more file but reached end")
        Encrypt.headers = sorted(unsorted)
        del unsorted
        del file
        del bar
        del count
        os.chdir("../src")
        gc.collect()
        return

# load_in only takes itself as a parameter.
# load_in accomplishes four main tasks:
#	- Reads in entries from the journald log to eventually append to dataList
#	- Appends the journald header values to the headers array for searching values
#	- Generates the nonce to be associated with a given entry in dataList
#	- Deletes the plaintext entries in journald
#
    def load_in(self):
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

# search_keyword only takes itself as a parameter.
# search_keyword prompts the user to select which keyword to find in 
# dataList. The function takes the chosen entry from the headers array
# and returns all entries in dataList that have that key.
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

# search_nonce only takes itself as a parameter.
# search_nonce prompts the user for a known nonce to find in 
# dataList. The function searches through dataList for all
# entries where the given nonce matches the 'nonce' key.
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

# search_index only takes itself as a parameter.
# search_index prompts the user to enter an index value (starting at 0) 
# and returns all keys in dataList for that index value.
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

# search_keyword only takes itself as a parameter.
# search_header prompts the user to select a header to find in 
# dataList. The function takes the chosen entry from the headers array
# and returns all entries in dataList that have that key. It includes
# where in the entry the header value is found with the pos variable.
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

# print_values only takes itself as a parameter.
# print_values prints a formatted block of all entries found in dataList.
    def print_values(self):
        index = len(Encrypt.dataList)
        for i in range(index):
            pprint(Encrypt.dataList[i])
        del index
        gc.collect()
        return
