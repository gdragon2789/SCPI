from SCPI.api.__init__ import *


class DeviceConst(Enum):
    R_MIN_READING = 1
    R_MAX_READING = 10000
    SAMPle_MIN_COUNT = 1
    SAMPle_MAX_COUNT = 599999999
    DC_VOLTAGE_RANGE = (200 * 1e-3, 2, 20, 200, 1000, "AUTO")
    AC_VOLTAGE_RANGE = (200 * 1e-3, 2, 20, 200, 750, "AUTO")
    DC_CURRENT_RANGE = (200 * 1e-6, 2 * 1e-3, 20 * 1e-3, 200 * 1e-3, 2, 10, "AUTO")
    AC_CURRENT_RANGE = (20 * 1e-3, 200 * 1e-3, 2, 10, "AUTO")
    NPLC_RANGE = (0.3, 1, 10)
    RANGE_200uA = 200 * 1e-6
    RANGE_2mA = 2 * 1e-3
    RANGE_20mA = 20 * 1e-3
    RANGE_200mA = 200 * 1e-3
    RANGE_2A = 2
    RANGE_10A = 10
    RANGE_200mV = 200 * 1e-3
    RANGE_2V = 2
    RANGE_20V = 20
    RANGE_200V = 200
    RANGE_750V = 750
    RANGE_1000V = 1000
    RANGE_AUTO = "AUTO"
    FILTER_RANGE = (0, 1)


class SDM3055(VISA_INSTRUMENT):
    def __init__(self, visa_port=None, connection_type=None):
        super().__init__(visa_port, connection_type)
        self.controller._connection.timeout = 60000

    def abort(self) -> None:
        self.write(":ABORt")

    def fetch(self):
        return self.query(":FETCh?")

    def initiate(self):
        self.write(":INITiate:IMMediate")

    def output_trigger_slope(self, value="NEG"):
        cmd = f"OUTPut:TRIGger:SLOPe {value}"
        self.write(cmd)
        time.sleep(.001)

        result = self.query(":OUTPut:TRIGger:SLOPe?")
        if result == value:
            return True
        else:
            return False

    def r(self, max_reading: int = None):
        """
        :Purpose:
            Retrieves the last measured value
        :Timing:
            Immediate, no new trigger
        :Use Case
            When you need the last measurement without re-triggering the device
        :param max_reading:
        :return: The last measured value
        """
        if max_reading is None:
            return self.query(":R?")
        else:
            if self.validate_device_const(min_value=DeviceConst.R_MIN_READING.value,
                                          max_value=DeviceConst.R_MAX_READING.value,
                                          input_value=max_reading):
                return self.query(f":R? {max_reading}")

    def read(self):
        """
        :Purpose:
            Triggers a new measurement and returns it
        :Timing:
            Triggers a new measurement
        :Use Case
            When you need the latest measurement, triggering the device a new measurement.
        :return: The latest measurement
        """
        return self.query(":READ?")

    def sample(self, count: int = 1):
        if self.validate_device_const(min_value=DeviceConst.SAMPle_MIN_COUNT.value,
                                      max_value=DeviceConst.SAMPle_MAX_COUNT.value,
                                      input_value=count):
            self.write(f":SAMPle:COUNt {count}")
            time.sleep(0.001)
            result = int(self.query(":SAMPle:COUNt?"))
            if result == count:
                return True
            else:
                return False

    def get_device_mode(self):
        return self.query(":CONFigure?")

    def config_continuity(self):
        self.write(":CONFigure:CONTinuity")
        mode_selected = self.get_device_mode()
        if mode_selected == "CONT":
            return True
        else:
            return False

    def config_diode(self):
        self.write(":CONFigure:DIODe")
        mode_selected = self.get_device_mode()
        if mode_selected == "DIOD":
            return True
        else:
            return False

    def config_frequency(self):
        self.write(":CONFigure:FREQuency")
        mode_selected = self.get_device_mode()
        if mode_selected == "FREQ":
            return True
        else:
            return False

    def config_period(self):
        self.write(":CONFigure:PERiod")
        mode_selected = self.get_device_mode()
        if mode_selected == "PERi":
            return True
        else:
            return False

    def config_voltage_dc(self, range):
        if self.validate_device_const(list_range=DeviceConst.DC_VOLTAGE_RANGE.value, input_value=range):
            cmd = f"CONFigure:VOLTage:DC {range}"
            self.write(cmd)

    def config_current_dc(self, range):
        if self.validate_device_const(list_range=DeviceConst.DC_CURRENT_RANGE.value, input_value=range):
            cmd = f":CONFigure:CURRent:DC {range}"
            self.write(cmd)

    def config_current_ac(self, range):
        if self.validate_device_const(list_range=DeviceConst.AC_CURRENT_RANGE.value, input_value=range):
            cmd = f":CONFigure:CURRent:AC {range}"
            self.write(cmd)

    def resistance(self, range):
        pass

    def dc_voltage_nplc(self, nplc=None):
        if self.validate_device_const(list_range=DeviceConst.NPLC_RANGE.value, input_value=nplc):
            cmd = f"SENSe:VOLTage:DC:NPLC {nplc}"
            self.write(cmd)
            result = self.query("SENSe:VOLTage:DC:NPLC?")
            if result == nplc:
                return True
            else:
                return False

    def dc_voltage_filter(self, value=None):
        if self.validate_device_const(list_range=DeviceConst.FILTER_RANGE.value, input_value=value):
            cmd = f":SENSe:VOLTage:DC:FILTer:STATe {value}"
            self.write(cmd)
            result = self.query("SENSe:VOLTage:DC:FILTer:STATE?")
            if result == value:
                return True
            else:
                return False


