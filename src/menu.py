from classInfo import Encrypt
import datetime


def menu():
    choice = '0'
    today = datetime.datetime.today()
    nextYear = datetime.date(datetime.datetime.now().year, 1, 1)
    nextYear += datetime.timedelta(days=365)
    delta = nextYear - today.date()
    print("Loading log file...\n")
    obj = Encrypt()
    obj.load_in_from_file()
    print(delta.days, " days left until key changes")
    print('###Encryption menu###\nSelect from menu below')
    while(choice.lower() != 'q'):
        print("Total records: ", str(len(Encrypt.dataList)))
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
    obj.destructor()
    del obj
    del choice
    del today
    del nextYear
    del delta
    return

