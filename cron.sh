#!/bin/bash

/usr/bin/python /home/pi/Desktop/workbench/parking/CameraClient0.py
/usr/bin/python /home/pi/Desktop/workbench/parking/CameraClient1.py
/usr/bin/python /home/pi/Desktop/workbench/parking/CameraClient2.py
cd /home/pi/Desktop/workbench/parking && git pull -q origin master
sudo reboot
