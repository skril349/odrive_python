#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Calibrate motor and wait for it to finish
print("starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
my_drive.axis0.controller.input_pos = 3.14
print("Position setpoint is " + str(my_drive.axis0.controller.pos_setpoint))

# And this is how function calls are done:
for i in [1,2,3,4]:
    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))

# A sine wave to test
t0 = time.monotonic()
setpoint = 40
while True:
   
    print("position = " + str(int(setpoint)) + ", intensity = " + str(my_drive.axis0.motor.current_control.Iq_measured)+", voltage = " + str(my_drive.vbus_voltage))
    my_drive.axis0.controller.input_pos = setpoint
    current_state = my_drive.axis0.current_state
    position = my_drive.axis0.encoder.pos_estimate
    intensity = my_drive.axis0.motor.current_control.Iq_measured
    voltage = my_drive.vbus_voltage
    torque = ((8.27*my_drive.axis0.motor.current_control.Iq_setpoint/150) * 100)

    if current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
        if abs(position - setpoint) < 0.05:
        
            print("El motor ha llegado a la posición deseada.")
            setpoint=0
            

            
        else:
            pass
    else:
        print("El motor no está en control en bucle cerrado.")
