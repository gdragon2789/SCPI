import pyvisa as pyvisa

rm = pyvisa.ResourceManager()


print(rm.list_resources())
