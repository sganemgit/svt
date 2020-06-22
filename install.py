import os
cwd = os.getcwd()
home_dir = os.environ["HOME"]
bashrc_path = home_dir+ "/.bashrc"

with open(bashrc_path ,'a+') as bashrc:
    found = False
    for line in bashrc:
        if cwd in line:
            print("path is set")
            found = True
    if not found:
         bashrc.write("\nexport PYTHONPATH=$PYTHONPATH:{}".format(cwd))
         print("need to open a new terimnal for the changes to take place")

