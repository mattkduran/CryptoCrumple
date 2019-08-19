'''
receiverID = SHA256(x)
senderID = SHA256(receiverID)
'''

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import os

class Encrypt:
    dataList = []

    def __init__(self):
        nonce = ''
        cipher = ''

    def encrypt(nonce):
        cipher = AES.new(nonce, AES.MODE_CFB)
        ciphertext = cipher.encrypt(input("Enter encrypted text: ").encode())
        return ciphertext

    def gen_nonce(self):
        random = os.urandom(8).hex().encode()
        return random

    def add_values(self):
        dictionary = {}

        index = len(Encrypt.dataList)
        nonce = Encrypt.gen_nonce(self)
        data = Encrypt.encrypt(nonce)
        dictionary['index'] = index
        dictionary['key'] = nonce
        dictionary['data'] = data
        Encrypt.dataList.append(dictionary)

        del dictionary
        return

    def print_values(self):
        index = len(Encrypt.dataList)

        for i in range(index):
            print(Encrypt.dataList[i])

'''
# Probably only necessary if using CBC mode
def pad(text):
    while len(text) % 8 != 0:
        text += ' '
    text = text.encode()
    return text
'''

def menu():
    choice = '0'
    obj = Encrypt()

    print('###Encryption menu###\nSelect from menu below\n')
    while(choice.lower() != 'q'):
        print("1: Add encrypted value")
        print("2: Print out current list")
        print("Q: Quit program")
        choice = input("Enter choice: ")
        if choice == '1':
            obj.add_values()
        elif choice == '2':
            obj.print_values()
        else:
            print("Quitting program.")
            break
    return


def main():
    #menu()

    h = SHA256.new()
    h.update(b'Hello')
    print(h)

    return 0

##########################

main()