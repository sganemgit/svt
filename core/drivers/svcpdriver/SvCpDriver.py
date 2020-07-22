import libPyMevCp
import os
import random
import textwrap
import libPyApi
import libSvPython
import libPyAdminqApi

from svdk.model.proxy import DriverProxy
from argparse import ArgumentParser

import struct
from ctypes import *
import threading
from ipacore.drivers.aq_descriptor import AqDescriptor
from ipacore.drivers.projectsspecificdata import ProjectsSpecificData

interrupted = False

MEVCP_OPCODES = {
    "MEVCP_OP_UNKNOWN": libPyMevCp.mevcp_op_unknown,
    "MEVCP_OP_VERSION": libPyMevCp.mevcp_op_version,
    "MEVCP_OP_CONFIG_TX_QUEUE": libPyMevCp.mevcp_op_config_tx_queue,
    "MEVCP_OP_CONFIG_RX_QUEUE": libPyMevCp.mevcp_op_config_rx_queue,
    "MEVCP_OP_CONFIG_IRQ_MAP": libPyMevCp.mevcp_op_config_irq_map,
    "MEVCP_OP_ENABLE_QUEUES": libPyMevCp.mevcp_op_enable_queues,
    "MEVCP_OP_DISABLE_QUEUES": libPyMevCp.mevcp_op_disable_queues,
    "MEVCP_OP_GET_STATS": libPyMevCp.mevcp_op_get_stats,
    "MEVCP_OP_CONFIG_RSS_KEY": libPyMevCp.mevcp_op_config_rss_key,
    "MEVCP_OP_CONFIG_RSS_LUT": libPyMevCp.mevcp_op_config_rss_lut,
    "MEVCP_OP_REQUEST_QUEUES": libPyMevCp.mevcp_op_request_queues,
    "MEVCP_OP_GET_CAPS": libPyMevCp.mevcp_op_get_caps,
    "MEVCP_OP_CREATE_VPORT": libPyMevCp.mevcp_op_create_vport,
    "MEVCP_OP_DESTROY_VPORT": libPyMevCp.mevcp_op_destroy_vport,
    "MEVCP_OP_ENABLE_VPORT": libPyMevCp.mevcp_op_enable_vport,
    "MEVCP_OP_DISABLE_VPORT": libPyMevCp.mevcp_op_disable_vport,
    "MEVCP_OP_CONFIG_TX_QUEUES": libPyMevCp.mevcp_op_config_tx_queues,
    "MEVCP_OP_CONFIG_RX_QUEUES": libPyMevCp.mevcp_op_config_rx_queues,
    "MEVCP_OP_ADD_QUEUES": libPyMevCp.mevcp_op_add_queues,
    "MEVCP_OP_DEL_QUEUES": libPyMevCp.mevcp_op_del_queues,
    "MEVCP_OP_MAP_VECTOR_QUEUE": libPyMevCp.mevcp_op_map_vector_queue,
    "MEVCP_OP_UNMAP_VECTOR_QUEUE": libPyMevCp.mevcp_op_unmap_vector_queue,
    "MEVCP_OP_MAP_VECTOR_ITR": libPyMevCp.mevcp_op_map_vector_itr,
    "MEVCP_OP_GET_RSS_KEY": libPyMevCp.mevcp_op_get_rss_key,
    "MEVCP_OP_CREATE_VFS": libPyMevCp.mevcp_op_create_vfs,
    "MEVCP_OP_DESTROY_VFS": libPyMevCp.mevcp_op_destroy_vfs
}

WB_MODE = {
    "DD_BIT": libPyApi.SV_DD_BIT_WB_MODE,
    "HEAD_WB": libPyApi.SV_HEAD_WB_MODE,
    "PUSH_MODE": libPyApi.SV_PUSH_MODE,
    "COMP_QUEUE": libPyApi.SV_COMPLETION_QUEUE_MODE
}

PACKET_TYPE = {
    "L2": libPyApi.PT_L2_DRIVER_PACKET,
    "IPV4": libPyApi.PT_TCP_IPV4,
    "IPV6": libPyApi.PT_TCP_IPV6,
    "UDPV4": libPyApi.PT_UDP_IPV4,
    "UDPV6": libPyApi.PT_UDP_IPV6
}

