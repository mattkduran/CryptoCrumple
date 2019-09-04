
from Crypto.Hash import SHA256
import Crypto.Random
import json

class Encrypt:

    dataList = []
    headers = []

    def __init__(self):
        nonce = ''
        cipher = ''

    def crumple(raw, padding, nonce):
        sysTime = '20190903' # Clocktime for implementation
        k0 = SHA256.new(nonce) # Generate a new SHA256 'key' with nonce
        k0.update(bytes(str(raw), 'UTF-8') + bytes(str(padding), 'UTF-*8')) # Add in random data and padding
        hash = str(k0.hexdigest()) + str(nonce) # Pad on the nonce as the check post brute force
        k1 = SHA256.new(bytes(hash, 'UTF-8') + bytes(sysTime, 'UTF-8')) # Abrasion with system time added on, then run through SHA256
        return k1.hexdigest()

    def load_in(self):
        file = open("/home/main/PycharmProjects/Crypto/log.json", "r")
        index = 0
        nonce = ''

        for line in file:
            dictionary = json.loads(line)
            for key in dictionary:
                if key not in Encrypt.headers:
                    Encrypt.headers.append(key)
            dictionary['index'] = index
            nonce = Encrypt.gen_nonce()
            dictionary['nonce'] = nonce
            Encrypt.dataList.append(dictionary)
            del dictionary
            nonce = ''
            index += 1
        file.close()
        return

    def search_keyword(self):
        index = len(Encrypt.dataList)
        word = input("Enter keyword to search for: ")

        for i in range(index):
            if word in Encrypt.dataList[i].values():
                for key, item in Encrypt.dataList[i].items():
                    if item == word:
                        print("Found in ", key)
                        print(Encrypt.dataList[i])

        print("\n\n######")
        return

    def search_header(self):
        logIndex = len(Encrypt.dataList)
        headerIndex = len(Encrypt.headers)
        choice = ''
        term = ''

        print("Select search term from " + str(logIndex) + " records: ")
        for i in range(headerIndex):
            print(str(i), ": ", Encrypt.headers[i])
        choice = input("Enter choice: ")
        if int(choice) <= headerIndex - 1:
            term = Encrypt.headers[int(choice)]
            for i in range(logIndex):
                for j in Encrypt.dataList[i]:
                    if term in Encrypt.dataList[i]:
                        print("Index: ", Encrypt.dataList[i]['index'])
                        print(Encrypt.dataList[i])
        else:
            print("Choice out of range, dropping to main menu.")
        print("\n","\n")

        return

    def gen_nonce():
        random = Crypto.Random.get_random_bytes(16)
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
                    '__CURSOR']
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
            print(Encrypt.dataList[i])

def menu():
    choice = '0'

    print("Loading log file...\n")
    obj = Encrypt()
    obj.load_in()
    obj.hide_values()
    print('###Encryption menu###\nSelect from menu below\n')
    while(choice.lower() != 'q'):
        print("1: Search by header value")
        print("\t Returns all values with the given header.")
        print("2: Search by keyword")
        print("\t Returns all records with the given keyword")
        print("3: Print all records")
        print("\t Returns all logs that were captured")
        print("Q: Quit program")
        print("########################")
        choice = input("Enter choice: ")
        if choice == '1':
            obj.search_header()
        elif choice == '2':
            obj.search_keyword()
        elif choice == '3':
            obj.print_values()
        elif choice.lower() == 'q':
            print("Quitting program.")
            break
        else:
            print("Unknown option, quitting program.")
            break
    return


def main():
    menu()
    return 0

##########################

main()

