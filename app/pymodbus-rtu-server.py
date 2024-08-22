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
            for key in data:
                obj = data[key]
                if "id" in obj and "value" in obj:
                    self.setValues(obj["id"], [obj["value"]])
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

    if not "endpoint_url" in config:
        raise ValueError("The endpoint URL is required in the config.json file")
    if not "serial_port" in config:
        raise ValueError("The serial port is required in the config.json file")
    if not "baudrate" in config:
        raise ValueError("The baudrate is required in the config.json file")
    if not "timeout" in config:
        raise ValueError("The timeout is required in the config.json file")
    if not "stopbits" in config:
        raise ValueError("The stopbits is required in the config.json file")
    if not "bytesize" in config:
        raise ValueError("The bytesize is required in the config.json file")
    if not "parity" in config:
        raise ValueError("The parity is required in the config.json file")
    
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