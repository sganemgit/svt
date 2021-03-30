
# @author Ganem, shady <shady.ganem@intel.com>

class PMBus:

    #from table 19 "command summary" PMBus spepcificatoin PartII revesion 1.0
    pmbus_commands = {"page": 0x0,
                      "operation": 0x1,
                      "on_off_config": 0x2,
                      "clear_fault": 0x3,
                      "write_protect": 0x10,
                      "store_default_all": 0x11,
                      "restore_default_all": 0x14,
                      "vout_mode": 0x20,
                      "vout_command": 0x21,
                      "vout_trim": 0x22, 
                      "vout_call": 0x23}
