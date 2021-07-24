import asyncio
from bleak import discover
from bleak import BleakClient, BleakScanner
import logging
import commands
from termcolor import colored
import argparse
import signal
from prettytable import PrettyTable
from goprocam import constants

camera_info_chars = {"00002a00-0000-1000-8000-00805f9b34fb": {
	"name": "Camera ID"
},  # Camera ID
	commands.Characteristics.BatteryLevel: {
	"name": "Battery Level"
},  # Battery Level
	commands.Characteristics.SerialNumber: {
	"name": "Serial Number"
},  # Serial
	commands.Characteristics.FirmwareVersion: {
	"name": "Firmware Version"
},  # Firmware version
	"b5f90002-aa8d-11e3-9046-0002a5d5c51b": {
		"name": "WiFi SSID"
},  # SSID
}

commands_supported = {

	"command": {
		"record start": {
			"value": commands.Commands.Shutter.Start,
		},
		"record stop": {
			"value": commands.Commands.Shutter.Stop,
		},
		"mode video": {
			"value": commands.Commands.Mode.Video,
		},
		"mode photo": {
			"value": commands.Commands.Mode.Photo,
		},
		"mode multishot": {
			"value": commands.Commands.Mode.Multishot,
		},
		"mode video single":{
			"value": commands.Commands.Submode.Video.Single
		},
  		"mode video timelapse":{
			"value": commands.Commands.Submode.Video.TimeLapse
		},
		"mode photo single":{
			"value": commands.Commands.Submode.Photo.Single
		},
		"mode photo night":{
			"value": commands.Commands.Submode.Photo.Night
		},
		"mode multishot burst":{
			"value": commands.Commands.Submode.Multishot.Burst
		},
		"mode multishot timelapse":{
			"value": commands.Commands.Submode.Multishot.TimeLapse
		},
		"mode multishot nightlapse":{
			"value": commands.Commands.Submode.Multishot.NightLapse
		},
		"poweroff": {
			"value": commands.Commands.Basic.PowerOff,
		},
		"poweroff-force": {
			"value": commands.Commands.Basic.PowerOffForce,
		},
		"tag": {
			"value": commands.Commands.Basic.HiLightTag,
		},
		"locate on": {
			"value": commands.Commands.Locate.ON,
		},
		"locate off": {
			"value": commands.Commands.Locate.OFF,
		},
		"wifi on": {
			"value": commands.Commands.WiFi.ON,
		},
		"wifi off": {
			"value": commands.Commands.WiFi.OFF,
		},
  
		# OpenGoPro-spec commands
		"preset activity": {
			"value": commands.Commands.Presets.Activity
		},
		"preset burst": {
			"value": commands.Commands.Presets.BurstPhoto
		},
		"preset cinematic": {
			"value": commands.Commands.Presets.Cinematic
		},
		"preset liveburst": {
			"value": commands.Commands.Presets.LiveBurst
		},
		"preset nightphoto": {
			"value": commands.Commands.Presets.NightPhoto
		},
		"preset nightlapse": {
			"value": commands.Commands.Presets.NightLapse
		},
		"preset photo": {
			"value": commands.Commands.Presets.Photo
		},
		"preset slomo": {
			"value": commands.Commands.Presets.SloMo
		},
		"preset standard": {
			"value": commands.Commands.Presets.Standard
		},
		"preset timelapse": {
			"value": commands.Commands.Presets.TimeLapse
		},
		"preset timewarp": {
			"value": commands.Commands.Presets.TimeWarp
		},
		"preset maxphoto": {
			"value": commands.Commands.Presets.MaxPhoto
		},
		"preset maxtimewarp": {
			"value": commands.Commands.Presets.MaxTimewarp
		},
		"preset maxvideo": {
			"value": commands.Commands.Presets.MaxVideo
		},
		"preset group video": {
			"value": commands.Commands.PresetGroups.Video
		},
		"preset group photo": {
			"value": commands.Commands.PresetGroups.Photo
		},
		"preset group multishot": {
			"value": commands.Commands.PresetGroups.Timelapse
		},
		"turbo on": {
			"value": commands.Commands.Turbo.ON
		},
  		"turbo off": {
			"value": commands.Commands.Turbo.OFF
		}
	}
}

