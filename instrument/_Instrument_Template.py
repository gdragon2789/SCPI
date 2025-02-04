from SCPI.api.__init__ import *

class DeviceConst(Enum):
    pass

class INSTRUMENT_NAME(VISA_INSTRUMENT):
    def __init__(self, visa_port=None, connection_type=None):
        super().__init__(visa_port, connection_type)


if __name__ == '__main__':
    scanner = PyVISAScanner()
    scanner.scan_instruments()
    connect_type, port = scanner.scan_for_instruments(expected_id="INSTRUMENT_NAME")

    instr = INSTRUMENT_NAME(visa_port=port, connection_type=connect_type)
    instr.controller.close()