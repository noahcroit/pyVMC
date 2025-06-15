# -*- coding: utf-8 -*-
from . import helpers
from . import constants as c
import serial
import time



class VMC:
    def __init__(self, port=None, 
                    baudrate=9600, 
                    bytesize=8, 
                    stopbits=1, 
                    parity=c.PARITY_NONE, 
                    timeout=1):
        self.uart = serial.Serial(
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout 
        )
        self.__temperature = 0
    
    def uart_reconfig(self, port=None,
                    baudrate=9600, 
                    bytesize=8, 
                    stopbits=1, 
                    parity=c.PARITY_NONE, 
                    timeout=1):
        self.uart.port = port 
        self.uart.baudrate = baudrate 
        self.uart.bytesize = bytesize
        self.uart.stopbits = stopbits
        self.uart.parity = parity
        self.uart.timeout = timeout
        if self.uart.port != None:
            self.uart.open()

    def uart_send_package(self, data):
        self.uart.write(data)

    def uart_receive_package(self):
        timeout_cnt = 100 * self.uart.timeout
        package_completed=False
        state=c.STATE_FIND_SOF
        dataframe = bytearray()
        
        # Find the SOF 
        while state == c.STATE_FIND_SOF:
            byte = self.uart.read(1)
            if not byte:
                timeout_cnt -= 1
            else:
                timeout_cnt=100
                if byte == c.BYTE_SOF:
                    dataframe.extend(byte)
                    state = c.STATE_FIND_LEN
            if timeout_cnt <= 0:
                return c.PACKAGE_ERROR, dataframe
            time.sleep(0.01)

        # Find the byte lenght
        byte = self.uart.read(1)
        dataframe.extend(byte)
        bytelen = byte[0]
        state = c.STATE_FIND_DATA

        # Find data(s)
        # It consists of CMD, ADDR, STATUS, Data
        byte = self.uart.read(bytelen)
        dataframe.extend(byte)
        state = c.STATE_FIND_EOF
        
        # Find the EOF
        byte = self.uart.read(1)
        if byte == c.BYTE_EOF:
            dataframe.extend(byte)
        else:
            return c.PACKAGE_ERROR, dataframe 
         
        return c.PACKAGE_OK, dataframe

    def poll_status(self, mac_addr=0x01) -> dict:
        # poll package setup
        b_sof = c.BYTE_SOF
        b_len = c.BYTE_LEN_POLL
        b_cmd = c.BYTE_CMD_POLL
        b_addr = bytes(mac_addr)
        b_status = b'\x00'
        b_data = bytes(c.BYTESIZE_DATA_POLL)
        b_eof = c.BYTE_EOF
        b_crc = c.BYTE_CRC
        packet = b_sof + b_len + b_cmd + b_addr + b_status + b_data + b_eof + b_crc
        # send poll
        self.uart_send_package(packet)
        # receive the response & extract the status data(s)
        ret, dataframe = self.uart_receive_package()
        if ret == c.PACKAGE_OK:
            print("dataframe", dataframe)
            # find the status
            status = dataframe[4]
            print("VMC Status=", status) 
            # find the temperature value
            self.__temperature = dataframe[5]
            # find the inventory status
            inv_status = dataframe[6 : 17]

            d_status = {
                "status": status,
                "inventory": inv_status
            }       
            return d_status
        else:
            return c.PACKAGE_ERROR

    def get_temperature(self) -> int:
        return self.__temperature
    
    def dispense(self):
        pass

    def is_dispense_done(self):
        pass



class TagIssuer(VMC):
    def __init__(self):
        super().__init__(port=None,
                    baudrate=9600, 
                    bytesize=8, 
                    stopbits=1, 
                    parity=c.PARITY_NONE, 
                    timeout=1
        )
        self.__slot_cnt = 0

    def release_slot(self, s : int) -> int:
        if not err:
            self.__slot_cnt += 1
            return self.__slot_cnt
        else:
            return -1
   
    def reset_count(self):
        self.__slot_cnt = 0