settings_supported = {
	"video": {
		"resolution": {
			"first": constants.Video.RESOLUTION,
			"contents": "constants.Video.Resolution",
			"prefix": "R"
		},
		"framerate": {
			"first": constants.Video.FRAME_RATE,
			"contents": "constants.Video.FrameRate",
			"prefix": "FR"
		},
		"fov": {
			"first": constants.Video.FOV,
			"contents": "constants.Video.Fov",
			"prefix": ""
		},
		# "aspect_ratio": {
		# 	"first": constants.Video.ASPECT_RATIO,
		# 	"contents": "constants.Video.AspectRatio",
		# 	"prefix": "AP"
		# },
		"lowlight": {
			"first": constants.Video.LOW_LIGHT,
			"contents": "constants.Video.LowLight",
			"prefix": ""
		},
		# "hypersmooth": {
		# 	"first": constants.Video.HYPERSMOOTH,
		# 	"contents": "constants.Video.Hypersmooth",
		# 	"prefix": ""
		# },
		# "lens": {
		# 	"first": constants.Video.LENS,
		# 	"contents": "constants.Video.Lens",
		# 	"prefix": ""
		# },
		"protune": {
			"first": constants.Video.PROTUNE_VIDEO,
			"contents": "constants.Video.ProTune",
			"prefix": ""
		},
		"white_balance": {
			"first": constants.Video.WHITE_BALANCE,
			"contents": "constants.Video.WhiteBalance",
			"prefix": "WB"
		},
		"color": {
			"first": constants.Video.COLOR,
			"contents": "constants.Video.Color",
			"prefix": ""
		},
		"iso_limit": {
			"first": constants.Video.ISO_LIMIT,
			"contents": "constants.Video.IsoLimit",
			"prefix": "ISO"
		},
		"sharpness": {
			"first": constants.Video.SHARPNESS,
			"contents": "constants.Video.Sharpness",
			"prefix": ""
		},
	},
	"photo": {
		"resolution": {
			"first": constants.Photo.RESOLUTION,
			"contents": "constants.Photo.Resolution",
			"prefix": "R"
		},
		"raw": {
			"first": constants.Photo.RAW_PHOTO,
			"contents": "constants.Photo.RawPhoto",
			"prefix": ""
		},
		"superphoto": {
			"first": constants.Photo.SUPER_PHOTO,
			"contents": "constants.Photo.SuperPhoto",
			"prefix": ""
		},
		"protune": {
			"first": constants.Photo.PROTUNE_PHOTO,
			"contents": "constants.Photo.ProTune",
			"prefix": ""
		},
		"white_balance": {
			"first": constants.Photo.WHITE_BALANCE,
			"contents": "constants.Photo.WhiteBalance",
			"prefix": "WB"
		},
		"color": {
			"first": constants.Photo.COLOR,
			"contents": "constants.Photo.Color",
			"prefix": ""
		},
		"iso_limit": {
			"first": constants.Photo.ISO_LIMIT,
			"contents": "constants.Photo.IsoLimit",
			"prefix": "ISO"
		},
		"iso_min": {
			"first": constants.Photo.ISO_MIN,
			"contents": "constants.Photo.IsoMin",
			"prefix": "ISO"
		},
		"sharpness": {
			"first": constants.Photo.SHARPNESS,
			"contents": "constants.Photo.Sharpness",
			"prefix": ""
		},
	},
	"multishot": {
		"resolution": {
			"first": constants.Multishot.RESOLUTION,
			"contents": "constants.Multishot.Resolution",
			"prefix": "R"
		},
		"nightlapse_exp": {
			"first": constants.Multishot.NIGHT_LAPSE_EXP,
			"contents": "constants.Multishot.NightLapseExp",
			"prefix": "Exp"
		},
		"nightlapse_interval": {
			"first": constants.Multishot.NIGHT_LAPSE_INTERVAL,
			"contents": "constants.Multishot.NightLapseInterval",
			"prefix": "I"
		},
		"timelapse_interval": {
			"first": constants.Multishot.TIMELAPSE_INTERVAL,
			"contents": "constants.Multishot.TimeLapseInterval",
			"prefix": "I"
		},
		"burst_rate": {
			"first": constants.Multishot.BURST_RATE,
			"contents": "constants.Multishot.BurstRate",
			"prefix": "B"
		},
		"protune": {
			"first": constants.Multishot.PROTUNE_MULTISHOT,
			"contents": "constants.Multishot.ProTune",
			"prefix": ""
		},
		"white_balance": {
			"first": constants.Multishot.WHITE_BALANCE,
			"contents": "constants.Multishot.WhiteBalance",
			"prefix": "WB"
		},
		"color": {
			"first": constants.Multishot.COLOR,
			"contents": "constants.Multishot.Color",
			"prefix": ""
		},
		"iso_limit": {
			"first": constants.Multishot.ISO_LIMIT,
			"contents": "constants.Multishot.IsoLimit",
			"prefix": "ISO"
		},
		"iso_min": {
			"first": constants.Multishot.ISO_MIN,
			"contents": "constants.Multishot.IsoMin",
			"prefix": "ISO"
		},
		"sharpness": {
			"first": constants.Multishot.SHARPNESS,
			"contents": "constants.Multishot.Sharpness",
			"prefix": ""
		},
	},
}

