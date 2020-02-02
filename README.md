# OctoPrint-Tiltcam

This plugin adds a new tab to control a [pan tilt stand](https://de.aliexpress.com/item/2048998846.html?spm=a2g0o.productlist.0.0.66692b12ZJAJIk&algo_pvid=c0d9bf2b-ebfc-4a9b-b1e3-87eaf26f9300&algo_expid=c0d9bf2b-ebfc-4a9b-b1e3-87eaf26f9300-0&btsid=b421ad8d-d002-4e9b-9c55-5e1982c82b8a&ws_ab_test=searchweb0_0,searchweb201602_10,searchweb201603_53) with a [camera](https://de.aliexpress.com/item/32669557411.html?spm=a2g0o.productlist.0.0.328e570dHcoaKl&algo_pvid=940b6a7d-e67c-4b68-8f6f-2f652d8427cc&algo_expid=940b6a7d-e67c-4b68-8f6f-2f652d8427cc-16&btsid=fcc6191e-e5eb-4bd9-b233-5d50490863f6&ws_ab_test=searchweb0_0,searchweb201602_10,searchweb201603_53) on top.

It uses the internal webcam setting of octoprint to show the camera image. If you click and hold you mousekey in the view and move around, you'll see the camera moves with your mouse.

## Setup

### Requirements
#### Hardware
- Tilt stand:
This plugin should work with all pan tilt stands that have two servos for X and Y moving.  
It is recommended to use slow servos to smooth out motions.
- Camera:
You can find a compatibility list [here](https://github.com/foosel/OctoPrint/wiki/Webcams-known-to-work)
#### Software
**IN ORDER TO FUNCTION PROPERLY YOU NEED TO INSTALL PIGPIOD MANUALLY:**  
```sudo apt install pigpiod```  
```reboot```  
or if you want a detailed instruction click [here]()  

### Installation
Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/fabiocaruso/OctoPrint-Tiltcam/archive/master.zip

## Configuration
On the first start of Octoprint you'll be asked by a wizard to enter the two GPIO pin numbers where your servos for the X and Y axis are connected. Enter the hardware GPIO number.  
You'll also be noticed if the plugin can't connect to the pigpio daemon, if so, you need to (re-)install pigpiod.

## TODO
- Pigpiod wizard installation
- Speed improvements (websocket)
- Integration in controls tab
- Add to offical repo
