# -*- coding: utf-8 -*-
from . import helpers
from . import constants as c
import serial



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

    def uart_sendpackage(self, data):
        self.uart.write(data)

    def uart_receive_package(self):
        status=[]
        data=[]
        return status, data

    def check_status(self):
        statue_code = None  
        return 
    
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
