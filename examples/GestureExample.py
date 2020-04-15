#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""

import time
import melopero_apds9960 as mp

def main():
    device = mp.APDS_9960()
    last_gesture = ""
    
    #General settings
    device.set_sleep_after_interrupt(False)
    
    device.enable_proximity_engine()
    device.enable_gestures_engine()
    device.power_up()
    
    while True :
        prox_data = device.get_proximity_data()
        
        gesture_data = []
        for i in range(device.get_number_of_datasets_in_fifo()):
            gesture_data.append(device.get_gesture_data())
        
        device_status = device.get_device_status()
        gesture_status = device.get_gesture_status()
        
        print("*** Device Status ***")
        for key, value in device_status.items():
            print(key, value)
            
        print(f"Proximity Data: {prox_data}")
        print("*** Gesture Status ***")
        for key, value in gesture_status.items():
            print(key, value)
        
        curr_gesture = process_gesture_data(gesture_data)
        print("*** Gesture Data ***")
        print(f"gesture: {curr_gesture}")
        print(f"last gesture: {last_gesture}")
        print("\n\n")
        if curr_gesture != "No gesture detected":
            last_gesture = curr_gesture
        time.sleep(.1)
    
def process_gesture_data(data, tolerance = 25, time_tolerance = 5):
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
    if peaks[0]-lows[0] > tolerance and peaks[1] - lows[1] > tolerance and abs(peaks_time[0] - peaks_time[1]) > time_tolerance:
        up_down = 1 if peaks_time[0] < peaks_time[1] else -1
    
    right_left = 0
    if peaks[2]-lows[2] > tolerance and peaks[3] - lows[3] > tolerance and abs(peaks_time[2] - peaks_time[3]) > time_tolerance:
        right_left = -1 if peaks_time[2] < peaks_time[3] else 1
    
    if up_down == 0 and right_left == 0:
        return "No gesture detected"
    
    ud_string = "up" if up_down > 0 else "down"
    rl_string = "right" if right_left > 0 else "left"
    
    return "moved " + ud_string + " " + rl_string
    
    
if __name__ == "__main__":
    main()
        
