# gopro-ble-py

Python Bluetooth controller for HERO 5 Black 

## How to run:

Enable WiFi on the GoPro and go to connect> connect new > GoPro APP

Then connect to the WiFi AP created by the GoPro

Make sure you have administrator priviledges so you can send commands from your BT module:

    sudo python main.py

Then enter the commands.

    >> record start
    [recv] ...

Commands available:

- record start
- record stop
- mode video
- mode photo
- mode multishot
- poweroff
- tag
- wifi off
- wifi on
- exit (disconnect && exit)

## Sources:

https://github.com/KonradIT/goprowifihack/blob/master/Bluetooth/Platforms/RaspberryPi.md

https://gethypoxic.com/blogs/technical/gopro-hero5-interfaces
