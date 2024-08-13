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
