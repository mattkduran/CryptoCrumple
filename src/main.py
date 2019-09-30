from menu import menu
import systemCheck

def main():
    checkFail = 0

    checkFail = systemCheck.checkup()
    if checkFail == 0:
        print("System check passed, loading menu...")
        service()
        menu()
    else:
        print("System check up failed.\nReference error codes to verify problem.")

##########################

main()
