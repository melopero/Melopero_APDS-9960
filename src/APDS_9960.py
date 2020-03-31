#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Leonardo La Rocca
"""
from smbus2 import SMBusWrapper


class APDS_9960():
    
    DEFAULT_I2C_ADDRESS = 0x39
    
    #Register addresses
    ENABLE_REG_ADDRESS = 0x80
    CONFIG_1_REG_ADDRESS = 0x8D
    
    #Proximity Registers Addresses
    
    #Wait Registers Addresses
    WAIT_TIME_REG_ADDRESS = 0x83
    
    def __init__(self, i2c_address = DEFAULT_I2C_ADDRESS, i2c_bus = 1):
        self.i2c_address = i2c_address
        self.i2c_bus = i2c_bus
    
    def read_byte_data(self, register_address, amount = 1):
        """Read a byte (or multiple bytes) from the device.\n
        :register_address: the adress where the read operation starts.\n
        :amount = 1: the amount of bytes to read, by default it is 1.\n
        Return value: an int if the amount is 1, a list of ints if the amount is greater than 1.\n
        """
        with SMBusWrapper(self.i2c_bus) as bus:
            data = bus.read_i2c_block_data(self.i2c_address, register_address, amount)
        if amount == 1:
            return data[0]
        else :
            return data
    
    def write_byte_data(self, value, register_address):
        """Write a byte (or multiple bytes) to the device.\n
        :value: The value to write to the register. Can also be a list of values.\n
        :register_address: the address where the write operation starts.\n
        """
        if type(value) != list:
            value = [value]
        with SMBusWrapper(self.i2c_bus) as bus:
            bus.write_i2c_block_data(self.i2c_address, register_address, value)
            
    def write_flag_data(self, flag, register_address, offset):
        """Writes a flag to a register with the given offset.\n
        :flag: A list of booleans
        :register_address: the address at which to write the flag
        :offset: the offset inside the register
        """
        if len(flag) + offset > 8:
            raise ValueError("Flag + offset exceeded 8 bit limit.")
            
        register_value = self.read_byte_data(register_address)
        for index, value in enumerate(flag):
            if value:
                register_value |= value << (index + offset)
            else :
                register_value &= value << (index + offset)
        self.write_byte_data(register_value, register_address)
            
    def set_power_up(self, power_up = True):
        """Toggles between IDLE and SLEEP state. In sleep state the device can 
        still receive and process I2C messages.\n
        :power_up = True: Enter the IDLE state if True else enter SLEEP state, by default the value is True.
        """
        self.write_flag_data([power_up], APDS_9960.ENABLE_REG_ADDRESS, 0)
        
    def enable_all_engines_and_power_up(self, enable = True):
        """Note: calling this function resets also the Proximity and ALS
        interrupt settings."""
        value = 0b01001111 if enable else 0
        self.write_byte_data(value, APDS_9960.ENABLE_REG_ADDRESS)
    
    def enable_proximity_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 2)
    
    def enable_gestures_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 6)
    
    def enable_als_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 1)
    
    def enable_wait_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 3)
        
    def enable_proximity_interrupts(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 5)
        
    def enable_als_interrupts(self, enable = True):
        self.write_flag_dat([enable], APDS_9960.ENABLE_REG_ADDRESS, 4)
        
    def set_wait_time(self, wtime, long_wait = False):
        """Sets the wait time in WTIME register. This is the time that will pass
        between two cycles.The wait time should be configured before the proximity 
        and the als engines get enabled.\n
        :wtime: the time value in millisenconds. Must be between 2.78ms and 712ms\n
        :long_wait = False: If true the wait time is multiplied by 12.\n
        """
        if not (2.78 <= wtime <= 712):
            raise ValueError("The wait time must be between 2.78 ms and 712 ms")
        
        #long_wait
        self.write_flag_data([long_wait], APDS_9960.CONFIG_1_REG_ADDRESS, 1)
        #wtime
        reg_value = 256 - int(wtime / 2.78)
        self.write_byte_data(reg_value, APDS_9960.WAIT_TIME_REG_ADDRESS)
    
    
        