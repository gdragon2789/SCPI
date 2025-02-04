from SCPI.api.__init__ import *


class DeviceConst(Enum):
    pass


class MSO2302A_S(VISA_INSTRUMENT):
    def __init__(self, visa_port=None, connection_type=None):
        super().__init__(visa_port, connection_type)
        self.acquire = self.ACQuire(self)

    def auto_scale(self):
        self.write(":AUToscale")

    def sys_auto_scale(self, value: int = 1):
        cmd = f":SYSTem:AUToscale {value}"
        self.write(cmd)
        time.sleep(0.001)
        result = float(self.query(f":SYSTem:AUToscale?"))
        if result == value:
            return True
        else:
            return False

    def clear(self):
        cmd = f":CLEar"
        self.write(cmd)

    def run(self):
        cmd = f":RUN"
        self.write(cmd)

    def stop(self):
        cmd = f":STOP"
        self.write(cmd)

    def single(self):
        cmd = f":SINGle"
        self.write(cmd)

    def tforce(self):
        cmd = f":TFORce"
        self.write(cmd)

    def tlhalf(self):
        cmd = f":TLHAlf"
        self.write(cmd)

    class ACQuire:
        def __init__(self, parent):
            self.parent = parent

        def AVERages(self, count: int = 2):
            cmd = f":ACQuire:AVERages {count}"
            self.parent.write(cmd)
            time.sleep(0.001)
            result = float(self.parent.query(":ACQuire:AVERages?"))
            if result == count:
                return True
            else:
                return False

        def is_AVERages(self):
            pass

    class BUS:
        def __init__(self):
            pass

    class CALCulate:
        def __init__(self):
            pass

    class CALibrate:
        def __init__(self):
            pass

    class CHANnel:
        def __init__(self):
            pass

    class CURSor:
        def __init__(self):
            pass

    class DISPlay:
        def __init__(self):
            pass

    class FUNCtion:
        def __init__(self):
            pass

    class LA:
        def __init__(self):
            pass

    class LAN:
        def __init__(self):
            pass

    class MASK:
        def __init__(self):
            pass

    class MEASure:
        def __init__(self):
            pass

    class OUTPut:
        def __init__(self):
            pass

    class RECall:
        def __init__(self):
            pass

    class REFerence:
        def __init__(self):
            pass

    class SAVE:
        def __init__(self):
            pass

    class TIMebase:
        def __init__(self):
            pass

    class TRACe:
        def __init__(self):
            pass

    class TRIGger:
        def __init__(self):
            pass

    class WAVeform:
        def __init__(self):
            pass


class UNITTEST:
    def __init__(self, visa_port, connection_type):
        self.device = MSO2302A_S(visa_port=visa_port, connection_type=connection_type)
        self.functions = self.list_functions()

    # Listing all functions of the class
    def list_functions(self):
        self.functions = [
            method
            for method in dir(self.device)
            if callable(getattr(self.device, method)) and not method.startswith("__")
        ]
        return self.functions

    def test_case_1(self):
        self.device.cls()
        self.device.rst()
        self.device.auto_scale()
        self.device.acquire.AVERages()


if __name__ == '__main__':
    scanner = PyVISAScanner()
    scanner.scan_instruments()
    connect_type, port = scanner.scan_for_instruments(expected_id="MSO2302A")

    # instr = MSO2302A_S(visa_port=port, connection_type=connect_type)
    # instr.auto_scale()
    # instr.controller.close()

    test = UNITTEST(visa_port=port, connection_type=connect_type)
    test.test_case_1()
