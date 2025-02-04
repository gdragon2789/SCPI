import time
from enum import Enum
from PYVISA import PYVISA_Controller
from PyVISAScanner import PyVISAScanner


class DeviceConst(Enum):
    Hz = 1
    kHz = 1e3
    MHz = 1e6
    GHz = 1e9
    VALID_FREQ_LL = 0
    VALID_FREQ_HL = 3.2 * 1e9
    VALID_BW_LL = 10
    VALID_BW_HL = 1e6
    TRACE_AVG_LL = 1
    TRACE_AVG_HL = 1000
    OBW_PERCENT_LL = 1.00
    OBW_PERCENT_HL = 99.99
    POWER_ATTENUATION_LL = 0
    POWER_ATTENUATION_HL = 30
    REFERENCE_LEVEL_LL = -100
    REFERENCE_LEVEL_HL = 20
    REFERENCE_LEVEL_OFFSET_LL = -300
    REFERENCE_LEVEL_OFFSET_HL = 300
    AMPLITUDE_SCALE_DIV_LL = 0.1
    AMPLITUDE_SCALE_DIV_HL = 20
    MARKER_NUMBER_LL = 1
    MARKER_NUMBER_HL = 4


class DSA832E:
    def __init__(self, visa_port=None, connection_type=None):
        self.visa_port = visa_port
        self.connection_type = connection_type
        self.controller = None
        self.__connect()

    def __connect(self):
        if self.connection_type == "USB":
            self.controller = PYVISA_Controller(visa_port=self.visa_port, debug=True)
            self.__cls()
        else:
            raise ValueError("Invalid connection type")

    # IEEE 488.2 CC
    def __cls(self):
        self.controller.cls()

    def rst(self):
        self.controller.rst()

    def close(self):
        self.controller.close()

    def write(self, command: str) -> None:
        self.controller.write(command)

    def query(self, command: str) -> str:
        return self.controller.query(command)

    def abort(self) -> None:
        self.write(":ABORt")

    def opc(self) -> bool:
        return self.controller.opc()

    def last_err(self):
        return self.query(":SYSTem:ERRor:NEXT?")

    def freq_center(self, value=None, unit:DeviceConst=None):
        short_value = value * unit.value
        if DeviceConst.VALID_FREQ_LL.value <= short_value <= DeviceConst.VALID_FREQ_HL.value:
            cmd = f":SENSe:FREQuency:CENTer {short_value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":SENSe:FREQuency:CENTer?"))
            if result == short_value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (0Hz - 3.2GHz)")

    def freq_span(self, value=None, unit=None):
        short_value = value * unit.value
        if DeviceConst.VALID_FREQ_LL.value <= short_value <= DeviceConst.VALID_FREQ_HL.value:
            cmd = f":SENSe:FREQuency:SPAN {short_value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":SENSe:FREQuency:SPAN?"))
            if result == short_value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (0Hz - 3.2GHz)")

    def freq_avg_time(self, value: int = None):
        if DeviceConst.TRACE_AVG_LL.value <= value <= DeviceConst.TRACE_AVG_HL.value:
            cmd = f":TRACe:AVERage:COUNt {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = int(self.query(":TRACe:AVERage:COUNt?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (1 - 1000)")

    def resolution_bandwidth(self, value=None, unit=None):
        def valid_range(raw_value):
            if raw_value <= 0:
                return False

            while raw_value > 1:
                if raw_value % 10 == 0:
                    raw_value /= 10
                elif raw_value % 3 == 0:
                    raw_value /= 3
                else:
                    return False
            return True

        short_value = value * unit.value
        if valid_range(short_value):
            if DeviceConst.VALID_BW_LL.value <= short_value <= DeviceConst.VALID_BW_HL.value:
                cmd = f":SENSe:BANDwidth:RESolution {short_value}"
                self.write(cmd)
                time.sleep(0.001)
                result = float(self.query(":SENSe:BANDwidth:RESolution?"))
                if result == short_value:
                    return True
                else:
                    return False
            else:
                raise ValueError("value out specs of the device (10Hz - 1MHz)")
        else:
            raise ValueError("value out step of Logarithmic Progression (1 - 3 - 10)")

    def detector_at_pos_peak(self):
        cmd = ":SENSe:DETector:FUNCtion POSitive"
        self.write(cmd)
        time.sleep(0.001)
        if self.query(":SENSe:DETector:FUNCtion?") == "POS":
            return True
        else:
            return False

    def continuous_peak_marker(self):
        cmd = ":CALCulate:MARKer1:CPEak:STATe 1"
        self.write(cmd)
        time.sleep(0.001)
        if self.query(":CALCulate:MARKer1:CPEak:STATe?") == "1":
            return True
        else:
            return False

    def measure_fctn_obw(self):
        """ Set the spectrum analyzer to the occupied bandwidth measurement state."""
        cmd = ":CONFigure:OBWidth"
        self.write(cmd)
        time.sleep(0.001)
        if self.query(":CONFigure?") == "OBW":
            return True
        else:
            return False

    def set_obw_span(self, value=None, unit:DeviceConst=None):
        short_value = value * unit.value
        if DeviceConst.VALID_FREQ_LL.value <= short_value <= DeviceConst.VALID_FREQ_HL.value:
            cmd = f":SENSe:OBWidth:FREQuency:SPAN {short_value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":SENSe:OBWidth:FREQuency:SPAN?"))
            if result == short_value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (0Hz - 3.2GHz)")

    def set_obw_percent(self,value:float = None):
        if DeviceConst.OBW_PERCENT_LL.value <= value <=DeviceConst.OBW_PERCENT_HL.value:
            cmd = f":SENSe:OBWidth:PERCent {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":SENSe:OBWidth:PERCent?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (1 - 99.99%)")

    def set_input_attenuation(self,value:int=None):
        if DeviceConst.POWER_ATTENUATION_LL.value <= value <= DeviceConst.POWER_ATTENUATION_HL.value:
            cmd = f":SENSe:POWer:RF:ATTenuation {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = int(self.query(":SENSe:POWer:RF:ATTenuation?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (0 - 30dB)")

    def set_ref_level_offset(self,value:int=None):
        if DeviceConst.REFERENCE_LEVEL_OFFSET_LL.value <= value <= DeviceConst.REFERENCE_LEVEL_OFFSET_HL.value:
            cmd = f":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel:OFFSet {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel:OFFSet?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (-300 - 300dB)")

    def set_ref_level(self,value:int=None):
        if DeviceConst.REFERENCE_LEVEL_LL.value <= value <= DeviceConst.REFERENCE_LEVEL_HL.value:
            cmd = f":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":DISPlay:WINdow:TRACe:Y:SCALe:RLEVel?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (-100 - 20dBm)")

    def set_scale_div(self,value:float=None):
        if DeviceConst.AMPLITUDE_SCALE_DIV_LL.value <= value <= DeviceConst.AMPLITUDE_SCALE_DIV_HL.value:
            cmd = f":DISPlay:WINdow:TRACe:Y:SCALe:PDIVision {value}"
            self.write(cmd)
            time.sleep(0.001)
            result = float(self.query(":DISPlay:WINdow:TRACe:Y:SCALe:PDIVision?"))
            if result == value:
                return True
            else:
                return False
        else:
            raise ValueError("value out specs of the device (0.1 - 20dB)")


    def __set_marker_readout(self,marker:int=1,mode="FREQuency"):
        cmd = f":CALCulate:MARKer{marker}:X:READout {mode}"
        self.write(cmd)
        time.sleep(0.001)
        result = self.query(f":CALCulate:MARKer{marker}:X:READout?")
        if result == mode[:4]:
            return True
        else:
            return False

    def read_marker(self, marker:int=1):
        self.__set_marker_readout()
        if DeviceConst.MARKER_NUMBER_LL.value <= marker <= DeviceConst.MARKER_NUMBER_HL.value:
            cmd = f":CALCulate:MARKer{marker}:X?"
            result = self.query(cmd)

            return int(result)
        else:
            raise ValueError("value out specs of the device (1 - 4)")

    def read_occupied_bandwidth(self):
        cmd = f":FETCh:OBWidth:OBWidth?"
        result = self.query(cmd)
        if result == "---":
            return 0
        return float(result)



