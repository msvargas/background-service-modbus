from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging
import random

# Configuración del logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# Crear el contexto Modbus con valores iniciales para emular sensores
store = ModbusSlaveContext(
    hr=ModbusSequentialDataBlock(0x000, random.sample(range(100),28)), 
)
context = ModbusServerContext(slaves=store, single=True)

# Información del dispositivo
identity = ModbusDeviceIdentification()
identity.VendorName = 'ModbusServer'
identity.ProductCode = 'MS'
identity.VendorUrl = 'http://example.com'
identity.ProductName = 'Modbus RTU Server'
identity.ModelName = 'Modbus RTU Server Model'
identity.MajorMinorRevision = '1.0'

# Iniciar el servidor Modbus RTU
if __name__ == "__main__":
    StartSerialServer(
        context=context, 
        identity=identity, 
        port='/dev/tty.usbserial-21230',  # Cambia esto por el puerto serial de tu conversor
        baudrate=9600, 
        timeout=1, 
        stopbits=1, 
        bytesize=8, 
        parity='N', 
        method='rtu'
    )