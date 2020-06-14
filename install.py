import os 
cwd = os.getcwd()
home_dir = os.environ["HOME"]
bashrc_path = home_dir+ "/.bashrc"

with open(bashrc_path ,'a') as bashrc:
    bashrc.write(F"\nexport PYTHONPATH=$PYTHONPATH:{cwd}")

    
