# rpi-miflora-mqtt
Xiaomi Mi Flower Care - MQTT bridge

Script to read Xiaomi Flora values and publish it via MQTT to be used in Openhab or other home automation

It will scan for all Xiaomi miflora devices and publish the values to the MQTT server.

Paho (mqtt) and gatt libraries are required.

to install :
```
sudo apt-get install python-pip
pip install paho-mqtt
pip install gattlib
```

this requires Bluez 5.37 or higher to be installed as well


```
0 */2 * * * /usr/bin/sudo hciconfig hci0 reset; /usr/bin/python /home/pi/miflora/miflora.py >/dev/null 2>&1
```