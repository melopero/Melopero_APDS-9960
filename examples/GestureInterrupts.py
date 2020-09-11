#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""

import gpiozero as gpio
import melopero_apds9960 as mp
from signal import pause


def main():
    device = mp.APDS_9960()

    # reset
    device.reset()

    device.enable_gestures_engine()

    # Setup the entry condition for the gesture engine
    device.set_gesture_prox_enter_threshold(100)
    device.set_gesture_exit_threshold(20)
    device.set_gesture_exit_persistence(mp.APDS_9960.EXIT_AFTER_4_GESTURE_END)

    # Setup interrupt settings
    device.enable_gesture_interrupts()
    device.set_gesture_fifo_threshold(mp.APDS_9960.FIFO_INT_AFTER_16_DATASETS)

    # Interrupt callback
    def on_interrupt():
        device.clear_gesture_engine_interrupts()
        n = device.get_number_of_datasets_in_fifo()
        print("There are {n} dataset in the fifo.")
        for i in range(n):
            print(device.get_gesture_data())
        print()


    device.wake_up()

    # Setup interrupt callback
    int_listener_pin = "GPIO4"
    interrupt = gpio.Button(int_listener_pin, pull_up=None, active_state=False)
    interrupt.when_pressed = on_interrupt

    pause()


if __name__ == '__main__':
    main()
