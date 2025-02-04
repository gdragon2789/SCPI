from SCPI.api.__init__ import *

class DG1022Z:
    def __init__(self, visa_port, connection_type):
        self.visa_port = visa_port
        self.connection_type = connection_type
        self.controller = None
        self.__connect()

    def __connect(self):
        if self.connection_type == "USB":
            self.controller = PYVISA_Controller(visa_port=self.visa_port,debug=True)
        elif self.connection_type == "TCP/IP":
            self.controller = TCPIP_Controller(ip_address=self.visa_port)
            self.__cls()
        elif self.connection_type == "Serial":
            self.controller = SERIAL_Controller(port=self.visa_port)
            self.__cls()

    def __cls(self):
        self.controller.write('*CLS')

if __name__ == '__main__':

    print('test')
    scanner = PyVISAScanner()
    connect_type, port = scanner.scan_for_instruments(expected_id="DG1022Z")

    instr = DG1022Z(visa_port=port, connection_type=connect_type)
    instr.controller.close()