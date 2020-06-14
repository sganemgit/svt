import subprocess


def svdt(flag):
    if flag == "-s":
        output = subprocess.check_output(['svdt','-s'])
        return output    

