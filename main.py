from bluetooth.ble import DiscoveryService
import gatt
from goprocam import GoProCamera, constants
import time
import logging
import commands

logger = logging.getLogger('GoPro BLE')
logger.setLevel(logging.DEBUG)

def discover_camera():
    cameras=[]
    service = DiscoveryService()
    devices = service.discover(2)

    for address, name in devices.items():
        if name.startswith("GoPro"):
            cameras.append([name,address])
    if len(cameras) == 0:
        print("No cameras detected.")
        exit()
    if len(cameras) == 1:
        return cameras[0][1]
    for index, i in enumerate(cameras):
        print("[{}] {} - {}".format(index, i[0], i[1]))
    return cameras[int(input("ENTER BT GoPro ADDR: "))][1]

mac_address=discover_camera()


manager = gatt.DeviceManager(adapter_name='hci0')
class AnyDevice(gatt.Device):

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))
        #gopro.pair(usepin=False)

    def services_resolved(self):
        super().services_resolved()
        control_service = next(
            s for s in self.services
            if s.uuid == commands.Characteristics.Control)

        time.sleep(5)
        
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
            print(i.uuid)
            if i.uuid.startswith("b5f90072"):
                i.write_value(bytearray(b'\x03\x02\x01\x00'))
        pass
    def characteristic_write_value_succeeded(self, characteristic):
        print("[recv] {}".format(characteristic.uuid))
        if characteristic.uuid.startswith("b5f90072"):
            cmd=input(">> ")
            if cmd == "exit":
                exit()
            elif cmd == "record start":
                characteristic.write_value(commands.Commands.Shutter.Start)
            elif cmd == "record stop":
                characteristic.write_value(commands.Commands.Shutter.Stop)
            elif cmd == "mode video":
                characteristic.write_value(commands.Commands.Mode.Video)
            elif cmd == "mode photo":
                characteristic.write_value(commands.Commands.Mode.Photo)
            elif cmd == "mode multishot":
                characteristic.write_value(commands.Commands.Mode.Multishot)
            elif cmd == "poweroff":
                characteristic.write_value(commands.Commands.Basic.PowerOff)
            elif cmd == "poweroff-force":
                characteristic.write_value(commands.Commands.Basic.PowerOffForce)
            elif cmd == "tag":
                characteristic.write_value(commands.Commands.Basic.HiLightTag)
            elif cmd == "locate on":
            	characteristic.write_value(commands.Commands.Locate.ON)
            elif cmd == "locate off":
            	characteristic.write_value(commands.Commands.Locate.OFF)
            elif cmd == "wifi off":
                characteristic.write_value(commands.Commands.WiFi.OFF)
            elif cmd == "wifi on":
                characteristic.write_value(commands.Commands.WiFi.ON)
            elif cmd.startswith("cmd"):
                characteristic.write_value(bytearray( cmd.split("cmd" )[1].encode() ))    
            else:
            	exit()    
    def characteristic_value_updated(self, characteristic, value):
        charsObj = commands.Characteristics()
        chars =  [a for a in dir(charsObj) if not a.startswith('__')]
        for namedchar in chars:
            if getattr(charsObj, namedchar) == characteristic.uuid:   
                print(">>>", namedchar)
                print("\t>>>", value.decode("utf-8"))
device = AnyDevice(mac_address=mac_address, manager=manager)
device.connect()
manager.run()