class IRT3_SPECTRUM_ANALYZER_SETUP:
    def __init__(self):
        self.scanner = PyVISAScanner()
        self.connect_type, self.connect_port = self.scanner.scan_for_instruments(expected_id="DSA832E")
        self.instrument = DSA832E(visa_port=self.connect_port, connection_type=self.connect_type)

    def frequency_calibration_setup(self):
        def frequency_center():
            return self.instrument.freq_center(value=3, unit=DeviceConst.MHz)

        def frequency_span():
            return self.instrument.freq_span(value=2, unit=DeviceConst.MHz)

        def resolution_bandwidth():
            return self.instrument.resolution_bandwidth(value=3, unit=DeviceConst.kHz)

        def detector_at_pos_peak():
            return self.instrument.detector_at_pos_peak()

        def continuous_peak_marker():
            return self.instrument.continuous_peak_marker()

        def freq_avg_time():
            return self.instrument.freq_avg_time(value=100)

        def set_input_attenuation():
            return self.instrument.set_input_attenuation(value=30)

        def set_ref_level():
            return self.instrument.set_ref_level(value=20)

        def set_scale_div():
            return self.instrument.set_scale_div(value=20)

        results = []
        list_of_setup = {
            "set_input_attenuation": set_input_attenuation,
            "set_ref_level": set_ref_level,
            "set_scale_div": set_scale_div,
            "freq_span": frequency_span,
            "resolution": resolution_bandwidth,
            "detector": detector_at_pos_peak,
            "marker": continuous_peak_marker,
            "avg": freq_avg_time,
            "freq_center": frequency_center,
        }
        self.instrument.rst()
        for step_name,setup in list_of_setup.items():
            step_result = setup()
            print(f"{step_name}: {step_result}")
            results.append(step_result)
            time.sleep(0.01)
        # self.instrument.close()
        if len(results) == len(list_of_setup) and all(results):
            return True
        else:
            return False

    def deviation_calibration_setup(self):
        def frequency_span():
            return self.instrument.freq_span(value=200, unit=DeviceConst.kHz)

        def measure_fctn_obw():
            return self.instrument.measure_fctn_obw()

        def set_obw_span():
            return self.instrument.set_obw_span(value=200,unit=DeviceConst.kHz)

        def set_obw_percent():
            return self.instrument.set_obw_percent(value=90.00)

        def freq_avg_time():
            return self.instrument.freq_avg_time(value=100)

        def resolution_bandwidth():
            return self.instrument.resolution_bandwidth(value=1, unit=DeviceConst.kHz)

        def frequency_center():
            return self.instrument.freq_center(value=2.3, unit=DeviceConst.MHz)

        def set_input_attenuation():
            return self.instrument.set_input_attenuation(value=20)

        def set_ref_level():
            return self.instrument.set_ref_level(value=0)

        def set_scale_div():
            return self.instrument.set_scale_div(value=10)

        results = []
        list_of_setup = {
            "set_scale_div":set_scale_div,
            "set_input_attenuation": set_input_attenuation,
            "set_ref_level": set_ref_level,
            "freq_span": frequency_span,
            "measure_fctn_obw": measure_fctn_obw,
            "set_obw_span": set_obw_span,
            "set_obw_percent": set_obw_percent,
            "freq_avg_time": freq_avg_time,
            "resolution_bandwidth": resolution_bandwidth,
            "frequency_center": frequency_center,
        }
        # self.instrument.rst()
        for step_name,setup in list_of_setup.items():
            step_result = setup()
            print(f"{step_name}: {step_result}")
            results.append(step_result)
        # self.instrument.close()
        if len(results) == len(list_of_setup) and all(results):
            return True
        else:
            return False



