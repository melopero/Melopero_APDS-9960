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
    device.enter_immediately_gesture_engine()
    device.wake_up()

    while True:
        for i in range(device.get_number_of_datasets_in_fifo()):
            print(device.get_gesture_data())


if __name__ == "__main__":
    main()
