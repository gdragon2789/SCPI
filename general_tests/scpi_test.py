import pyvisa

# Initialize VISA resource manager
rm = pyvisa.ResourceManager()

# List available instruments
print("Available instruments:", rm.list_resources())

# Replace with your Keithley 6500 resource string (adjust as needed)
# Example: 'USB0::0x05E6::0x6500::12345678::INSTR'
resource_string = 'USB0::0x05E6::0x6500::04507717::INSTR'

try:
    # Connect to the Keithley 6500
    instr = rm.open_resource(resource_string)
    print(f"Connected to: {instr.query('*IDN?')}")

    instr.write('*RST')  # Reset the instrument
    instr.write('TRIGger: MODE NORMAL')  # Set trigger mode to NORMAL

    # Step 1: Configure the first Measure Digitize action
    instr.write('TRIGger:A:LOAD "MeasureDigitize"')  # Load Measure Digitize into Trigger Model
    instr.write('FUNCtion "VOLTage:DC"')  # Set measurement type to DC Voltage
    instr.write('RANGe 10')  # Set measurement range to 10V
    instr.write('TRIGger:A:COUNt 1')  # Perform 1 measurement



except pyvisa.errors.VisaIOError as e:
    print(f"VISA Error: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
finally:
    # Close the connection to the instrument
    if 'instr' in locals():
        instr.close()
        print("Connection closed.")
