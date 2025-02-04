import serial
import serial.tools.list_ports

class SCPIUARTScanner:
    def __init__(self, baudrate=115200, timeout=0.001, buffer_size=4096):
        self.baudrate = baudrate
        self.timeout = timeout
        self.buffer_size = buffer_size

    def scan_ports(self, expected_id: str):
        """
        Scans all available COM ports and sends *IDN? to identify the instrument.

        :param expected_id: The expected identifier string from the *IDN? response.
        :return: The COM port that matches the expected identifier, or None if not found.
        """
        ports = serial.tools.list_ports.comports()
        scan_result = []
        for port in ports:
            try:
                with serial.Serial(
                    port=port.device,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                ) as ser:
                    ser.write(b'*IDN?\n')
                    response = ser.read(self.buffer_size).decode().strip()
                    if expected_id in response:
                        print(f"Instrument found on {port.device}: {response}")
                        return port.device
                    else:
                        print(f"No matching instrument on {port.device}")
            except (serial.SerialException, UnicodeDecodeError) as e:
                print(f"Error on {port.device}: {e}")
        return None

if __name__ == "__main__":
    expected_id = "SPE6053"  # Replace with the expected identifier substring
    scanner = SCPIUARTScanner()
    matching_port = scanner.scan_ports(expected_id)
    if matching_port:
        print(f"Matching instrument found on: {matching_port}")
    else:
        print("No matching instrument found.")
