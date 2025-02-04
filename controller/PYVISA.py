import time

import pyvisa


class PYVISA_Controller:
    def __init__(self,
                 visa_port,
                 debug=False):
        self.visa_port = visa_port
        self._resource_manager = pyvisa.ResourceManager()
        self._connection = self._resource_manager.open_resource(resource_name=self.visa_port)
        self._idn = None
        self.debug = debug

        idn = self.query("*IDN?")
        if idn:
            self._idn = idn
            if self.debug:
                print(f"Connected to {idn} on port {visa_port}.")

    def write(self, command):
        self._connection.write(command)
        time.sleep(0.001)

    def query(self, command):
        result = self._connection.query(command).strip()
        time.sleep(0.01)
        return result

    def cls(self) -> None:
        self.write("*CLS")

    def rst(self):
        self.write("*RST")

    def opc(self) -> bool:
        return self.query("*OPC?").lower() == "1"

    def close(self) -> None:
        """Closes PyVISA connection."""
        self._connection.close()
        # if self._connection:
        #     self._connection.close()

    @property
    def idn(self):
        return self._idn
