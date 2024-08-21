from pymodbus.client import ModbusSerialClient
import logging

# Configuración del logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Configuración del cliente Modbus RTU
client = ModbusSerialClient(
    port='/dev/ttyUSB1',  # Cambia esto por el puerto serial de tu otro conversor
    baudrate=9600,
    timeout=1,
    stopbits=1,
    bytesize=8,
    parity='N'
)
if client.connect():
    # Leer 4 registros de la dirección 0 del servidor
    result = client.read_holding_registers(0, 5,slave=1)
    
    if not result.isError():
        print(f"Resistance: {result.registers[0]} V")
        print(f"Isolation: {result.registers[1]} A")
        print(f"Pressure: {result.registers[2]} °C")
        print(f"Vibration: {result.registers[3]} mm/s")
        print(f"Temperature: {result.registers[4]} mm/s")
    else:
        print("Error al leer los registros")

    client.close()
else:
    print("Error al conectar al servidor Modbus RTU")