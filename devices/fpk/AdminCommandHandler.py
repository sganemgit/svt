
# @author Shady Ganem <shady.ganem@intel.com>

from core.utilities.BitManipulation import *
from core.structs.AqDescriptor import AqDescriptor

class AdminCommandHandler:
    def __init__(self, driver_reference):
        self.driver = driver_reference

    def SetPhyConfig(self, config, debug=False):
        pass 

    def GetPhyAbilities(self, config, debug=False):
        aq_desc = AqDescriptor()
        data_len = 0x1000
        aq_desc.opcode = 0x0600
        aq_desc.datalen = data_len
        buffer = [0] * data_len
        aq_desc.param0 = config.get("report_active_init", 0x1) << 1 | config.get("report_qualified_modules", 0x1)
        aq_desc.param1 = 0
        aq_desc.addr_high = 0
        aq_desc.addr_low = 0
        aq_desc.flags = 0x1200  
        status = self.driver.send_aq_command(aq_desc, buffer, debug, False)
        if status != 0 or aq_desc.retval != 0:
            msg = "Failed to send Get PHY Abilities Admin Command, status: {} FW ret value: {}".format(status, aq_desc.retval)
            print(msg)
            raise Exception(msg)
            
        err_flag = (aq_desc.flags & 0x4) >> 2  # isolate the error flag

        if status or err_flag:
            status = (True, aq_desc.retval)
        else:
            # The static section of Get PHY Abilities is 32 bytes
            # ut.compose_num_from_array_slice(input, index, width)
            data = {}
            data['phy_type'] = compose_num_from_array_slice(buffer, 0, 4)
            data["link_speed_abil"] = compose_num_from_array_slice(buffer, 4, 1)
            data["pause_abil"] = compose_num_from_array_slice(buffer, 5, 1) & 0x3
            data["low_power_abil"] = compose_num_from_array_slice(buffer, 5, 1) & 0x4
            data["link_mode"] = compose_num_from_array_slice(buffer, 5, 1) & 0x8
            data["AN_mode"] = compose_num_from_array_slice(buffer, 5, 1) & 0x8
            data["enable_module_qualification"] = compose_num_from_array_slice(buffer, 5, 1) & 0x10
            data["EEE_caps"] = compose_num_from_array_slice(buffer, 6, 2) 
            data["EEER"] = compose_num_from_array_slice(buffer, 8, 4) 
            data["Low_power_control"] = compose_num_from_array_slice(buffer, 12, 1) 
            data["current_phy_id"] = compose_num_from_array_slice(buffer, 16, 4) 

            status = (False, data)
        return status
