import logging
import requests
import asyncio
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncSerialServer

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class CustomModbusDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address, values):
        super().__init__(address, values)

    async def getValues(self, address, count=1):
        response = requests.get('http://localhost:8000/getLastMeasurements')
        if response.status_code == 200:
            data = response.json()
            ## Print the data to see what it looks like
            print(data)
            values = []
            for i in range(count):
                values.append(data.get(f'register_{address + i}', 0))
            return values
        else:
            log.error(f"Failed to get data from endpoint: {response.status_code}")
            return [0] * count

# Create the datastore
store = ModbusSlaveContext(
    hr=CustomModbusDataBlock(0, [0] * 100),  # Holding registers
    di=ModbusSequentialDataBlock(0, [0] * 100),  # Discrete inputs
    co=ModbusSequentialDataBlock(0, [0] * 100),  # Coils
    ir=ModbusSequentialDataBlock(0, [0] * 100)  # Input registers
)
context = ModbusServerContext(slaves=store, single=True)

# Initialize the server information
identity = ModbusDeviceIdentification()
identity.VendorName = 'MyVendor'
identity.ProductCode = 'MyProduct'
identity.VendorUrl = 'http://example.com'
identity.ProductName = 'MyModbusServer'
identity.ModelName = 'MyModel'
identity.MajorMinorRevision = '1.0'

async def run_server():
    await StartAsyncSerialServer(
        context=context,
        identity=identity,
        port='/dev/cu.usbserial-10',
        timeout=1,
        baudrate=9600,
        parity='N',
        stopbits=1,
        bytesize=8,
        framer='rtu'
    )

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_server())
    loop.run_forever()