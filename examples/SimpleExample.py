#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""

import time
import melopero_apds9960 as mp

device = mp.APDS_9960()

#General settings
device.set_sleep_after_interrupt(False)

#Wait settings

#Proximity settings

#Color/ALS settings

#Gesture settings

device.enable_all_engines_and_power_up()

while True :
    prox_data = device.get_proximity_data()
    color_data = device.get_color_data()
    gesture_data = []
    for i in range(device.get_number_of_datasets_in_fifo()):
        gesture_data.append(device.get_gesture_data())
    
    device_status = device.get_status()
    gesture_status = device.get_gesture_status()
    
    print("*** Device Status ***")
    for key, value in device_status.items():
        print(key, value)
    print("*** Gesture Status ***")
    for key, value in gesture_status.items():
        print(key, value)
    
    print("*** Data ***")
    print(f"Proximity : {prox_data}")
    print(f"Color/ALS : (c: {color_data[0]}, r: {color_data[1]}, g: {color_data[2]}, b: {color_data[3]})")
    print("*** Gesture Data ***")
    for sample in gesture_data:
        print(f"U: {sample[0]}, D: {sample[1]}, L: {sample[2]}, R: {sample[3]}")
    print("\n\n")
    time.sleep(.1)
        
