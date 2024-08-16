from pymodbus.server import StartSerialServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging
import requests

# Configuración del logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

# URL del endpoint
endpoint_url = "http://localhost:8000/getLastMeasurements"

# Subclass ModbusSequentialDataBlock to customize getValues
class CustomModbusDataBlock(ModbusSequentialDataBlock):
    def getValues(self, address, count=1):
        # Fetch data from the endpoint on each request
        data = self.fetch_data_from_endpoint()
        if data:
            # Update registers based on the id as the address
            for key in data:
                obj = data[key]
                if "id" in obj and "value" in obj:
                    print(f"Updating register {obj['id']} with value {obj['value']}")
                    self.setValues(obj["id"], [obj["value"]])

        return super().getValues(address, count)

    def fetch_data_from_endpoint(self):
        try:
            response = requests.get(endpoint_url)
            response.raise_for_status()  # Raise an error for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Error al obtener los datos del endpoint: {e}")
            return None

# Crear el contexto Modbus con la clase personalizada
store = ModbusSlaveContext(
    hr=CustomModbusDataBlock(0x000, [0]*6),  # Assume max 6 registers for initialization
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