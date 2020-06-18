import subprocess


def svdt(flag):
    if flag == "-s":
        output = subprocess.check_output(["svdt","-s"])
        return output    


def check_device_availability(project_name, device_number, port_number):
    try:
        output = svdt("-s")
        output = output.decode(encoding = "utf-8")
        lines = output.split("\n")
        for line in lines:
            if project_name in line:
                line_components = line.split()
                if line_components[2] == str(device_number):
                    if line_components[3] == str(port_number):
                        return True
        return False
    except Exception as e:
        print("svdt -s failed:")
        print(str(e))

def get_device_id_by_name(project_name, device_number, port_number):
    output = svdt("-s")
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    for line in lines:
        if project_name in line:
            line_component = line.split()
            if line_component[2] == str(device_number):
                if line_component[3] == str(port_number):
                    return line_component[5].replace("0x","")

def get_device_bdf_by_name(project_name, device_number, port_number):
    output = svdt("-s")
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    for line in lines:
        if project_name in line:
            line_component = line.split()
            if line_component[2] == str(device_number):
                if line_component[3] == str(port_number):
                    return line_component[4]
def get_device_specific_id(project_name,device_number, port_number):
    output = svdt("-s")
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    for line in lines:
        if project_name in line:
            line_component = line.split()
            if line_component[2] == str(device_number):
                if line_component[3] == str(port_number):
                    return line_component[1]

def get_detected_devices(project_name):
    output = svdt("-s")
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    devices = dict()
    for line in lines:
        if project_name in line:
            line_component = line.split()
            info = dict()
            info['device_number'] = line_component[2]
            info['port_number'] = line_component[3]
            devices[line_component[0]] = info
    return devices

if __name__=="__main__":
    print(get_device_specific_id("cvl",0,0))
