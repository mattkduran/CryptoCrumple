
from Crypto.Hash import SHA256
from datetime import datetime
import Crypto.Random
import json

class Encrypt:

    dataList = []
    headers = []

    def __init__(self):
        nonce = ''
        cipher = ''

    def encrypt(data):
        data = bytes(data, 'UTF-8')
        cipher = SHA256.new(data)
        return cipher.digest()

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
                #print("Here it is!")
                for key, item in Encrypt.dataList[i].items():
                    if item == word:
                        print("Found in ", key)
                        print(Encrypt.dataList[i])

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
        term = Encrypt.headers[int(choice)]

        for i in range(logIndex):
            for j in Encrypt.dataList[i]:
                if term in Encrypt.dataList[i]:
                    print("Index: ", Encrypt.dataList[i]['index'])
                    print(Encrypt.dataList[i])
        print("\n","\n")

        return

    def gen_nonce():
        random = Crypto.Random.get_random_bytes(8)
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
                    Encrypt.dataList[i][key] = Encrypt.encrypt(data)
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
        else:
            print("Quitting program.")
            break
    return


def main():
    menu()
    return 0

##########################

main()

