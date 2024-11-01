import json
import asyncio
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
    def __init__(self, address, values):
        super().__init__(address, values)
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.periodic_update())

    async def periodic_update(self):
        while True:
            data = await self.fetch_data_from_endpoint()
            if data:
                self.update_values(data)
            await asyncio.sleep(config["request_interval"])  # Espera de 1 minuto entre actualizaciones

    async def fetch_data_from_endpoint(self):
        try:
            # URL del endpoint
            endpoint_url = config["endpoint_url"]
            response = requests.get(endpoint_url, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log.error(f"Error al obtener los datos del endpoint: {e}")
            return None

    def update_values(self, data):
        for obj in data["result"]:
            if isinstance(obj, dict) and "id" in obj and "value" in obj:
                measure_type = obj.get("measure_type", "desconocido")  # Si no hay "measure_type", usa "desconocido"
                log.debug(f"Actualizando valor de {measure_type} ID:{obj['id']} => {obj['value']}")
                # Multiplicar el valor por 10 para simular un valor de 1 decimal y enviar un entero siempre
                value = int(obj["value"] * config["multiplier"])
                self.setValues(obj["id"], [value])
            else:
                measure_type = obj.get("measure_type", "desconocido")  # Si no hay "measure_type", usa "desconocido"
                log.warning(f"Datos inválidos para {measure_type}: {obj}")

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
    required_keys = ["endpoint_url", "serial_port", "baudrate", "timeout", "stopbits", "bytesize", "parity", "slave_id", "request_interval", "multiplier"]
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
        id=config["slave_id"],
        method='rtu',
    )
