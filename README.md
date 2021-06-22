# gopro-ble-py

Python Bluetooth controller for GoPro cameras starting from the HERO5 Black (successfully tested with the HERO5 Black, HERO6 Black, HERO7 Black, MAX, HERO9 Black)

![](https://i.imgur.com/AMluyqy.png)

# Important note regarding OpenGoPro:

GoPro released a proper BLE documentation over at [opengopro](https://gopro.com/OpenGoPro) and it matches what I've reverse engineered in the past. But they've done _so much stuff_ I missed, such as getting the status of the camera and doing Protobuf decoding. Their [examples](https://gopro.github.io/OpenGoPro/demos/python/sdk_wireless_camera_control) are extremely well programmed too.

## How to run:

### First pairing:

Enable Wireless Connections on the GoPro and go to connect > connect new > GoPro APP

Then connect your device to the camera via Bluetooth.

On Windows, make sure when you connect to wait for the PC to successfully pair with the camera:

![](https://i.imgur.com/Z0OzHxC.png)

The camera should return to the last mode and exit the pairing screen.

Then run:

    python main.py

Then enter the commands.

    >> record start
    [recv] ...

### Usage:

Commands available:

-   record start
-   record stop
-   mode video
-   mode photo
-   mode multishot
-   poweroff
-   tag
-   wifi off
-   wifi on
-   set (will prompt you to enter settings)
-   exit (disconnect && exit)

Settings are parsed as constant strings from my library [gopro-py-api](http://github.com/konradit/gopro-py-api).

Settings available:

-   video:
    -   resolution
    -   framerate
    -   fov
    -   lowlight
    -   protune
    -   white_balance
    -   color
    -   iso_limit
    -   sharpness

### Multi-camera:

[Video demo](https://twitter.com/konrad_it/status/1368558805706039303)

Pass a list of Bluetooth MAC addresses in the `--address` parameter to control multiple cameras.

### Using via CLI:

By default this script runs in interactive mode, but to control camera aspects via the command line or a bash script pass `--address` and/or `--command`

## Scripting possiblilities:

Commands can be passed using the `--command` parameter (multi camera supported)

`python .\main.py --verbose --address "XX:XX:XX:XX:XX:XX" --command "record start"`

`python .\main.py --verbose --address "XX:XX:XX:XX:XX:XX" --command "wifi on"`

## What happened to the old version?

It relied on `gatt` library and `bluetooth` library, and it was a PITA to work on and install. I decided to move to `bleak` which works perfectly on Windows and Raspbian.

## Sources:

https://github.com/KonradIT/goprowifihack/blob/master/Bluetooth/Platforms/RaspberryPi.md

https://gethypoxic.com/blogs/technical/gopro-hero5-interfaces
