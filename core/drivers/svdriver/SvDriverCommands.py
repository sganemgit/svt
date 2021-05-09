
# @author Shady Ganem <shady.ganem@intel.com>

import subprocess

def port_discovery():
    output = subprocess.check_output(["port_discovery"])
    return output

def svdt(flag, remote = ''):
    if remote:
        output = subprocess.check_output(["svdt", flag, remote])
    else:
        output = subprocess.check_output(["svdt",flag])
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

def get_detected_devices(project_name, remote = ''):
    output = svdt("-s", remote) 
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    devices = dict()
    for line in lines:
        if project_name in line:
            line_component = line.split()
            if len(line_component) >= 12:
                info = dict()
                info['device_number'] = line_component[2].replace("@"+remote, "")
                info['port_number'] = line_component[3]
                info["driver_family"] = line_component[10]
                devices[line_component[0].replace("@","_")] = info
    return devices

def detect_connected_devices():
    output = port_discovery()
    output = output.decode(encoding = "utf-8")
    lines = output.split("\n")
    pairs = list()
    for line in lines:
        if "is connected to" in line:
            line_components = line.split()
            pair = dict()
            pair["first"] = line_components[0]
            pair["second"] = line_components[-1]
            pairs.append(pair)
    return pairs

if __name__=="__main__":
    print(get_detected_devices('cvl'))
