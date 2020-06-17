from cvl import cvl 
import sys
import time

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")



#TODO: dynammically detect devices and instantiant object accordingly

print("intializing cvl objects")

for i in range(2):
    globals()["cvl" + str(i)] = cvl(0,i)



cvl0.DBG_print_cvl_info()
cvl1.DBG_print_cvl_info()

def MacloopbackWithLP():
    print "teseting for 1000SGMII"
    print "FECs are NoFec"
    reset_list = ["pfr","globr","empr"]


    for reset in reset_list:
        cvl0.SetPhyConfiguration("1G-SGMII","NO_FEC")
        time.sleep(10)
        timer = time.time() + 20 #20 seconds timer 
        while True:
            macLinkStatus = cvl0.GetMacLinkStatus()
            print macLinkStatus
            if time.time() > timer and macLinkStatus == 0:
                print("link is Down")
                sys.exit()
            elif macLinkStatus == 1:
                print("LINK IS UP")
                break
if __name__=="__main__":
    pass
#    MacloopbackWithLP()
