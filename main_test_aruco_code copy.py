# -*- coding: utf-8 -*-

"""

Created on Tue Mar 22 16:38:20 2022

 

@author: alouik

"""

 

from djitellopy import Tello
import cv2

tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamon()

while True:
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (400, 250))
    cv2.imshow("Image", img)
    cv2.waitKey(1)