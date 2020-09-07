#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""

import time
import melopero_apds9960 as mp

def main():
    device = mp.APDS_9960()

    device.reset()

    device.enable_proximity_engine()
    device.power_up()
    print(device.get_status())
    while True:
        time.sleep(.5)
        print(device.get_proximity_data())


if __name__ == "__main__":
    main()
