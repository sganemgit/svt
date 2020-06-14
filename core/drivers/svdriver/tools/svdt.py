import subprocess



class svdt:
    @classmethod 
    def reset(cls,device_name, reset_type):
        '''this method will call svdt -r to perform a reset'''
        output = subprocess.check_output(['svdt','-r',device_name,reset_type])
        return output





if __name__=="__main__":
   svdt.reset("cvl:0","empr")

