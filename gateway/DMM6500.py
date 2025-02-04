# socket_instrument.py
import time
from TCPIP import TCPIP_Controller
from SERIAL import SERIAL_Controller
from PyVISAScanner import PyVISAScanner

class DMM6500:
    def __init__(self, visa_port=None, connection_type=None):
        self.visa_port = visa_port
        self.connection_type = connection_type
        self.controller = None
        self.__connect()

    def __connect(self):
        if self.connection_type == "USB":
            pass
        elif self.connection_type == "TCP/IP":
            self.controller = TCPIP_Controller(ip_address=self.visa_port)
            self.__cls()
        elif self.connection_type == "Serial":
            self.controller = SERIAL_Controller(port=self.visa_port)
            self.__cls()


    def __cls(self):
        self.controller.write('*CLS')

    def write(self, command: str) -> None:
        self.controller.write(command)

    def query(self, command: str) -> str:
        return self.controller.query(command)

    def fetch(self, buffer_name="defbuffer1"):
        return self.controller.query(f':FETCh? "{buffer_name}"')

    def close(self):
        self.controller.close()

    def meas_vdc(self,meas_range='AUTO'):
        # cmd = r"[:SENSe[1]]:VOLTage[:DC]:RANGe: AUTO"
        cmd = "VOLT:DC:RANG:AUTO ON"
        # cmd = ":SENS:VOLT:DC:RANG AUTO"

        self.write(cmd)

        return self.query(":MEASure:VOLTage:DC?")

    def meas_idc(self,meas_range='AUTO'):
        # cmd = r"[:SENSe[1]]:VOLTage[:DC]:RANGe: AUTO"
        cmd = "CURR:DC:RANG:AUTO ON"
        # cmd = ":SENS:VOLT:DC:RANG AUTO"

        self.write(cmd)

        return self.query(":MEASure:CURRent:DC?")

    def meas_vac(self,meas_range='AUTO'):
        # cmd = r"[:SENSe[1]]:VOLTage[:DC]:RANGe: AUTO"
        cmd = "VOLT:AC:RANG:AUTO ON"
        # cmd = ":SENS:VOLT:DC:RANG AUTO"

        self.write(cmd)

        return self.query(":MEASure:VOLTage:AC?")

    def meas_2w(self,meas_range='AUTO'):
        cmd = "RES:RANG:AUTO ON"
        self.write(cmd)

        return self.query(":MEASure:RESistance?")

    def clear_trigger(self):
        scpi_instruction = {
            'cmd1': ':*RST',
        }
        for key, value in scpi_instruction.items():
            self.write(value)

    def trigger_mode(self):
        range_cmd = ":SENS:VOLT:DC:RANG 10"
        self.write(range_cmd)

        scpi_instruction = {
            'cmd1': ':*RST',
            'cmd2': ':TRIGger:LOAD "EMPTY"',
            'cmd3': ':TRIGger:BLOCk:BUFFer:CLE 1, "defbuffer1"',
            'cmd4': ':TRIGger:BLOCk:DELay:CONStant 2, 1e-3',
            'cmd5': ':TRIGger:BLOCk:MDIGitize 3, "defbuffer1", 1',
            'cmd6': ':TRIGger:BLOCk:BRANch:LIMit:CONStant 4, ABOVe, 0, 1.6, 1,3',
            'cmd7': ':TRIGger:BLOCk:MDIGitize 5, "defbuffer1", 1',
            'cmd8': ':TRIGger:BLOCk:BRANch:LIMit:CONStant 6, BELow, 1.5, 0, 0,5',
            'cmd9': ':INIT'
        }
        for key, value in scpi_instruction.items():
            self.write(value)

    def get_data_from_trigger_model(self):
        while True:
            data = self.query(':TRIGger:STATe?')
            print(data)# "IDLE;IDLE;6"
            results = data.split(sep=';')
            if results[0] == "IDLE" and results[1] == "IDLE" and results[2] == "6":
                return round(float(self.fetch()),3)
            time.sleep(0.001)







if __name__ == "__main__":
    scanner = PyVISAScanner()
    connect_type, port = scanner.scan_for_instruments(expected_id="DMM6500")

    instr = DMM6500(visa_port=port, connection_type=connect_type)

    cycle = 1000
    for i in range(cycle):
        instr.trigger_mode()
        result = instr.get_data_from_trigger_model()
        print(f"Lasted value: {result}")
        if result > 1.6:
            print(f"Failed at {i}")

            break
        time.sleep(1)
    print(f"Finish {cycle} cycle")
    instr.clear_trigger()

    # dcv = instr.meas_vdc()
    # print(f'Measured Voltage: {dcv}')
    # print(f'Fetch buffer: {instr.fetch()}')
    #
    # idc = instr.meas_idc()
    # print(f'Measured Current: {idc}')
    # print(f'Fetch buffer: {instr.fetch()}')

    # acv = instr.meas_vac()
    # print(f'Measured Voltage: {acv}')

    # resistance_2w = instr.meas_2w()
    # print(f'Measured Resistance: {resistance_2w}')
    # print(f'Fetch buffer: {instr.fetch()}')

    instr.close()