class UNITTEST:
    def __init__(self, visa_port, connection_type):
        self.dmm = SDM3055(visa_port=visa_port, connection_type=connection_type)

    def config(self):
        self.dmm.dc_voltage_nplc(nplc=0.3)
        # self.dmm.config_voltage_dc(range=DeviceConst.RANGE_2V.value)
        self.dmm.sample(count=50)
        self.dmm.dc_voltage_filter(value=1)
        start = time.time()
        result = self.dmm.read()
        end = time.time()
        duration = end - start
        print(f"Duration: {duration}s")
        # Convert the string to a list of floats
        data_list = [float(value) for value in result.split(",")]

        print(data_list)
        print(f"Buffer length: {len(data_list)}")
        for i, data in enumerate(data_list):
            print(f"Buffer data {i}: {data}")
        self.dmm.abort()
        return data_list


if __name__ == '__main__':
    scanner = PyVISAScanner()
    # scanner.scan_instruments()
    # connect_type, port = scanner.scan_for_instruments(expected_id="SDM3055")

    hacked_port = "USB0::0xF4EC::0xEE38::SDM35GBC7R0208::INSTR"
    hacked_usb = "USB"

    test = UNITTEST(visa_port=hacked_port, connection_type=hacked_usb)

    import matplotlib.pyplot as plt


    data = test.config()  # Replace with your actual data

    # Create an x-axis based on the number of data points
    x = range(len(data))

    # Plot the graph
    plt.figure(figsize=(10, 5))
    plt.plot(x, data, label="Data Points")
    plt.title("Graph of Data Points")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.legend()
    plt.show()

    # instr = SDM3055(visa_port=port, connection_type=connect_type)
    # # print(instr.fetch())
    #
    # # instr.abort()
    # instr.cls()
    # instr.dc_voltage_nplc(nplc=0.3)
    # print(instr.meas_voltage_dc(range=DeviceConst.RANGE_2V.value))
    #
    # while True:
    #     print(instr.meas_voltage_dc(range=DeviceConst.RANGE_2V.value))
    #     time.sleep(0.1)
    # # instr.diode()
    # # instr.frequency()
    # # instr.period()
    #
    #
    #
    # # instr.current_dc(range=DeviceConst.RANGE_20mA.value)
    # # instr.current_ac(range=DeviceConst.RANGE_2A.value)
    #
    # # a = instr.get_device_mode()
    # # print(instr.get_device_mode())
    #
    # # instr.continuity()
    # # if instr.sample(count=5):
    # #     print(f"Buffer length: {len(instr.r())}")
    # #     print(instr.read())
    # #     # print(instr.r())
    # #     # print(instr.read())
    # #     instr.controller.close()
