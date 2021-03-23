BLE_CHAR_STRING = "0000{}-0000-1000-8000-00805f9b34fb"
BLE_CHAR_V2_STRING = "{}-aa8d-11e3-9046-0002a5d5c51b"
class Commands:
	class Shutter:
		Start = bytearray(b'\x03\x01\x01\x01')
		Stop = bytearray(b'\x03\x01\x01\x00')
	class Mode:
		Video = bytearray(b'\x03\x02\x01\x00')
		Photo = bytearray(b'\x03\x02\x01\x01')
		Multishot = bytearray(b'\x03\x02\x01\x02')
	class Submode:
		class Video:
			Single =    bytearray(b'\x05\x03\x01\x00\x01\x00')
			TimeLapse = bytearray(b'\x05\x03\x01\x00\x01\x01')
		class Photo:
			Single = bytearray(b'\x05\x03\x01\x01\x01\x01')
			Night = bytearray(b'\x05\x03\x01\x01\x01\x02')
		class Multishot:	
			Burst =      bytearray(b'\x05\x03\x01\x02\x01\x00')
			TimeLapse =  bytearray(b'\x05\x03\x01\x02\x01\x01')
			NightLapse = bytearray(b'\x05\x03\x01\x02\x01\x02')

	class Basic:
		PowerOff = bytearray(b'\x01\x05')
		PowerOffForce = bytearray(b'\x01\x04')
		HiLightTag = bytearray(b'\x01\x18')
	class Locate:
		ON = bytearray(b'\x03\x16\x01\x01')
		OFF = bytearray(b'\x03\x16\x01\x00')
	class WiFi:
		ON = bytearray(b'\x03\x17\x01\x01')
		OFF = bytearray(b'\x03\x17\x01\x00')
		
class Characteristics:
	Control = BLE_CHAR_STRING.format("FEA6".lower())
	Info = BLE_CHAR_STRING.format("180A".lower())
	Battery = BLE_CHAR_STRING.format("180F".lower())
	
	FirmwareVersion = BLE_CHAR_STRING.format("2A26".lower())
	SerialNumber = BLE_CHAR_STRING.format("2A25".lower())
	BatteryLevel = BLE_CHAR_STRING.format("2A19".lower())

	ControlCharacteristic = BLE_CHAR_V2_STRING.format("B5F90072".lower())
	SettingCharacteristic = BLE_CHAR_V2_STRING.format("B5F90074".lower())

	CommandNotifications = BLE_CHAR_V2_STRING.format("B5F90073".lower())
	SettingNotifications = BLE_CHAR_V2_STRING.format("B5F90075".lower())