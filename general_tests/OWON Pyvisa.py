import pyvisa

# Initialize the PyVISA Resource Manager
rm = pyvisa.ResourceManager()

# Connect to the OWON SPE6053 via the serial port
# 'ASRL39::INSTR' is the resource string for the serial port connection
instrument = rm.open_resource('ASRL39::INSTR')

# Optional: Configure serial port settings if necessary
instrument.baud_rate = 115200  # Set the baud rate as per the device's requirement
instrument.data_bits = 8
instrument.stop_bits = pyvisa.constants.StopBits.one
instrument.parity = pyvisa.constants.Parity.none

# Example command to check connection (this may vary based on the OWON's command set)
response = instrument.query('*IDN?')

# Print the response from the device
print(f'Device response: {response}')

# Always close the connection after use
instrument.close()
