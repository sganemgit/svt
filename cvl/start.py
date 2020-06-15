from cvl import cvl 

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

cvl0 = cvl(0,0)
cvl1 = cvl(0,1)

cvl0.print_info()

cvl1.print_info()





