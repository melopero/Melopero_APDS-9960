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

device.enable_gesture_engine()
device.power_up()

while True :
    gesture_data = []
    for i in range(device.get_number_of_datasets_in_fifo()):
        gesture_data.append(device.get_gesture_data())
    
    device_status = device.get_device_status()
    gesture_status = device.get_gesture_status()
    
    print("*** Device Status ***")
    for key, value in device_status.items():
        print(key, value)
    print("*** Gesture Status ***")
    for key, value in gesture_status.items():
        print(key, value)
    
    print("*** Gesture Data ***")
    print(process_gesture_data(gesture_data))
    print("\n\n")
    time.sleep(.1)
    
def process_gesture_data(data, tolerance = 25):
    #find peaks
    peaks = [-1]*4
    peaks_time = [-1]*4
    #and lows to detect
    lows = [100000] * 4
    for time_step, sample in enumerate(data):
        for i in range(4):
            if peaks[i] < sample[i]:
                peaks[i] = sample[i]
                peaks_time[i] = time_step
            if lows[i] > sample[i]:
                lows[i] = sample[i]
    
    up_down = 0
    if peak[0]-lows[0] > tolerance and peak[1] - lows[1] > tolerance:
        up_down = 1 if peaks_time[0] < peaks_time[1] else -1
    
    right_left = 0
    if peak[2]-lows[2] > tolerance and peak[3] - lows[3] > tolerance:
        right_left = -1 if peaks_time[2] < peaks_time[3] else 1
    
    if up_down == 0 and right_left == 0:
        return "No gesture detected"
    
    ud_string = "up" if up_down > 0 else "down"
    rl_string = "right" if right_left > 0 else "left"
    
    return "moved " + ud_string + " " + rl_string
    
    
    
                        
        
