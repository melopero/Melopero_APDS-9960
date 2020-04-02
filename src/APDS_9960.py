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
    INTERRUPT_PERSISTANCE_REG_ADDRESS = 0x8C
    
    #Proximity Registers Addresses
    PROX_INT_LOW_THR_REG_ADDRESS = 0x89
    PROX_INT_HIGH_THR_REG_ADDRESS = 0x8B
    PROX_PULSE_COUNT_REG_ADDRESS = 0x8E
    PROX_UP_RIGHT_OFFSET_REG_ADDRESS = 0x9D
    PROX_DOWN_LEFT_OFFSET_REG_ADDRESS = 0x9E
    PROX_DATA_REG_ADDRESS = 0x9C
    
    #ALS Register Addresses
    ALS_ATIME_REG_ADDRESS = 0x81
    ALS_INT_LOW_THR_LOW_BYTE_REG_ADDRESS = 0x84 #This register provides the low byte of the low interrupt threshold.
    ALS_INT_LOW_THR_HIGH_BYTE_REG_ADDRESS = 0x85 #This register provides the high byte of the low interrupt threshold.
    ALS_INT_HIGH_THR_LOW_BYTE_REG_ADDRESS = 0x86 #This register provides the low byte of the high interrupt threshold.
    ALS_INT_HIGH_THR_HIGH_BYTE_REG_ADDRESS = 0x87 #This register provides the high byte of the high interrupt threshold.
    
    CLEAR_DATA_LOW_BYTE_REG_ADDRESS = 0x94 #Low Byte of clear channel data.
    CLEAR_DATA_HIGH_BYTE_REG_ADDRESS = 0x95 #High Byte of clear channel data.
    RED_DATA_LOW_BYTE_REG_ADDRESS = 0x96 #Low Byte of red channel data.
    RED_DATA_HIGH_BYTE_REG_ADDRESS = 0x97 #High Byte of red channel data.
    GREEN_DATA_LOW_BYTE_REG_ADDRESS = 0x98 #Low Byte of green channel data.
    GREEN_DATA_HIGH_BYTE_REG_ADDRESS = 0x99 #High Byte of green channel data.
    BLUE_DATA_LOW_BYTE_REG_ADDRESS = 0x9A #Low Byte of blue channel data.
    BLUE_DATA_HIGH_BYTE_REG_ADDRESS = 0x9B #High Byte of blue channel data.
    
    #Wait Registers Addresses
    WAIT_TIME_REG_ADDRESS = 0x83
    
    #Proximity pulse lengths
    PROX_PULSE_LEN_4_MICROS = 0
    PROX_PULSE_LEN_8_MICROS = 1
    PROX_PULSE_LEN_16_MICROS = 2
    PROX_PULSE_LEN_32_MICROS = 3
    
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
        
    # =========================================================================
    #     Proximity Engine Methods
    # =========================================================================
    def enable_proximity_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 2)
        
    def enable_proximity_interrupts(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 5)
        
    def set_proximity_interrupt_thresholds(self, low_thr, high_thr):
        """The Proximity Interrupt Threshold sets the high and low trigger points
        for the comparison function which generates an interrupt. If the value 
        generated by the proximity channel, crosses below the lower threshold 
        or above the higher threshold, an interrupt may be signaled to the host 
        processor. Interrupt generation is subject to the value set in 
        persistence.\n
        :low_thr: the low trigger point value.\n
        :high_thr: the high trigger point value. \n
        """
        self.write_byte_data(low_thr, APDS_9960.PROX_INT_LOW_THR_REG_ADDRESS)
        self.write_byte_data(high_thr, APDS_9960.PROX_INT_HIGH_THR_REG_ADDRESS)
    
    def set_proximity_interrupt_persistence(self, persistence):
        """The Interrupt Persistence sets a value which is compared with the 
        accumulated amount Proximity cycles in which results were outside 
        threshold values. Any Proximity result that is inside threshold values 
        resets the count.\n
        :persistence: int in range [0-15] \n
            0 : an interrupt is triggered every cycle.\n
            N > 0 : an interrupt is triggered after N results over the threshold.
        """
        if not (0 <= persistence <= 15):
            raise ValueError("persistance must be in range [0-15]")
        
        flag = []
        for i in range(4):
            flag.append(bool(persistence & (1 << i)))
        self.write_flag_data(flag, APDS_9960.INTERRUPT_PERSISTANCE_REG_ADDRESS, 4)
    
    def set_proximity_pulse_count_and_length(self, pulse_count, 
                                             pulse_length = PROX_PULSE_LEN_8_MICROS):
        """The proximity pulse count is the number of pulses to be output on
        the LDR pin. The proximity pulse length is the amount of time the LDR 
        pin is sinking current during a proximity pulse.\n
        :pulse_count: must be in range [1-64]\n
        :pulse_length: must be one of APDS_9960.PROX_PULSE_LEN_N_MICROS.
        """
        if not (1 <= pulse_count <= 64):
            raise ValueError("pulse_count must be in range [1-64]")
        if not (APDS_9960.PROX_PULSE_LEN_4_MICROS <= pulse_length 
                <= APDS_9960.PROX_PULSE_LEN_32_MICROS):
            raise ValueError("pulse_length must be one of APDS_9960.PROX_PULSE_LEN_N_MICROS")

        reg_value = pulse_length << 6
        reg_value |= pulse_count - 1
        self.write_byte_data(reg_value, APDS_9960.PROX_PULSE_COUNT_REG_ADDRESS)
        
    def set_proximity_offset(self, up_right_offset = 0, down_left_offset = 0):
        """In proximity mode, the UP and RIGHT and the DOWN and LEFT
        photodiodes are connected forming diode pairs. The offset is an 8-bit 
        value used to scale an internal offset correction factor to compensate 
        for crosstalk in the application.\n
        :up_right_offset: the up-right pair offset.\n
        :down_left_offset: the down-left pair offset.\n
        """
        if not (-127 <= up_right_offset <= 127 and -127 <= down_left_offset <= 127):
            raise ValueError("up_right_offset and down_left_offset must be in range [-127-127]")
        
        ur_reg_value = abs(up_right_offset)
        ur_reg_value |= 0x80 if up_right_offset < 0 else 0x00
        self.write_byte_data(ur_reg_value, APDS_9960.PROX_UP_RIGHT_OFFSET_REG_ADDRESS)
        dl_reg_value = abs(down_left_offset)
        dl_reg_value |= 0x80 if down_left_offset < 0 else 0x00
        self.write_byte_data(dl_reg_value, APDS_9960.PROX_DOWN_LEFT_OFFSET_REG_ADDRESS)
        
    def get_proximity_data(self):
        return self.read_byte_data(APDS_9960.PROX_DATA_REG_ADDRESS)
    
    # =========================================================================
    #     Gestures Engine Methods
    # =========================================================================
    def enable_gestures_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 6)
    
    # =========================================================================
    #     ALS Engine Methods
    # =========================================================================
    def enable_als_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 1)
        
    def enable_als_interrupts(self, enable = True):
        self.write_flag_dat([enable], APDS_9960.ENABLE_REG_ADDRESS, 4)
        
    def set_als_thresholds(self, low_thr, high_thr):
        """ALS level detection uses data generated by the Clear Channel.
        The ALS Interrupt Threshold registers provide 16-bit values to be used 
        as the high and low thresholds for comparison to the 16-bit CDATA values.
        If AIEN is enabled and CDATA is greater than AILTH/AIHTH or less than 
        AILTL/AIHTL for the number of consecutive samples specified in APERS
        an interrupt is asserted on the interrupt pin.\n
        :low_thr: the lower threshold value must be a 16 bit unsigned int\n
        :high_thr: the higher threshold value must be a 16 bit unsigned int
        """
        if not (0 <= low_thr <= 0xFFFF and 0 <= high_thr <= 0xFFFF):
            raise ValueError("low_thr and high_thr must be in range [0 - 0xFFFF]")
        
        ailtl = low_thr & 0xFF
        ailth = low_thr >> 8
        aihtl = high_thr & 0xFF
        aihth = high_thr >> 8
        self.write_byte_data([ailtl, ailth, aihtl, aihth], APDS_9960.ALS_INT_LOW_THR_LOW_BYTE_REG_ADDRESS)
        
    def set_als_interrupt_persistance(self, persistence):
        """The Interrupt Persistence sets a value which is compared with the 
        accumulated amount of ALS cycles in which results were outside threshold 
        values. Any Proximity or ALS result that is inside threshold values resets
        the count.\n
        :persistence: ALS Interrupt Persistence. Controls rate of Clear channel 
            interrupt to the host processor. Must be in range [0 - 15]:
                0 = Every ALS cycle\n
                1 = Any ALS value outside of threshold range\n
                2 = 2 consecutive ALS values out of range\n
                3 = 3 consecutive ALS values out of range\n
                N > 3 = (N - 3) * 5 consecutive ALS values out of range\n
        """
        if not (0 <= persistence <= 15):
            raise ValueError("Persistence must be in range [0 - 15]")
        
        flag = []
        for i in range(4):
            flag.append(bool(persistence & (1 << i)))
        self.write_flag_data(flag, APDS_9960.INTERRUPT_PERSISTANCE_REG_ADDRESS)
    
    def set_als_integration_time(self, wtime):
        """The ATIME register controls the internal integration time of 
        ALS/Color analog to digital converters. The maximum count (or saturation) 
        value can be calculated based upon the integration time and the size of 
        the count register (i.e. 16 bits). For ALS/Color, the maximum count 
        will be the lesser of either:
            65535 (based on the 16 bit register size) or
            The result of equation: CountMAX = 1025 x CYCLES\n
        :wtime: the integration time in millis must be in range [2.78 - 712]
        """
        if not (2.78 <= wtime <= 712):
            raise ValueError("The integration time must be in range [2.78 - 712] millis.")
            
        value = 256 - int(wtime / 2.78)
        self.write_byte_data(value, APDS_9960.ALS_ATIME_REG_ADDRESS)
        
    def get_color_data(self):
        """Red, green, blue, and clear data is stored as 16-bit values.\n
        Returns : The data is returned as 4 element list: [clear, red, green, blue]. 
        """
        color = []
        data = self.read_byte_data(APDS_9960.CLEAR_DATA_LOW_BYTE_REG_ADDRESS, 8)
        for i in range(4):
            channel_low = data[2 * i]
            channel_high = data[2 * i + 1]
            color.append((channel_high << 8) | channel_low)
        return color
    
    # =========================================================================
    #     Wait Engine Methods
    # =========================================================================
    def enable_wait_engine(self, enable = True):
        self.write_flag_data([enable], APDS_9960.ENABLE_REG_ADDRESS, 3)
        
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
    
    
        