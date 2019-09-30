from classInfo import Encrypt

def service():
    obj = Encrypt()
    obj.load_in()
    obj.hide_values()
    obj.write_out()
    obj.destructor()
    return

