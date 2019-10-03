from classInfo import Encrypt

def service():
    obj = Encrypt()
    print("Reading journald...")
    obj.load_in()
    print("Encrypting values...")
    obj.hide_values()
    print("Writing to log.bin...")
    obj.write_out()
    print("Quitting...")
    obj.destructor()
    return

################
service()
quit()
