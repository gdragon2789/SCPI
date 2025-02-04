# scpi_uart.py
from SCPI.api.__init__ import *


class SPE6053:
    def __init__(self, visa_port=None):
        self.visa_port = visa_port
        self.default_ovp = None
        self.default_ocp = None
        self.__get_default_status()

    def __get_default_status(self):
        self.default_ocp = float(self.visa_port.query(command="CURRent:LIMit?"))
        self.default_ovp = float(self.visa_port.query(command="VOLTage:LIMit?"))
        if self.visa_port.debug:
            print(f"Default OCP is set to: {self.default_ocp}A")
            print(f"Default OVP is set to: {self.default_ovp}V")

    def enable_output(self) -> None:
        cmd = "OUTPut ON"
        self.visa_port.write(command=cmd)
        while True:
            result = self.visa_port.query(command="OUTPut?")
            if result == "1" or result == "ON":
                break
            time.sleep(0.001)

    def disable_output(self) -> None:
        cmd = "OUTPut OFF"
        self.visa_port.write(command=cmd)
        while True:
            result = self.visa_port.query(command="OUTPut?")
            if result == "0" or result == "OFF":
                break
            time.sleep(0.001)

    def set_voltage(self, volt=0.0) -> None:
        if volt >= self.default_ovp:
            print("Voltage is higher than default OVP")
            print("Voltage reduced OVP - 1V")
            volt = volt - 1  # Default the OWON will set the voltage to default OVP - 1V

        cmd = f"VOLTage {volt}"
        verify = "VOLTage?"  # result is 5.000V less accurate 4.970V input
        # verify = "MEAS:VOLT:DC?" # result is 4.970V with more accuracy at 4.970V input
        self.visa_port.write(command=cmd)
        result = self.visa_port.query(command=verify)
        if self.visa_port.debug:
            print(f"Voltage is set to: {result}V")

    def set_over_voltage_protection(self, volt=0.0) -> None:
        cmd = f"VOLTage:LIMit {volt}"
        self.visa_port.write(command=cmd)
        result = self.visa_port.query(command="VOLTage:LIMit?")
        if self.visa_port.debug:
            print(f"OVP is set to: {result}V")
            if result == volt:
                print("OVP is set successfully")
            else:
                print("OVP is not set successfully")

    def set_current(self, curr=0.0) -> None:
        if curr >= self.default_ocp:
            print("Current is higher than default OCP")
            print("Current reduced OCP - 0.1A")
            curr = curr - 0.1  # Default the OWON will set the curent to default OCP - 0.1A

        cmd = f"CURRent {curr}"
        # verify = "CURRent?"
        verify = "MEASure:CURRent?"
        self.visa_port.write(command=cmd)
        result = self.visa_port.query(command=verify)
        if self.visa_port.debug:
            print(f"Current is set to: {result}A")

    def set_over_current_protection(self, curr=0.0) -> None:
        cmd = f"CURRent:LIMit {curr}"
        self.visa_port.write(command=cmd)
        result = self.visa_port.query(command="CURRent:LIMit?")
        if self.visa_port.debug:
            print(f"OCP is set to: {result}A")
            if result == curr:
                print("OCP is set successfully")
            else:
                print("OCP is not set successfully")

    def get_voltage(self) -> float:
        cmd = "MEAS:VOLT:DC?"
        result = self.visa_port.query(command=cmd)
        return float(result)

    def get_current(self) -> float:
        cmd = "MEAS:CURR:DC?"
        result = self.visa_port.query(command=cmd)
        return float(result)


if __name__ == "__main__":
    # Constants
    PERIOD = 2.000  # Total period in seconds
    ON_TIME = 1.000  # ON time in seconds

    scanner = PyVISAScanner()
    connect_type, port = scanner.scan_for_instruments(expected_id="SPE6053")
    print(f"SPE6053 found on {port}")
    SCPI_connection = SERIAL_Controller(port=port, debug=False)

    dcps = SPE6053(visa_port=SCPI_connection)
    dcps.disable_output()
    dcps.set_over_voltage_protection(volt=60.0)
    dcps.set_voltage(volt=1.0)
    dcps.set_current(curr=0.2)
    dcps.enable_output()

    # while True:
    #     dcps.set_voltage(volt=1.5)
    #     time.sleep(ON_TIME)
    #     off_time = PERIOD - ON_TIME
    #     dcps.set_voltage(volt=1.9)
    #     time.sleep(off_time)

    # print("Voltage set:",dcps.get_voltage())
    # print("Current set:",dcps.get_current())
    # instr.set_over_current_protection(curr=1)
    # instr.set_over_voltage_protection(volt=45)
    # Disconnect the visa_port
    dcps.visa_port.close()
