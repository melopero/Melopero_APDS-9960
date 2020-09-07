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

    device.enable_als_engine()
    device.set_als_integration_time(450)
    saturation = device.get_saturation()
    device.power_up()

    while True:
        time.sleep(.5)
        color = device.get_color_data()
        color = map(lambda val : val / saturation * 255, color)
        print(f"Alfa: {next(color)}  Red: {next(color)}  Green: {next(color)}  Blue: {next(color)}")


if __name__ == "__main__":
    main()
