# background-service-modbus

![image](https://github.com/user-attachments/assets/730a2c41-f5f3-4443-98ea-17067136e49c)


Run the application with the following command:

```shell
docker-compose up --build
```

Display available devices with the following command:

```shell
ls /dev/tty.usb*
ls /dev/ttyUSB*
ls /dev/tty.*
```

Test the serial connection with the following command:

```shell
screen /dev/tty.usbserial-1440 9600
```

Install the pyinstaller package with the following command:

```shell
pip install pyinstaller
```

Build the application with the following command:

```shell
pyinstaller --onefile app/pymodbus-rtu-server.py
```

Run the application with the following command:

```shell
./dist/pymodbus-rtu-server
```

Install the modpoll package in Raspberry with the following command:

```shell
sudo apt-get install modpoll
```

or https://www.modbusdriver.com/diagslave.html

Test the application with the following command:

```shell
modpoll -m rtu -a 1 -r 1 -c 1 -t 4 -b 9600 -d 8 -s 1 /dev/tty.usbserial-1440
```


Share mac os files with raspberry pi with the following command:

Mac to Pi
```shell
 rsync -avz ./ pi@192.168.1.38:/home/pi/shared
```

Pi to Mac
```shell
rsync -avz pi@192.168.1.38:/home/pi/shared ./```
```

Sync dist folder

```shell
rsync -avz pi@192.168.1.38:/home/pi/shared/dist ./
```

Create systemd service in Raspberry with the following command:

```shell
sudo cp modbus_server.service /etc/systemd/system/
```

Start and enable the service with the following command:

```shell
sudo systemctl daemon-reload
sudo systemctl restart modbus_server.service
```


Check status of the service with the following command:

```shell
sudo systemctl status modbus_server.service
```

```shell
 zip -r project.zip ./
```

## Config file:

```json
{
  "endpoint_url" : "http://localhost:8000/getLastMeasurements",
  "serial_port": "/dev/ttyUSB0",
  "baudrate": 9600,
  "timeout": 10,
  "stopbits": 1,
  "bytesize": 8,
  "parity": "N"
}
```


# Installation


Unzip project.zip in the desired location

```shell
mkdir ~/shared && cd ~/shared
```

![image](https://github.com/user-attachments/assets/65ab374b-0f36-4a00-be89-69fb26ebf172)

Run the following command to install the service:

```shell
sudo cp ~/shared/modbus_server.service /etc/systemd/system/
chmod +x ~/shared/dist/pymodbus-rtu-server
sudo systemctl daemon-reload
sudo systemctl restart modbus_server.service
sudo systemctl enable modbus_server.service
```

Check status of the service with the following command:

```shell
sudo systemctl status modbus_server.service
```

