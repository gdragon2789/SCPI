# Virtual instrument software architecture
import time
from enum import Enum
from SCPI.controller.__init__ import *


class DeviceConst(Enum):
    STANDARD_EVENT_STATUS_REGISTER_WEIGHTS = (1, 2, 4, 8, 16, 32, 64, 128)


class VISA_INSTRUMENT:
    def __init__(self, visa_port=None, connection_type=None):
        self.visa_port = visa_port
        self.connection_type = connection_type
        self.controller = None
        self.__connect()

    def __connect(self):
        if self.connection_type == "USB":
            self.controller = PYVISA_Controller(visa_port=self.visa_port, debug=True)
            self.cc_cls()
        elif self.connection_type == "TCP/IP":
            self.controller = TCPIP_Controller(ip_address=self.visa_port, debug=False)
            self.cc_cls()
        elif self.connection_type == "Serial":
            self.controller = SERIAL_Controller(port=self.visa_port, debug=True)
            self.cc_cls()

    def write(self, command: str) -> None:
        self.controller.write(command)

    def query(self, command: str) -> str:
        return self.controller.query(command)

    def close(self):
        self.controller.close()

    # IEEE 488.2 Common Commands
    def cc_cls(self) -> None:
        cmd = f"*CLS"
        self.controller.write(cmd)

    def cc_ese(self, mask: int = 0):
        if self.is_valid_combination(input_value=mask,
                                     list_range=DeviceConst.STANDARD_EVENT_STATUS_REGISTER_WEIGHTS.value):
            cmd = f":*ESE {mask}"
            self.controller.write(cmd)
            time.sleep(0.001)
            result = int(self.controller.query("*ESE?"))
            if result == mask:
                return True
            else:
                return False

    def cc_esr(self):
        cmd = f"*ESR?"
        return self.query(cmd)

    def cc_opc(self) -> bool:
        cmd = f"*OPC?"
        return self.controller.query(cmd).lower() == "1"

    def cc_rst(self):
        cmd = f"*RST"
        self.controller.write(cmd)

    def cc_sre(self, mask: int = 0):
        if self.is_valid_combination(input_value=mask,
                                     list_range=DeviceConst.STANDARD_EVENT_STATUS_REGISTER_WEIGHTS.value):
            cmd = f"*SRE {mask}"
            self.write(cmd)
            time.sleep(0.001)
            result = int(self.query("*SRE?"))
            if result == mask:
                return True
            else:
                return False

    def cc_stb(self):
        """
        Query the condition register for the state byte register set.
        :return:
        |Bit|Weights|Name|Enable
        |7|128|OPER|Operation Status Reg
        |6|64||Not Used

        """
        return self.query(f"*STB?")

    def cc_tst(self):
        """
        Perform a self-test and query the result.
        :return: 0 if Pass else 1 if Fail
        """
        return self.query(f"*TST?")

    def template_command(self, param=None) -> None:
        """
        Brief:
            -   This command returns the instrument to the setup that was saved with the *SAV command.
        Details:
            -   Restores the state of the instrument from a copy of user-saved settings that are stored in setup
            memory. The settings are saved using the *SAV command.

            -   If you view the user-saved settings from the front panel of the instrument, these are stored as scripts
            named Setup0<n>.
        Example:
            -   CMD: *RCL 3
        :return: None
        """
        # Enum information about the command, specified for each instrument.
        cmd = "ROOT.SET_RCL.value.format(param=user_setup)"
        self.write(command=cmd)

    def template_query(self,
                       param1=None,
                       param2=None) -> str:
        """
        Brief:
            -   This command requests the latest reading from a reading buffer.
        Details:
            -   This command requests the last available reading from a reading buffer. If you send this command
            more than once and there are no new readings, the returned values are the same. If the reading
            buffer is empty, an error is returned.
        Example:
            -   CMD: :FETCh? "defbuffer1",  READing
        :return: string
        """
        # Enum information about the command, specified for each instrument.
        cmd = "ROOT.GET_FETCh.value.format(bufferName=param1, bufferElements=param2)"
        return self.query(command=cmd)

    # Utility function
    @staticmethod
    def validate_device_const(**kwargs) -> bool:
        if len(kwargs) == 3:
            if kwargs["min_value"] <= kwargs["input_value"] <= kwargs["max_value"]:
                print("Valid arguments")
                return True
            else:
                return False
        elif len(kwargs) == 2:
            if kwargs["input_value"] in kwargs["list_range"]:
                return True
            else:
                raise ValueError(f"{kwargs["input_value"]:.6f} not exit in {kwargs["list_range"]}")

    @staticmethod
    def is_valid_combination(input_value, list_range):
        # The maximum possible sum from the weights
        max_sum = sum(list_range)

        # Validate the input is a positive integer and within the range [0, max_sum]
        if not isinstance(input_value, int) or input_value < 0 or input_value > max_sum:
            raise ValueError(f"Number {input_value} is not a positive integer within the range (0-{max_sum}).")

        # Sort the list_range in descending order to start with the largest weight
        for weight in sorted(list_range, reverse=True):
            print(f"Checking weight: {weight}, current value: {input_value}")  # Debugging line
            if input_value >= weight:
                input_value -= weight  # Subtract the weight from the input value if possible
                print(f"After subtracting weight {weight}, new value: {input_value}")  # Debugging line

        # If input_value is reduced to 0, it's a valid combination
        if input_value == 0:
            return True
        else:
            raise ValueError(f"Number {input_value} is not the sum of the binary weights in {list_range}.")
