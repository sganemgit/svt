from core.drivers.svdriver.SvDriverCommands import svdt

'''This data structure holds the information neccessry for creating a driver instance'''
class DeviceInfo():        
    def __init__(self, device_name, device_number, port_number):
        self.device_name = device_name
        self.device_number = device_number
        self.port_number = port_number

    def get_info_from_driver(self):
        svdt_dump = svdt("-s")
        print(svdt_dump)
        #TODO implement a parsing method to extract device info ftom svdt string




if __name__=="__main__":
    temp = DeviceInfo("cvl",0,0)
    temp.get_info_from_driver()