RING_STATE = {
    libPyApi.RING_STATE_DISABLED: "DISABLED",
    libPyApi.RING_STATE_IDLE: "IDLE",
    libPyApi.RING_STATE_WORKING: "WORKING",
    libPyApi.RING_STATE_STOPPED: "STOPPED",
    libPyApi.RING_STATE_NO_ACTIVITY: "NO_ACTIVITY",
    libPyApi.RING_STATE_DONE: "DONE",
    libPyApi.RING_STATE_HANG: "HANG"
}

DESC_TYPE = {
    "LEGACY": libPyApi.RXDT_LEGACY,
    "ADV_ONE_BUFFER": libPyApi.RXDT_ADV_ONE_BUFFER,
    "ADV_HDR_SPLIT": libPyApi.RXDT_ADV_HDR_SPLIT,
    "ADV_HDR_REPLIC": libPyApi.RXDT_ADV_HDR_REPLIC,
    "ADV_HDR_REPLIC_LONG": libPyApi.RXDT_ADV_HDR_REPLIC_LONG,
    "ADV_HDR_SPLIT_ALWAYS_USE_HEADER_BUFF": libPyApi.RXDT_ADV_HDR_SPLIT_ALWAYS_USE_HEADER_BUFF,
    "ADV_HDR_SPLIT_SMALL_LARGE": libPyApi.RXDT_ADV_HDR_SPLIT_SMALL_LARGE,
    "FLEX": libPyApi.RXDT_FLEX
}

DESC_SIZE = {
    16: libPyApi.RXDS_16_BYTES,
    32: libPyApi.RXDS_32_BYTES
}

OPERATION_MODE = {
    "DEFAULT": libPyApi.QOM_DEFAULT,
    "CC": libPyApi.QOM_CC,
    "SV": libPyApi.QOM_SV,
    "COMMS": libPyApi.QOM_COMMS,
    "NET": libPyApi.QOM_NET,
    "QAV": libPyApi.QOM_QAV,
    "SPLITQ": libPyApi.QOM_SPLITQ
}

MALICIOUS_MODE = {
    "NONE": libPyApi.MALICIOUS_NONE,
    "NO_EOP": libPyApi.MALICIOUS_NO_EOP,
    "TXADDR": libPyApi.MALICIOUS_TXADDR,
    "TXLEN": libPyApi.MALICIOUS_TXLEN
}

RESETS = {
    "PF": libPyApi.DRT_PF_RESET,
    "CORE": libPyApi.DRT_CORE_RESET,
    "GLOBAL": libPyApi.DRT_GLOBAL_RESET,
    "EMP": libPyApi.DRT_EMP_RESET,
    "BME": libPyApi.DRT_BME_RESET,
    "PCI": libPyApi.DRT_PCI_RESET,
    "FL": libPyApi.DRT_FL_RESET,
    "ACPI": libPyApi.DRT_ACPI_RESET,
    "VF_SW": libPyApi.DRT_VF_SW_RESET,
    "VFLR": libPyApi.DRT_VFLR_RESET,
    "PCI_RESTORE": libPyApi.DRT_PCI_RESET_RESTORE
}

AGENTS = {
    "default": libPyApi.IP_DEFAULT,
    "lan": libPyApi.IP_LAN,
    "ice": libPyApi.IP_ICE,
    "rdma": libPyApi.IP_RDMA,
    "fxp": libPyApi.IP_FXP,
    "hif": libPyApi.IP_HIF,
    "epl": libPyApi.IP_EPL
}


