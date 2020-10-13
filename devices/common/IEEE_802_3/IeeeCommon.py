


class IeeeCommon:
	
    fec_dict = {"400G-AUI8": ['25G_RS_544_FEC'],
                "400G-AUI8-AOC-ACC":['25G_RS_544_FEC'],
                "400GBase-DR4":['25G_RS_544_FEC'],
                "400GBase-LR8":['25G_RS_544_FEC'],
                "400GBase-FR8":['25G_RS_544_FEC'],
                "200G-AUI8":['25G_RS_544_FEC'],
                "200G-AUI8-AOC-ACC":['25G_RS_544_FEC'],
                "200G-AUI4":['25G_RS_544_FEC'],
                "200G-AUI4-AOC-ACC":['25G_RS_544_FEC'],
                "200GBase-KR4-PAM4":['25G_RS_544_FEC'],
                "200GBase-DR4":['25G_RS_544_FEC'],
                "200GBase-LR4":['25G_RS_544_FEC'],
                "200GBase-FR4":['25G_RS_544_FEC'],
                "200GBase-SR4":['25G_RS_544_FEC'],
                "200GBase-CR4-PAM4":['25G_RS_544_FEC'],
                "100G-AUI2":['25G_RS_544_FEC'],
                "100G-AUI2-AOC-ACC":['25G_RS_544_FEC'],
                "100G-CAUI2":['25G_RS_544_FEC'],
                "100G-CAUI2-AOC-ACC":['25G_RS_544_FEC'],
                "100GBase-KR2-PAM4":['25G_RS_544_FEC'],
                "100GBase-DR":['25G_RS_528_FEC'],
                "100GBase-SR2":['25G_RS_544_FEC'],
                "100GBase-CP2":['25G_RS_544_FEC'],
                "100GBase-KR-PAM4":['25G_RS_544_FEC'],
                "100GBase-CR-PAM4":['25G_RS_544_FEC'],
                "100G-AUI4":['25G_RS_544_FEC'],
                "100G-AUI4-AOC-ACC":['25G_RS_544_FEC'],
                "100G-CAUI4":['NO_FEC','25G_RS_528_FEC'],
                "100G-CAUI4-AOC-ACC":['NO_FEC','25G_RS_528_FEC'],
                "100GBase-KR4":['25G_RS_528_FEC'],
                "100GBase-LR4":['NO_FEC'],
                "100GBase-SR4":['25G_RS_528_FEC'],
                "100GBase-CR4":['25G_RS_528_FEC'],
                "50G-AUI1":['25G_RS_544_FEC'],
                "50G-AUI1-AOC-ACC":['25G_RS_544_FEC'],
                "50GBase-KR-PAM4":['25G_RS_544_FEC'],
                "50GBase-LR":['25G_RS_544_FEC'],
                "50GBase-FR":['25G_RS_544_FEC'],
                "50GBase-SR":['25G_RS_544_FEC'],
                "50GBase-CP":['25G_RS_544_FEC'],
                "50G-AUI2":['25G_RS_544_FEC'],
                "50G-AUI2-AOC-ACC":['25G_RS_544_FEC'],
                "50G-LAUI2":['NO_FEC'],
                "50G-LAUI2-AOC-ACC":['NO_FEC'],
                "50GBase-KR2":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "50GBase-LR2":['25G_RS_528_FEC'],
                "50GBase-SR2":['25G_RS_528_FEC'],
                "50GBase-CR2":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "40G-XLAUI":['NO_FEC'],
                "40G-XLAUI-AOC-ACC":['NO_FEC'],
                "40GBase-KR4":['NO_FEC','10G_KR_FEC'],
                "40GBase-LR4":['NO_FEC'],
                "40GBase-SR4":['NO_FEC'],
                "40GBase-CR4":['NO_FEC','10G_KR_FEC'],
                "25G-AUI-C2C":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25G-AUI-AOC-ACC":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-KR1":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-KR-S":['NO_FEC','25G_KR_FEC'],
                "25GBase-KR":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-LR":['25G_RS_528_FEC'],
                "25GBase-SR":['25G_RS_528_FEC'],
                "25GBase-CR1":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-CR-S":['NO_FEC','25G_KR_FEC'],
                "25GBase-CR":['NO_FEC','25G_KR_FEC','25G_RS_528_FEC'],
                "25GBase-T":['NO_FEC'],
                "10G-SFI-C2C":['NO_FEC'],
                "10G-SFI-AOC-ACC":['NO_FEC'],
                "10GBase-KR-CR1":['NO_FEC','10G_KR_FEC'],
                "10GBase-LR":['NO_FEC'],
                "10GBase-SR":['NO_FEC'],
                "10G-SFI-DA":['NO_FEC'],
                "10GBase-T":['NO_FEC'],
                "5GBase-KR":['NO_FEC'],
                "5GBase-T":['NO_FEC'],
                "2.5GBase-KX":['NO_FEC'],
                "2.5GBase-X":['NO_FEC'],
                "2.5GBase-T":['NO_FEC'],
                "1G-SGMII":['NO_FEC'],
                "1000Base-KX":['NO_FEC'],
                "1000Base-LX":['NO_FEC'],
                "1000Base-SX":['NO_FEC'],
                "1000Base-T":['NO_FEC'],
                "100Base-TX":['NO_FEC'],
                "100M-SGMII":['NO_FEC']}

    reset_type_dict = {"globr": "GLOBAL", "pfr": "PF", "corer": "CORE", "empr": "EMP", "flr": "FL", "pcir": "PCI","bmer": "BME", "vfr": "VF_SW", "vflr": "VFLR"}