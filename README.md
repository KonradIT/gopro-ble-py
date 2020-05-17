# gopro-ble-py

Python Bluetooth controller for GoPro cameras starting from the HERO5 Black (successfully tested with the HERO5 Black, HERO6 Black, HERO7 Black, MAX)

## How to run:

Enable WiFi on the GoPro and go to connect > connect new > GoPro APP

Then connect to the WiFi AP created by the GoPro

Make sure you have administrator priviledges so you can send commands from your BT module:

    sudo python main.py

Then enter the commands.

    >> record start
    [recv] ...

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

Settings are parsed as constant strings from my library [gopro-py-api](http://github.com/konradit/gopro-py-api). Such as: Video.RESOLUTION Video.Resolution.R4k

## Scripting possiblilities:

See [start_timelapse.py](./start_timelapse.py) on an example on how to write a script to control a camera programatically.

## Sources:

https://github.com/KonradIT/goprowifihack/blob/master/Bluetooth/Platforms/RaspberryPi.md

https://gethypoxic.com/blogs/technical/gopro-hero5-interfaces