if __name__ == '__main__':
    spectrum = IRT3_SPECTRUM_ANALYZER_SETUP()
    spectrum.instrument.rst()
    res = spectrum.frequency_calibration_setup()
    print(f"Frequency Calibration Setup?: {res}")
    step_1 = spectrum.instrument.read_marker()
    print(f"Frequency Calibration step 1: {step_1}")
    step_2 = spectrum.instrument.read_marker()
    print(f"Frequency Calibration step 2: {step_2}")
    step_3 = spectrum.instrument.read_marker()
    print(f"Frequency Calibration step 3: {step_3}")
    step_4 = spectrum.instrument.read_marker()
    print(f"Frequency Calibration step 4: {step_4}")



    # res = spectrum.deviation_calibration_setup()
    # print(f"Deviation Calibration?: {res}")
    # while True:
    #     step_5 = spectrum.instrument.read_occupied_bandwidth()
    #     print(f"Deviation Calibration step 5: {step_5}")
    #     time.sleep(0.01)
    #     if 97000 <= step_5 <= 99000:
    #         print(f"Deviation Calibration step 5 Done: {step_5}")
    #         break
    #
    # spectrum.instrument.freq_center(value=2.8, unit=DeviceConst.MHz)
    # while True:
    #     step_6 = spectrum.instrument.read_occupied_bandwidth()
    #     print(f"Deviation Calibration step 6: {step_6}")
    #     time.sleep(0.01)
    #     if 97000 <= step_6 <= 99000:
    #         print(f"Deviation Calibration step 6 Done: {step_6}")
    #         break
    #
    # spectrum.instrument.freq_center(value=3.3, unit=DeviceConst.MHz)
    # while True:
    #     step_7 = spectrum.instrument.read_occupied_bandwidth()
    #     print(f"Deviation Calibration step 7: {step_7}")
    #     time.sleep(0.01)
    #     if 97000 <= step_7 <= 99000:
    #         print(f"Deviation Calibration step 7 Done: {step_7}")
    #         break
    #
    # spectrum.instrument.freq_center(value=3.8, unit=DeviceConst.MHz)
    # while True:
    #     step_8 = spectrum.instrument.read_occupied_bandwidth()
    #     print(f"Deviation Calibration step 8: {step_8}")
    #     time.sleep(0.01)
    #     if 97000 <= step_8 <= 99000:
    #         print(f"Deviation Calibration step 8 Done: {step_7}")
    #         break

    print(spectrum.instrument.last_err())
    # spectrum.instrument.close()