start_mode = commands.Commands.Mode.Video

def handle_exit(signal, frame):
	print("\n\nExiting program. Safe flights.")
	exit()


async def run(address, command_to_run=None, is_verbose=True):
	log = logging.getLogger(__name__)
	log.setLevel(logging.DEBUG if is_verbose else logging.WARNING)
	async with BleakClient(address) as client:
		def callback(sender: int, data: bytearray):
			log.warning(colored("{}: {}".format(sender, data.hex()), "green"))

		caminfo = PrettyTable()
		caminfo.field_names = [colored("Info", "cyan", attrs=["bold", "underline"]), colored(
			"Value", "green", attrs=["bold", "underline"])]
		caminfo.align = "l"
		for service in client.services:
			for char in service.characteristics:
				if "read" in char.properties:
					if char.uuid not in camera_info_chars:
						continue
					try:
						value = bytes(await client.read_gatt_char(char.uuid))
						valueinutf = value.decode("utf-8")
						if char.uuid == "00002a19-0000-1000-8000-00805f9b34fb":
							valueinutf = str(ord(value)) + "%"
						caminfo.add_row([colored(camera_info_chars[char.uuid].get(
							"name"), "cyan"), colored(valueinutf, "green")])
					except Exception:
						continue
		if is_verbose:
			print(caminfo)

		await client.start_notify(commands.Characteristics.CommandNotifications, callback)
		await client.start_notify(commands.Characteristics.SettingNotifications, callback)
		await client.start_notify(commands.Characteristics.StatusNotifications, callback)

		if client.is_connected:
			log.info("Camera is connected")
		if command_to_run is None:
			await client.write_gatt_char(commands.Characteristics.ControlCharacteristic, start_mode)
		await client.write_gatt_char(commands.Characteristics.ControlCharacteristic, commands.Commands.Analytics.SetThirdPartyClient)
		await asyncio.sleep(1.0)
		signal.signal(signal.SIGINT, handle_exit)
  
		if command_to_run is not None:
			if command_to_run in commands_supported["command"]:
				await client.write_gatt_char(commands.Characteristics.ControlCharacteristic, commands_supported["command"][command_to_run].get("value"))

			elif command_to_run.startswith("cmd"):
				await client.write_gatt_char(commands.Characteristics.ControlCharacteristic,
											 bytearray(command_to_run.split("cmd")[1].encode()))
			elif command_to_run.startswith("set"):

				if len(command_to_run.strip().split(" ")) != 4:
					log.error(
						"Bad syntax. Should be: set [video/photo/multishot/setup] [setting key] [value]")

				first = 0
				contents = None
				prefix = ""

				section = command_to_run.split(" ")[1]
				key = command_to_run.split(" ")[2]
				val = command_to_run.split(" ")[3]

				if section in settings_supported and key in settings_supported[section]:
					first = settings_supported[section][key]["first"]
					contents = settings_supported[section][key]["contents"]
					prefix = settings_supported[section][key]["prefix"]

				try:
					command = "\x03" + \
						chr(int(first)) + "\x01" + \
						chr(int(eval(contents + "." + prefix + val)))
					await client.write_gatt_char(commands.Characteristics.SettingCharacteristic, bytearray(command.encode()))
				except:
					log.error("Bad settings combination.")
			else:
				log.error("Unrecognized command %s" % command_to_run)
			return
		while True:

			cmd = input(">> ")
			if cmd == "exit":
				exit()
			elif cmd == "help":
				print("Supported commands")
				for command in commands_supported["command"].keys():
					print(colored("\t" + command, "yellow"))
			elif cmd in commands_supported["command"]:
				await client.write_gatt_char(commands.Characteristics.ControlCharacteristic, commands_supported["command"][cmd].get("value"))

			elif cmd.startswith("cmd"):
				await client.write_gatt_char(commands.Characteristics.ControlCharacteristic,
											 bytearray(cmd.split("cmd")[1].encode()))
			elif cmd.startswith("set"):

				if len(cmd.strip().split(" ")) != 4:
					log.error(
						"Bad syntax. Should be: set [video/photo/multishot/setup] [setting key] [value]")

				first = 0
				contents = None
				prefix = ""

				section = cmd.split(" ")[1]
				key = cmd.split(" ")[2]
				val = cmd.split(" ")[3]

				if section in settings_supported and key in settings_supported[section]:
					first = settings_supported[section][key]["first"]
					contents = settings_supported[section][key]["contents"]
					prefix = settings_supported[section][key]["prefix"]

				try:
					command = "\x03" + \
						chr(int(first)) + "\x01" + \
						chr(int(eval(contents + "." + prefix + val)))
					await client.write_gatt_char(commands.Characteristics.SettingCharacteristic, bytearray(command.encode()))
				except:
					log.error("Bad settings combination.")
			else:
				log.error("Unrecognized command %s" % cmd)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--interactive', "-i", help="Interactive control shell",
						required=False, type=bool, default=True)
	parser.add_argument('--address', "-a", help="Camera BLE HW address",
						required=False, default=[], action="append", nargs="+")
	parser.add_argument(
		'--command', "-c", help="Execute command, overrides `-i`", required=False, type=str)
	parser.add_argument(
		'--from-file', "-f", help="Execute instructions from file", required=False, default="")
	parser.add_argument('--verbose', dest='verbose', action='store_true')
	parser.add_argument('--no-verbose', dest='verbose', action='store_false')
	parser.set_defaults(verbose=True)
	args = parser.parse_args()
 
	command_to_run = None
	is_verbose = args.verbose
	if args.address == []:

		async def discovercameras():
			cameras = []
			devices = await discover()
			global address
			for d in devices:

				if "GoPro" in str(d):
					cameras.append(["GoPro", d.address])
			if len(cameras) == 0:
				print("No cameras detected.")
				exit()
			if len(cameras) == 1:
				print(colored("Connecting to " +
							  cameras[0][1], "green", attrs=["bold"]))
				address = [cameras[0][1]]
			else:
				for index, i in enumerate(cameras):
					print(
						colored("[{}] {} - {}".format(index, i[0], i[1]), "cyan"))
				address = [cameras[int(input(">>> "))][1]]

		loop = asyncio.get_event_loop()
		loop.run_until_complete(discovercameras())
	else:
		address = args.address[0]
	if args.command != "":
		command_to_run = args.command
		args.interactive = False
	if args.interactive:
		command_to_run=None
		if len(address) > 1:
			print("Only one camera supported in interactive mode")
			exit()
	loop = asyncio.get_event_loop()
	loop.set_debug(False)
	tasks = asyncio.gather(*(run(add, command_to_run, is_verbose) for add in address))
	loop.run_until_complete(tasks)
