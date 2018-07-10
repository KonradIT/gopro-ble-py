# bluetooth low energy scan
from bluetooth.ble import DiscoveryService
import gatt
from goprocam import GoProCamera, constants
import time

gopro = GoProCamera.GoPro()
def discover_camera():
	service = DiscoveryService()
	devices = service.discover(2)
	for address, name in devices.items():
		if name.startswith("GoPro"):
			print("name: {}, address: {}".format(name, address))

discover_camera()
mac_address=input("ENTER GoPro BT ADDR: ")

manager = gatt.DeviceManager(adapter_name='hci0')
class AnyDevice(gatt.Device):

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))
        gopro.pair(usepin=False)

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))


    def services_resolved(self):
        super().services_resolved()

        for service in self.services:
            print("[%s]  Service [%s]" % (self.mac_address, service.uuid))
            for characteristic in service.characteristics:
                print("[%s]    Characteristic [%s]" % (self.mac_address, characteristic.uuid))
        device_information_service = next(
            s for s in self.services
            if s.uuid == '0000180a-0000-1000-8000-00805f9b34fb')

        firmware_version_characteristic = next(
            c for c in device_information_service.characteristics
            if c.uuid == '00002a26-0000-1000-8000-00805f9b34fb')

        firmware_version_characteristic.read_value()

        control_service = next(
            s for s in self.services
            if s.uuid == '0000fea6-0000-1000-8000-00805f9b34fb')

        time.sleep(5)
        print("PHOTO")
        for i in control_service.characteristics:
            time.sleep(5)
            print(i.uuid)
            i.write_value(bytearray(b'\x02\x01\x01'))
		

        command_characteristic = next(
            c for c in control_service.characteristics
            if c.uuid == 'b5f90072-aa8d-11e3-9046-0002a5d5c51b')
        command_characteristic.write_value(bytearray(b'\x02\x01\x00'))
        time.sleep(1)

        command_characteristic.write_value(bytearray(b'\x02\x02\x00'))
        time.sleep(1)
        
        command_characteristic.write_value(bytearray(b'\x02\x02\x01'))
        time.sleep(1)

        command_characteristic.write_value(bytearray(b'\x02\x02\x02'))
        time.sleep(1)

        command_characteristic.write_value(bytearray(b'\x03\x02\x01\x01'))
        time.sleep(1)

        command_characteristic.write_value(bytearray(b'\x02\x01\x01'))
        time.sleep(1)
        pass
    def characteristic_value_updated(self, characteristic, value):
        print("Firmware version:", value.decode("utf-8"))
        pass

device = AnyDevice(mac_address=mac_address, manager=manager)
device.connect()
while True:
	cmd=input(">> ")
	if cmd == "disconnect":
		device.disconnect()
		exit()
	if cmd == "record start":
		print("record")

manager.run()
