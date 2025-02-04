from SCPI.instrument.Digital_Multimeter.DMM6500 import *
from SCPI.instrument.Digital_Multimeter.SDM3055 import *

if __name__ == '__main__':
    scanner = PyVISAScanner()
    connect_type, port = scanner.scan_for_instruments(expected_id="DMM6500")

    instr = DMM6500(visa_port=port, connection_type=connect_type)