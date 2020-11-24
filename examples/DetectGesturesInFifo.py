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
    device.set_gesture_prox_enter_threshold(25)
    device.set_gesture_exit_threshold(20)
    device.set_gesture_exit_persistence(mp.APDS_9960.EXIT_AFTER_4_GESTURE_END)

    # Setup interrupt settings
    device.enable_gesture_interrupts()
    device.set_gesture_fifo_threshold(mp.APDS_9960.FIFO_INT_AFTER_16_DATASETS)

    # To clear the interrupt pin we have to read all datasets that are available in the fifo.
    # Since it takes a little bit of time to read alla these datasets the device may collect
    # new ones in the meantime and prevent us from clearing the interrupt ( since the fifo
    # would not be empty ). To prevent this behaviour we tell the device to enter the sleep
    # state after an interrupt occurred. The device will exit the sleep state when the interrupt
    # is cleared.
    device.set_sleep_after_interrupt(True)

    # Interrupt callback
    def on_interrupt():
        detected_gestures = device.parse_gesture_in_fifo()
        print(detected_gestures)

    device.wake_up()

    # Setup interrupt callback
    int_listener_pin = "GPIO4"
    interrupt = gpio.Button(int_listener_pin, pull_up=True, active_state=False)
    interrupt.when_pressed = on_interrupt

    pause()


if __name__ == '__main__':
    main()
