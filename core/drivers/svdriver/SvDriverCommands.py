import subprocess


def svdt(flag):
    if flag == "-s":
        output = subprocess.check_output(["svdt","-s"])
        return output    


def check_device_availability(project_name, device_number, port_number):
    try:
        output = subprocess.check_output(["svdt","-s"])
        output = output.decode(encoding = "utf-8")
        lines = output.split("\n")
        print(output)
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

    
if __name__=="__main__":
    print(check_device_availability("cvl", 1, 2))
