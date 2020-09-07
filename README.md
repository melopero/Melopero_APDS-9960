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
