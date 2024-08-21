# background-service-modbus

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