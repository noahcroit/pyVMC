# -*- coding: utf-8 -*-
from .context import vmc
import time
import unittest



class TestVMC(unittest.TestCase):
    def test_vmc_uart_init(self):
        print("Test VMC UART init")
        # In default when create VMC instance, UART port is None, closed.
        vmc_test = vmc.core.VMC()
        self.assertEqual(vmc_test.uart.port, None)
        self.assertEqual(vmc_test.uart.is_open, False)

        # Initialize with parameters
        # Must connect the USB-to-Serial Converter
        serialport="/dev/ttyUSB0"
        vmc_test = vmc.core.VMC(port=serialport,
                                baudrate=9600,
                                bytesize=8,
                                stopbits=1,
                                parity=vmc.constants.PARITY_NONE,
                                timeout=5
        )
        self.assertEqual(vmc_test.uart.port, serialport)
        self.assertEqual(vmc_test.uart.is_open, True)

    def test_vmc_uart_reconfig(self):
        print("Test VMC UART reconfig")
        vmc_test = vmc.core.VMC()
        port1=vmc_test.uart.port
        baud1=vmc_test.uart.baudrate
        # reconfig
        vmc_test.uart_reconfig(port="/dev/ttyUSB0", baudrate=115200)
        port2=vmc_test.uart.port
        baud2=vmc_test.uart.baudrate
        # compare the old config with the new config
        self.assertNotEqual(port1, port2)
        self.assertNotEqual(baud1, baud2)

    def test_poll_status(self):
        print("Test sending poll package")
        vmc_test = vmc.core.VMC()
        vmc_test.uart_reconfig(port="/dev/ttyUSB0",
                                baudrate=9600,
                                bytesize=8,
                                stopbits=1,
                                parity=vmc.constants.PARITY_NONE
        )
        ret = vmc_test.poll_status()
        status = ret["status"]
        inv = ret["inventory"]
        print("returned poll status=", status, ", inventory=", inv)
        self.assertNotEqual(status, vmc.constants.PACKAGE_ERROR)
    
if __name__ == '__main__':
    #print("test basic")
    unittest.main()
