
# @author Ganem, shady <shady.ganem@intel.com>

class PCIe:
    
    pcie_capabilities_ids = {'pci_express': 0x10,
                             'power_managment': 0x01}

    pcie_supported_Link_speed_vector = {0:'2.5G',
                                       1:'5.0G',
                                       2:'8.0G',
                                       3:'16.0G',
                                       4:'reserved',
                                       5:'reserved',
                                       6:'reserved'}

    pcie_link_speed_encoding = {0x1:0,
                               0x2:1,
                               0x3:2,
                               0x4:3,
                               0x5:4,
                               0x6:5,
                               0x7:6}

    pcie_link_width_encoding = {1:'x1',
                                2:'x2',
                                4:'x4',
                                8:'x8',
                                12:'x12',
                                16:'x16',
                                32:'x32'}

    pcie_power_state_encoding = {0: "D0",
                                 2: "Reserved",
                                 3: "D3hot"}
