#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""

import time
import melopero_apds9960 as mp


def main():
    device = mp.APDS_9960()

    # reset
    device.reset()

    device.enable_gestures_engine()

    device.set_gesture_prox_enter_threshold(25)
    device.set_gesture_exit_threshold(20)
    device.set_gesture_exit_persistence(mp.APDS_9960.EXIT_AFTER_4_GESTURE_END)

    device.wake_up()

    while True:
        gesture_status = device.get_gesture_status()
        if gesture_status["Gesture FIFO Data"]:
            # try to detect and parse a gesture for 300 milliseconds
            detected_gestures = device.parse_gesture(300)
            print(detected_gestures)


if __name__ == "__main__":
    main()
