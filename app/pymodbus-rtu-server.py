import json
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

# Leer configuración desde config.json
def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

config = load_config('config.json')

class CustomModbusDataBlock(ModbusSequentialDataBlock):
    def getValues(self, address, count=1):
        data = self.fetch_data_from_endpoint()
        if data:
            self.update_values(data)
        return super().getValues(address, count)

    def fetch_data_from_endpoint(self):
        try:
            # URL del endpoint
            endpoint_url = config["endpoint_url"]
            response = requests.get(endpoint_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Error al obtener los datos del endpoint: {e}")
            return None

    def update_values(self, data):
        for key, obj in data.items():
            if isinstance(obj, dict) and "id" in obj and "value" in obj:
                self.setValues(obj["id"], [obj["value"]])
            else:
                log.warning(f"Datos inválidos para la clave {key}: {obj}")

# Crear el contexto Modbus con la clase personalizada
store = ModbusSlaveContext(
    hr=CustomModbusDataBlock(0x000, [0]*100),  # Assume max 6 registers for initialization
)
context = ModbusServerContext(slaves=store, single=True)

identity = ModbusDeviceIdentification()
identity.VendorName = 'ModbusServer'
identity.ProductCode = 'MS'
identity.VendorUrl = 'http://example.com'
identity.ProductName = 'Modbus RTU Server'
identity.ModelName = 'Modbus RTU Server Model'
identity.MajorMinorRevision = '1.0'

if __name__ == "__main__":

    required_keys = ["endpoint_url", "serial_port", "baudrate", "timeout", "stopbits", "bytesize", "parity"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"The {key} is required in the config.json file")
    
    StartSerialServer(
        context=context,
        identity=identity,
        port=config["serial_port"],
        baudrate=config["baudrate"],
        timeout=config["timeout"],
        stopbits=config["stopbits"],
        bytesize=config["bytesize"],
        parity=config["parity"],
        method='rtu'
    )