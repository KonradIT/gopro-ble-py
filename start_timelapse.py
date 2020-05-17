import gatt
from goprocam import GoProCamera, constants
import time
import logging
import commands
import sys


command_list = [
	commands.Commands.Mode.Multishot,
 	commands.Commands.WiFi.OFF,
	commands.Commands.Shutter.Start
]

index = 0

manager = gatt.DeviceManager(adapter_name='hci1')

class AnyDevice(gatt.Device):

	def connect_succeeded(self):
		super().connect_succeeded()
		print("[%s] Connected" % (self.mac_address))

	def services_resolved(self):
		super().services_resolved()
		control_service = next(
			s for s in self.services
			if s.uuid == commands.Characteristics.Control)
		
		device_information_service = next(
			s for s in self.services
			if s.uuid == commands.Characteristics.Info)

		firmware_version_characteristic = next(
			c for c in device_information_service.characteristics
			if c.uuid == commands.Characteristics.FirmwareVersion)

		serial_number_characteristic = next(
			c for c in device_information_service.characteristics
			if c.uuid == commands.Characteristics.SerialNumber)

		firmware_version_characteristic.read_value()
		serial_number_characteristic.read_value()
  
		for i in control_service.characteristics:
			if i.uuid.startswith("b5f90072"):
				print("Sending commands....")
				i.write_value(command_list[index])
		pass

	def characteristic_write_value_succeeded(self, characteristic):
		print("[recv] {}".format(characteristic.uuid))
		global index
		index += 1
		if index == len(command_list):
				self.disconnect()
				self.manager.stop()
		if index is not len(command_list): characteristic.write_value(command_list[index])


	def characteristic_value_updated(self, characteristic, value):
		chars_obj = commands.Characteristics()
		chars = [a for a in dir(chars_obj) if not a.startswith('__')]
		for namedchar in chars:
			if getattr(chars_obj, namedchar) == characteristic.uuid:
				print(">>>", namedchar)
				print("\t>>>", value.decode("utf-8"))


for addr in ["F9:04:71:AA:AE:18", "D5:DB:AB:69:4B:76"]:
	print("Connecting to:", addr)
	index = 0
	device = AnyDevice(mac_address=addr, manager=manager)
	device.connect()
	manager.run()

sys.exit()
