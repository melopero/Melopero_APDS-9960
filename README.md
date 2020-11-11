# Melopero_APDS-9960

## Install

To install the module, open a terminal and run this command:
```pip3 install melopero-apds9960```  

## Introduction 

The sensor is made up of four different 'engines':

- Proximity Engine

- Gesture Engine

- Color/Als Engine

- Wait Engine

The sensor works like a state machine where each engine represents a state. There are also the SLEEP and IDLE state.  
The states are entered sequentially in the order depicted below:

![States](/images/states.png)

## How to use

Importing the module and device object creation:

```python
import melopero_apds9960 as mp

device = mp.APDS_9960()
# Alternatively you can specify which i2c bus and address to use
device = mp.APDS_9960(i2c_addr=MY_ADDRESS, i2c_bus=MY_BUS)

# Reset device : Disables all engines and enters the SLEEP state
device.reset()
```

Enabling/Disabling the engines:

```python
device.enable_proximity_engine(enable=True)
device.enable_als_engine(enable=True)
device.enable_gesture_engine(enable=True)
device.enable_wait_engine(enable=True)
```

### General Device Methods

To toggle between the low consumption SLEEP state and the operating IDLE state:  

```python
device.wake_up(True) # Enter IDLE state
device.wake_up(False) # Enter SLEEP state
```

Other general methods:  

```python
device.set_sleep_after_interrupt(True)
# Enters SLEEP state after an interrupt occurred

device.set_led_drive(led_drive)
# Sets the LED drive strength. Must be one of mp.APDS_9960.LED_DRIVE_N_mA

device.set_led_boost(led_boost)
# The LED_BOOST allows the LDR pin to sink more current above the maximum settings. Must be
# one of mp.APDS_9960.LED_BOOST_N (where N is the percentage).

device.get_status()
# Returns a dictionary containing information about the device status.
```

### Proximity engine

To read the last measured proximity value (to update the proximity values the engine must be enabled):

```python
device.get_proximity_data()
# Returns a value ranging from 0 (far) to 255 (near)
```

#### Proximity interrupts

```python
device.enable_proximity_interrupts(enable=True)

device.clear_proximity_interrupts()

device.set_proximity_interrupt_thresholds(low, high) 
# The Proximity Interrupt Threshold sets the high and low trigger points for the comparison
# function which generates an interrupt. If the value generated by the proximity channel,
# crosses below the lower threshold or above the higher threshold, an interrupt may be
# signaled to the host processor.

device.set_proximity_interrupt_persistence(persistance)
# The Interrupt Persistence sets a value which is compared with the accumulated amount
# Proximity cycles in which results were outside threshold values. Any Proximity result
# that is inside threshold values resets the count.
```

#### Advanced settings

```python
device.set_proximity_gain(prox_gain)
# prox_gain must be one of mp.APDS_9960.PROXIMITY_GAIN_NX

device.set_proximity_pulse_count_and_length(pulse_count, pulse_length)
# The proximity pulse count is the number of pulses to be output on the LDR pin. The proximity
# pulse length is the amount of time the LDR pin is sinking current during a proximity pulse.
# pulse_count must be in range [1-64] and pulse_length must be one of mp.APDS_9960.
# PULSE_LEN_N_MICROS
```

### Gesture engine

The sensor enters the gesture engine state only if the proximity measurement is over a certain threshold.

```python
device.set_gesture_prox_enter_threshold(enter_thr) # Sets the enter threshold

device.set_gesture_exit_threshold(exit_thr) # Sets the exit threshold

device.set_gesture_exit_persistence(persistence)
# Sets number of consecutive measurements that have to be below the exit threshold
# to exit the gesture state.  

device.set_gesture_exit_mask(mask_up, mask_down, mask_left, mask_right)
# Controls which of the gesture detector photodiodes (UDLR) will be included to
# determine a “gesture end” and subsequent exit of the gesture state machine

# This methods are NOT meant to be called every measurement... they are called just
# once to set the gesture engine state enter and exit condition

# To make sure the gesture engine state is always entered you can set both thresholds to 0
device.set_gesture_prox_enter_threshold(0)
device.set_gesture_exit_threshold(0)
```

The gesture data is made of datasets of four bytes that represent the values of the UDLR photodiodes.
The gesture data is stored in a FIFO queue and can be retrieved with the following methods:  

```python
n = device.get_number_of_datasets_in_fifo()

for i in range(n):
    dataset = device.get_gesture_data() # Reads the first dataset in the queue
    print(dataset)
```

Other general methods:

```python
device.is_gesture_engine_running()

device.get_gesture_status() 
# Returns a dictionary containing data about the gesture engine status
```

#### Gesture interrupts

```python
device.enable_gesture_interrupts()

device.set_gesture_fifo_threshold(fifo_thr)
# if the number of datasets in the FIFO exceeds the given threshold an interrupt is generated.

device.reset_gesture_engine_interrupt_settings()
```

#### Advanced settings

There are several other methods (similar to the proximity engine) to tweak the gesture engine's settings.

### Color/Als engine

To read the last measured color value (to update the color values the engine must be enabled):

```python
device.get_color_data()
# Returns the last measured ARGB values (Alfa Red Green Blue) as 16 bit integers
```

The maximum values for the ARGB values depends on the saturation value which depends on the color engine's settings. To normalize the color values :

```python
# First set the Color engine settigns
# ....
# ....

# Then retrieve the saturation value
saturation = device.get_saturation()

raw_data = device.get_color_data() # the raw data retrieved from the sensor 16 bit uints
normalized_data = list(map(lambda v : v / saturation, raw_data)) # values range from 0 to 1
byte_format = list(map(lambda v : v * 255, normalized_data)) # values range from 0 to 255
```

#### Color/Als interrupts

```python
device.enable_als_interrupts()

device.set_als_thresholds(low, high)
# if clear channel data is less than low or greater than high an interrupt is generated.

device.set_als_interrupt_persistence(persistence)
# Sets the number of measurements that meet the interrupt conditions to generate an interrupt.

device.clear_als_interrupts()
```

#### Advanced settings

```python
device.set_als_gain(als_gain)
# als_gain must be one of mp.APDS_9960.ALS_GAIN_NX

device.set_als_integration_time(wtime)
# the internal integration time of ALS/Color analog to digital converters.
# If in a low light environment a longer integration time may lead to
# better results.
```

### Wait engine

To set the wait time you can use:

```python
device.set_wait_time(wtime, long_wait=False)
# This is the time that will pass between two cycles.The wait time should be
# configured before the proximity and the als engines get enabled.
# wtime: the time value in milliseconds. Must be between 2.78ms and 712ms
# long_wait = False: If true the wait time is multiplied by 12.
```
