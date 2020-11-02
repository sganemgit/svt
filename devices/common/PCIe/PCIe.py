

class PCIe:
    pcie_capabilities_ids = {'pci_express': 0x10,
                             'power_managment': 0x01}

    supported_Link_speed_vector = {0:'2.5G',
                                       1:'5.0G',
                                       2:'8.0G',
                                       3:'16.0G',
                                       4:'reserved',
                                       5:'reserved',
                                       6:'reserved'}

    link_speed_encoding = {0x1:0,
                            0x2:1,
                            0x3:2,
                            0x4:3,
                            0x5:4,
                            0x6:5,
                            0x7:6}

    link_width_encoding = {0x1:'x1',
                               0x2:'x2',
                               0x4:'x4',
                               0x8:'x8',
                               0x12:'x12',
                               0x16:'x16',
                               0x32:'x32'}