class SvCpDriver(object):
    """This class wrapps 'libSvPython' module (python wrapper for SV driver)"""

    def __init__(self, device_info):
        self._port_number = int(device_info.port_number)
        self._project_name = device_info.project_name
        self._device_number = device_info.device_number
        self._device_string = device_info.driver_specific_id
        self._dev_id = device_info.dev_id
        self._bdf_location = device_info.location

        # self._mdio_lock = None

        self._dp = None
        self._tx_ring = None
        self._tx_ring_status = None
        self._rx_ring = None
        self._rx_ring_status = None

        self._mdio_cntrl, self._mdio_data = ProjectsSpecificData.get_mdios_regs(self._project_name)
        if self._mdio_cntrl is None:
           raise ValueError('Missing data for MDIO registers for project ' + self._project_name)

        # create adapter handle
        self.create()

    def __del__(self):
        self._release()

    def set_additional_fields(self, **kwargs):
        self._mdio_lock = kwargs['mdio_locker']

    def port_number(self):
        '''
        This method return port number of current port.
        '''
        return self._port_number

    def device_number(self):
        '''
        This method return device number to which current port belongs.
        '''
        return self._device_number

    def get_version(self):
        device = self._device_string  # "mev1:0"
        version = True
        config_packet = False
        nsl_set = False
        nsl_get = False
        mbx_opcode = "MEVCP_OP_UNKNOWN"
        rc, cpf_ver_major, cpf_ver_minor = self.cpf_send(device, version, config_packet, nsl_set, nsl_get, mbx_opcode)

        if rc != 0:
            raise RuntimeError("cpf_send, status = %s" % (rc))
        return ("CP version: %d.%d" % (cpf_ver_major, cpf_ver_minor))

    def cpf_send(self, device, version, config_packet, nsl_set, nsl_get, mbx_opcode):
        """
        """
        dp = DriverProxy(device.split(":")[0], int(device.split(":")[1]))

        if mbx_opcode == "MEVCP_OP_VERSION" or version:
            cpf_ver = libPyMevCp.CpfVersion()
            cpf_ver.major = 0
            cpf_ver.minor = 0
            rc = self._dp.cpf().get_cpf_version(cpf_ver)
            print("CP version: %d.%d" % (cpf_ver.major, cpf_ver.minor))

            cpf_ver.major = 0
            cpf_ver.minor = 0

            rc = self._dp.cpf().get_cpf_ext_version(cpf_ver)

            print("CP sv_ext version: %d.%d" % (cpf_ver.major, cpf_ver.minor))
            return rc, cpf_ver.major, cpf_ver.minor

        if mbx_opcode == "MEVCP_OP_GET_CAPS":
            func_caps = libPyMevCp.MevFuncCapablities()
            func_caps.cap_flags = 0xffff
            rc = self._dp.cpf().get_func_capabilities(func_caps)
            print("func_caps.cap_flags: 0x%x" % (func_caps.cap_flags))
            print("func_caps.max_num_vfs: %d" % (func_caps.max_num_vfs))
            return rc

        if mbx_opcode == "MEVCP_OP_CREATE_VPORT":
            vport_msg = libPyMevCp.MevCreateVport()
            vport_msg.txq_model = 0  # libPyMevCp.VIRTCHNL_QUEUE_MODEL_SINGLE;
            vport_msg.rxq_model = 0  # libPyMevCp.VIRTCHNL_QUEUE_MODEL_SINGLE;
            vport_msg.vport_type = 0  # libPyMevCp.VIRTCHNL_VPORT_TYPE_DEFAULT;
            vport_msg.num_tx_q = 1
            vport_msg.num_rx_q = 1
            vport_msg.num_tx_complq = 0
            vport_msg.num_rx_bufq = 0
            vport_msg.num_vectors = 2
            rc = self._dp.cpf().create_vport(vport_msg)
            if rc != 0:
                raise RuntimeError("create_vport failed, status = %s" % (self._dp.driver_error_to_string(rc)))

            print("vport_msg.vport_id: 0x%x" % (vport_msg.vport_id))
            return rc

        if mbx_opcode == "MEVCP_OP_DESTROY_VPORT":
            vport_id = 0
            rc = self._dp.cpf().destroy_vport(vport_id)
            if rc != 0:
                raise RuntimeError("destroy_vport failed, status = %s" % (self._dp.driver_error_to_string(rc)))
            return rc

        if config_packet:
            opcode = 1
            context = 0
            rett = 0
            array = libPyApi.vector_uint8(128)
            self._dp.cpf().send_config_packet(opcode, context, array)

        nsl = self._dp.cpf().nsl()
        vsi_cfg = libPyMevCp.nsl_sem_vsi_cfg()

        if nsl_get:
            rc = nsl.nsl_sem_get_vsi(2, vsi_cfg)
            if rc != 0:
                raise RuntimeError("nsl_sem_get_vsi failed, status = %s" % (self._dp.driver_error_to_string(rc)))
            print("vsi_cfg.lem_epoch = %x" % vsi_cfg.lem_epoch)
            print("vsi_cfg.flags = %x" % vsi_cfg.flags)
            return rc

        if nsl_set:
            vsi_cfg.flags = 1
            vsi_cfg.pf_num = 8
            vsi_cfg.func_type = libPyMevCp.nsl_vsi_ftype_pf
            rc = nsl.nsl_sem_set_vsi(2, vsi_cfg)
            if rc != 0:
                raise RuntimeError("nsl_sem_set_vsi failed, status = %s" % (self._dp.driver_error_to_string(rc)))
            return rc

        return 0

    def get_device_info(self):
        return {'dev_id': self._dev_id, 'device_number': self._device_number, 'port_number': self._port_number,
                'bdf_location': self._bdf_location.get_location_string(), 'b': self._bdf_location.a,
                'd': self._bdf_location.b, 'f': self._bdf_location.c}

    def start_tx(self, packet_size=1024, packets_to_send=-1, skip_tx_ring_cfg=False):
        self._tx_ring = None
        '''
        This method starts TX on ring 0. Parameters can be passed in **kwargs dictionary
        as key-value pairs. List of parameters and their default values
        if not passed in **kwargs:
            'packet_size' - default value 512            
            'packets_to_send' - passed value -1 means infinite. Default value infinite            
        '''
        # packet_size = 512
        # packets_to_send = -1

        # if 'packet_size' in kwargs:
        #     packet_size = int(kwargs['packet_size'])
        # if 'packets_to_send' in kwargs:
        #     packets_to_send = int(kwargs['packets_to_send'])

        # skip_ring_cfg = False
        ringId = 0
        txringSize = 8160
        packet_type = "L2"
        wbmode = "DD_BIT"
        descsPerPacket = 1
        cqid = 0xffff
        cqsize = 1024
        cqtype = 1

        # dp = DriverProxy(self._device_string.split(":")[0], int(self._device_string.split(":")[1]))
        self._tx_ring_status = libPyApi.TxRingStatus()

        # get the tx_ring object
        self._tx_ring = self._dp.get_tx_ring(ringId)

        ring_cfg = libPyApi.TxRingConfiguration()

        ring_cfg.packet_size = packet_size
        ring_cfg.packet_type = PACKET_TYPE[packet_type]
        ring_cfg.descs_per_packet = descsPerPacket
        ring_cfg.ring_size = txringSize
        ring_cfg.wb_mode = WB_MODE[wbmode]
        ring_cfg.operation_mode = OPERATION_MODE["DEFAULT"]
        ring_cfg.cq_id = cqid

        if (cqsize != 1024) or (cqtype != 1):
            if cqid == 0xffff:
                cqid = ringId
            txcq = self._dp.create_tx_cq_ring()
            rc = txcq.configure_tx_cq_ring(cqid, cqsize, cqtype)
            if rc != 0:
                raise RuntimeError("configure TXCQ ring failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        if not skip_tx_ring_cfg:
            rc = self._tx_ring.configure_tx_ring_with_properties(ring_cfg)
            if rc != 0:
                raise RuntimeError("configure TX ring failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        # start sending packets
        if packets_to_send == -1:
            rc = self._tx_ring.start_tx_infinite()
        else:
            rc = self._tx_ring.start_tx(packets_to_send)
        # elif tx_time > 0:
        # rc = self._tx_ring.start_tx_time_limit(tx_time)

        if rc != 0:
            raise RuntimeError("start tx failed, status = %s" % (self._dp.driver_error_to_string(rc)))
        print("TX started")

    def stop_tx(self):
        '''
        This method stops TX on ring 0.
        '''

        if (self._tx_ring == None):
            return

        rc = self._tx_ring.stop_tx()

        if rc != 0:
            raise RuntimeError("stop tx failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        pass

    def get_tx_statistic(self):
        if (self._tx_ring_status is None):
            raise RuntimeError("get rx statistic failed, please call start TX first!!")

        rc = self._tx_ring.get_status(self._tx_ring_status)

        if rc != 0:
            raise RuntimeError("get status failed, status = %s" % (self._dp.driver_error_to_string(rc)))
        return self._tx_ring_status

    def start_rx(self, **kwargs):
        '''
        This method starts RX on ring 0.
        '''
        ring_num = 0

        self._rx_ring = self._dp.get_rx_ring(ring_num)
        self._rx_ring_status = libPyApi.RxRingStatus()
        desc_count = 128
        desc_type = "ADV_ONE_BUFFER"
        desc_size = 16
        buffer_size = 2048
        hdr_size = 128
        operation_mode = "DEFAULT"
        malicious_mode = "NONE"

        rp = libPyApi.RxRingProperties()

        rp.desc_count = desc_count
        rp.desc_type = DESC_TYPE[desc_type]
        rp.desc_size = DESC_SIZE[desc_size]
        rp.buffer_size = buffer_size
        rp.hdr_size = hdr_size
        rp.operation_mode = OPERATION_MODE[operation_mode]
        rp.srrctl_index = int("0xFFFF", 16)
        rp.malicious_mode = MALICIOUS_MODE[malicious_mode]
        rp.mirroring_replication = False

        # print "skip rx value:" + str(self.skip_rx_ring_cfg)
        # if skip_rx_ring_cfg == False:
        rc = self._rx_ring.configure_rx_ring(rp)
        if rc != 0:
            raise RuntimeError("configure RX ring failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        rc = self._rx_ring.start_rx()

        if rc != 0:
            raise RuntimeError("start RX failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        print("RX started")
        pass

    def stop_rx(self):
        '''
        This method stops RX on ring 0.
        '''
        if (self._rx_ring is None):
            print
            "Rx ring not set!!"
            return

        rc = self._rx_ring.stop_rx()

        if rc != 0:
            raise RuntimeError("stop rx failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        self._rx_ring_status = None
        pass

    def get_rx_statistic(self):
        if (self._rx_ring_status is None):
            raise RuntimeError("get rx statistic failed, please start RC first!!")

        rc = self._rx_ring.get_status(self._rx_ring_status)

        if rc != 0:
            raise RuntimeError("get status failed, status = %s" % (self._dp.driver_error_to_string(rc)))

        return self._rx_ring_status

    def print_ring_status(self, txFlag):
        """
        @param txFlag: if want tx ring status put True
        """
        # clear console before printing ring status
        os.system("clear")
        ring_num = 0

        rs = self._rx_ring_status
        if (txFlag is True):
            rs = self._tx_ring_status
            print("TX[%d] Status:" % (ring_num))
        else:
            print("RX[%d] Status:" % (ring_num))
        print("    State: %s" % (RING_STATE[rs.State]))
        print("    Packets: %s" % (rs.Counters.packets))
        print("    Descriptors: %s" % (rs.Counters.desc_passed))
        print("    Bytes: %s" % (rs.Counters.bytes))
        print("    Time: %sms" % (rs.Counters.milli_seconds))
        print("    Interrupts: %s" % (rs.Counters.interrupts))

        if rs.Counters.milli_seconds:
            print("    Throughput: %sbps" % (rs.Counters.bytes / rs.Counters.milli_seconds * 8000))

    def read_bar(self, address, bar=0, width=32):
        '''
        This method reads 32-bits pci register at offset specified
        in 'register_offset' and returns register value.
        '''
        mem = self._dp.mem()

        if (address is str):
            raise RuntimeError("Address cannot be a string")
        print()

        if width == 32:
            val = mem.read_bar(address, bar)[1]
            return val

        return mem.read_bar64(address, bar)[1]

    def write_bar(self, address, value, bar=0, width=32):
        '''
        This method writes value specified in 'write_value'
        to 32-bits pci register at offset specified in 'register_offset'.
        '''
        mem = self._dp.mem()

        print(bar)
        if (address is str):
            raise RuntimeError("Address cannot be a string")

        if (value is str):
            raise RuntimeError("Address value cannot be a string")

        if width == 32:
            return mem.write_bar_32(address, value, bar)
        pass

    def read_csr(self, address, agent="default", width=32):
        '''
        This method reads 32-bits csr register at offset specified
        in 'register_offset' and returns register value.
        '''
        if width == 32:
            return self._dp.csr(AGENTS[agent]).read(address)[1]

        return self._dp.csr(AGENTS[agent]).read_64(address)[1]

    def write_csr(self, address, value, agent="default", width=32):
        '''
        This method writes value specified in 'write_value'
        to 32-bits csr register at offset specified in 'register_offset'.
        '''
        if width == 32:
            return self._dp.csr(AGENTS[agent]).write(address, value)

        return self._dp.csr(AGENTS[agent]).write_64(address, value)

    def read_phy_register(self, page, register_offset, phy_add):
        '''
        This method reads phy register according to
        'page', 'register_offset' and 'phy_add' and returns register value.
        '''
        with self._mdio_lock:
            # key = threading.current_thread().getName()
            # print 'read mdio thread ' + key
            value = 0
            value = value | ((phy_add & 0x1f) << 21)  # set phy address
            value = value | ((page & 0x1F) << 16)  # set phy page
            value = value | (register_offset & 0xFFFF)  # set phy page
            value = value | 0x40000000  # set mdio cmd

            self.write_csr(self._mdio_cntrl, value)
            while self.read_csr(self._mdio_cntrl) & 0x40000000:
                pass

            # read cycle
            value = value | (0x3 << 26)  # set opcode to read operation
            value = value | 0x40000000  # set mdio cmd

            self.write_csr(self._mdio_cntrl, value)

            while self.read_csr(self._mdio_cntrl) & 0x40000000:
                pass

            value = self.read_csr(self._mdio_data)
            value = (value & 0xffff0000) >> 16
            # print 'finished reading medio thread ' + key
            return value

    def write_phy_register(self, page, register_offset, phy_add, write_value):
        '''
        This method writes value specified in 'write_value'
        to phy register according to 'page', 'register_offset' and 'phy_add'.
        '''
        with self._mdio_lock:
            # key = threading.current_thread().getName()
            # print 'writing mdio thread ' + key

            # address cycle

            value = 0
            value = value | ((phy_add & 0x1f) << 21)  # set phy address
            value = value | ((page & 0x1F) << 16)  # set phy page
            value = value | (register_offset & 0xFFFF)  # set phy page
            value = value | 0x40000000  # set mdio cmd

            self.write_csr(self._mdio_cntrl, value)
            while self.read_csr(self._mdio_cntrl) & 0x40000000:
                pass
            # write data register
            self.write_csr(self._mdio_data, (write_value & 0xFFFF))

            # write cycle
            value = value | (0x1 << 26)  # set opcode to read operation
            value = value | 0x40000000  # set mdio cmd

            self.write_csr(self._mdio_cntrl, value)

            while self.read_csr(self._mdio_cntrl) & 0x40000000:
                pass

                # print 'finished writing mdio thread ' + key


    def read_pci(self, register_offset):
        '''
        This method reads 32-bits pci register at offset specified
        in 'register_offset' and returns register value.
        '''

        pci = self._dp.create_pci_block()
        value = pci.read_dword(register_offset)
        return value[1]

    def write_pci(self, register_offset, write_value):
        '''
        This method writes value specified in 'write_value'
        to 32-bits pci register at offset specified in 'register_offset'.
        '''

        pci = self._dp.create_pci_block()
        pci.write_dword(register_offset, write_value)

    def tohex(val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def print_csr_value(self, value, width):
        """
        @description: print csr value in hex and bin format
        @param value: csr read value
        @param width: read width
        """
        # convert to binary value
        if width == 32:
            value_bin = "{0:032b}".format(int(str(value), 16))

        else:
            value_bin = "{0:064b}".format(int(str(value), 16))

        # print value in hex and bin
        print("value (hex): %s" % (tohex(value, width)))
        print("value (bin): %s" % (" ".join(textwrap.wrap(value_bin, 4))))

    def device_reset(self, reset_type):

        if reset_type not in RESETS.keys():
            raise RuntimeError("Unsupported reset type " + reset_type)

        rc = self._dp.cfg().reset_device(RESETS[reset_type])

        if rc:
            print("reset type: %s, failed (status = %s)" % (reset_type, hex(rc)))
        else:
            print("reset type: %s, done (status = %s)" % (reset_type, hex(rc)))

        return 0

    def send_aq_command(self, aq_descriptor, aq_buffer=None, debug_print=False):
        '''This function sends AQ command.
                    Arguments:
                        aq_descriptor - aq command data descriptor with following fields
                            opcode, flags, param0, param1, cookie_high, cookie_low, address_high, address_low, retval, datalen.
                            If one of these fields not set default value is 0.
                        aq_buffer - optional buffer for AQ. Refer to EAS for specific command, each value represents byte.
                                     If no buffer required pass None, default value is None.
        				debug_print - print AQ descriptor or not
                        Responsse from FW will be returned in these arguments.
                    Returns:
                        0 if aq command sent successfully, else error code
                '''



        aq = self._dp.create_admin_queue()
        desc = libPyAdminqApi.ControlQueueDescriptor()

        aq_buffer_size = 0
        sent_aq_buffer = None
        if aq_buffer is not None:
            aq_buffer_size = len(aq_buffer)
            sent_aq_buffer = libSvPython.ByteArray(aq_buffer_size)
            j = 0
            while j < aq_buffer_size:
                sent_aq_buffer[j] = aq_buffer[j]
                j += 1

        desc.flags = aq_descriptor.flags
        desc.opcode = aq_descriptor.opcode
        desc.param0 = aq_descriptor.param0
        desc.param1 = aq_descriptor.param1
        desc.retval = aq_descriptor.retval
        desc.datalen = aq_descriptor.datalen
        desc.cookie_low = aq_descriptor.cookie_low
        desc.cookie_high = aq_descriptor.cookie_high
        desc.addr_low = aq_descriptor.addr_low
        desc.addr_high = aq_descriptor.addr_high

        if debug_print:
            print 'AQ descriptor sent:'
            print aq_descriptor
            print

        ret_val = None
        ret_val = aq.admin_queue_send_command(desc, sent_aq_buffer, aq_buffer_size, True)

        if debug_print:
            print 'AQ descriptor received:'
            print aq_descriptor
            print

        aq_descriptor.flags = desc.flags
        aq_descriptor.opcode = desc.opcode
        aq_descriptor.param0 = desc.param0
        aq_descriptor.param1 = desc.param1
        aq_descriptor.retval = desc.retval
        aq_descriptor.datalen = desc.datalen
        aq_descriptor.cookie_low = desc.cookie_low
        aq_descriptor.cookie_high = desc.cookie_high
        aq_descriptor.addr_low = desc.addr_low
        aq_descriptor.addr_high = desc.addr_high

        if aq_buffer is not None:
            j = 0
            while j < aq_buffer_size:
                aq_buffer[j] = sent_aq_buffer[j]
                j += 1

        return 0 if ret_val is not None else 1

    def receive_aq_command(self, aq_descriptor, aq_buffer=None, debug_print=False):
        '''This function receives AQ command.
            Arguments:
                aq_descriptor - aq command data descriptor with following fields
                    opcode, flags, param0, param1, cookie_high, cookie_low, address_high, address_low, retval, datalen.
                    If one of these fields not set default value is 0.
            aq_buffer - optional buffer for AQ. Refer to EAS for specific command, each value represents byte.
                            If no buffer required pass None, default value is None.
            debug_print - print AQ descriptor or not
            Responsse from FW will be returned in these arguments.
            Returns:
                0 if aq command sent successfully, else error code
        '''
        desc_size = libSvPython.get_aq_descriptor_size()
        descriptor = libSvPython.ByteArray(desc_size)

        aq_buffer_size = 0
        sent_aq_buffer = None
        if aq_buffer is not None:
            aq_buffer_size = len(aq_buffer)
            s = struct.Struct('b' * aq_buffer_size)
            packed_s = s.pack(*aq_buffer)
            sent_aq_buffer = str(packed_s)

        descriptor[0] = aq_descriptor.flags & 0xff
        descriptor[1] = (aq_descriptor.flags >> 8) & 0xff
        descriptor[2] = aq_descriptor.opcode & 0xff
        descriptor[3] = (aq_descriptor.opcode >> 8) & 0xff
        descriptor[4] = aq_descriptor.datalen & 0xff
        descriptor[5] = (aq_descriptor.datalen >> 8) & 0xff
        descriptor[6] = aq_descriptor.retval & 0xff
        descriptor[7] = (aq_descriptor.retval >> 8) & 0xff
        descriptor[8] = aq_descriptor.cookie_high & 0xff
        descriptor[9] = (aq_descriptor.cookie_high >> 8) & 0xff
        descriptor[10] = (aq_descriptor.cookie_high >> 16) & 0xff
        descriptor[11] = (aq_descriptor.cookie_high >> 24) & 0xff
        descriptor[12] = aq_descriptor.cookie_low & 0xff
        descriptor[13] = (aq_descriptor.cookie_low >> 8) & 0xff
        descriptor[14] = (aq_descriptor.cookie_low >> 16) & 0xff
        descriptor[15] = (aq_descriptor.cookie_low >> 24) & 0xff
        descriptor[16] = aq_descriptor.param0 & 0xff
        descriptor[17] = (aq_descriptor.param0 >> 8) & 0xff
        descriptor[18] = (aq_descriptor.param0 >> 16) & 0xff
        descriptor[19] = (aq_descriptor.param0 >> 24) & 0xff
        descriptor[20] = aq_descriptor.param1 & 0xff
        descriptor[21] = (aq_descriptor.param1 >> 8) & 0xff
        descriptor[22] = (aq_descriptor.param1 >> 16) & 0xff
        descriptor[23] = (aq_descriptor.param1 >> 24) & 0xff
        descriptor[24] = aq_descriptor.addr_high & 0xff
        descriptor[25] = (aq_descriptor.addr_high >> 8) & 0xff
        descriptor[26] = (aq_descriptor.addr_high >> 16) & 0xff
        descriptor[27] = (aq_descriptor.addr_high >> 24) & 0xff
        descriptor[28] = aq_descriptor.addr_low & 0xff
        descriptor[29] = (aq_descriptor.addr_low >> 8) & 0xff
        descriptor[30] = (aq_descriptor.addr_low >> 16) & 0xff
        descriptor[31] = (aq_descriptor.addr_low >> 24) & 0xff

        if debug_print:
            print 'AQ descriptor sent:'
            for i in range(0, desc_size):
                print descriptor[i],
            print
            print 'Sent buffer:', sent_aq_buffer.__repr__()

        status = libSvPython.receive_adminqueue_command(self._device_string, descriptor, sent_aq_buffer,
                                                        aq_buffer_size)

        if debug_print:
            print 'AQ descriptor received:'
            for i in range(0, desc_size):
                print descriptor[i],
            print
            print 'Received buffer:', sent_aq_buffer.__repr__()

        aq_descriptor.flags = libSvPython.get_aq_descriptor_flags(descriptor)
        aq_descriptor.opcode = libSvPython.get_aq_descriptor_opcode(descriptor)
        aq_descriptor.param0 = libSvPython.get_aq_descriptor_param0(descriptor)
        aq_descriptor.param1 = libSvPython.get_aq_descriptor_param1(descriptor)
        aq_descriptor.retval = libSvPython.get_aq_descriptor_retval(descriptor)
        aq_descriptor.datalen = libSvPython.get_aq_descriptor_datalen(descriptor)
        aq_descriptor.cookie_low = libSvPython.get_aq_descriptor_coockie_low(descriptor)
        aq_descriptor.cookie_high = libSvPython.get_aq_descriptor_cookie_high(descriptor)
        aq_descriptor.addr_low = libSvPython.get_aq_descriptor_addr(descriptor, True)
        aq_descriptor.addr_high = libSvPython.get_aq_descriptor_addr(descriptor, False)

        if aq_buffer is not None:
            response_buffer = s.unpack(sent_aq_buffer)
            for i in range(0, len(response_buffer)):
                aq_buffer[i] = int(response_buffer[i])

        return status

    def create(self):
        ring_id = 0
        print self._device_string
        self._dp = DriverProxy(self._device_string.split(":")[0], int(self._device_string.split(":")[1]))
        self._tx_ring = self._dp.get_tx_ring(ring_id)
        self._rx_ring = self._dp.get_rx_ring(ring_id)
        if self._dp is None:
            raise RuntimeError(
                "Failed to init device {} device number {} port number {}, device not found".format(self._project_name,
                                                                                                    self._device_number,
                                                                                                    self._port_number))

    def _release(self):
        pass
