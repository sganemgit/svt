from cvl import cvl 
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
cvl0.EthStartTraffic()

time.sleep(5)
cvl0.EthStopTraffic()


cvl0.GetTPR()

cvl0.GetTPT()
