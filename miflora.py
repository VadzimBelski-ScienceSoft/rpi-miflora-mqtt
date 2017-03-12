#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-
# Scans for and reads data from Xiaomi flower monitor and publish via MQTT


import sys
from struct import unpack
import paho.mqtt.client as mqtt
from gattlib import DiscoveryService, GATTRequester, GATTResponse

verbose = True

service = DiscoveryService("hci0")
devices = service.discover(6)

baseTopic = "miflower/"

mqttc = mqtt.Client("miflora")
mqttc.username_pw_set("<USER NAME>","<PASSWORD>")
mqttc.connect("<IP ADDRESS>", 1883)

for address, name in list(devices.items()):
    try:	
	if (name == "Flower care"):
		
		topic= baseTopic + address.replace(':', '') + '/'
		requester = GATTRequester(address, True)

		#Read battery and firmware version attribute
		data=requester.read_by_handle(0x0038)[0]
		battery, firmware = unpack('<B6s',data)

		#Enable real-time data reading
		requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))

		#Read plant data
		data=requester.read_by_handle(0x0035)[0]
		temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)

		mqttc.publish(topic + 'battery', battery )
		mqttc.publish(topic + 'temperature', temperature / 10.)
		mqttc.publish(topic + 'sunlight', sunlight)
		mqttc.publish(topic + 'moisture', moisture)
		mqttc.publish(topic + 'fertility', fertility)

		if (verbose):
			print("name: {}, address: {}".format(name, address))
			print "Battery level:",battery,"%"
			print "Firmware version:",firmware
			print "Light intensity:",sunlight,"lux"
			print "Temperature:",temperature/10.," C"
			print "Soil moisture:",moisture,"%"
			print "Soil fertility:",fertility,"uS/cm"

    except:
        print "Error during reafing:", sys.exc_info()[0]
