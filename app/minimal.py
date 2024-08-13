#!/usr/bin/env python3
import minimalmodbus

# Print USB devices
import serial.tools.list_ports
for port in serial.tools.list_ports.comports():
    print(port)
instrument = minimalmodbus.Instrument('/dev/tty.usbserial-21210', 1, debug=True)  # port name, slave address (in decimal)

## Read temperature (PV = ProcessValue) ##
temperature = instrument.read_register(0, 1)  # Registernumber, number of decimals
print(temperature)

## Change temperature setpoint (SP) ##
#NEW_TEMPERATURE = 95
#instrument.write_register(24, NEW_TEMPERATURE, 1)  # Registernumber, value, number of decimals for storage