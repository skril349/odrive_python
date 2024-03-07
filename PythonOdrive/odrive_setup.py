import odrive
from odrive.enums import *
import time

def setup_odrive():
    print("Finding an ODrive...")
    my_drive = odrive.find_any()

    print("Starting calibration...")
    my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    while my_drive.axis0.current_state != AXIS_STATE_IDLE:
        time.sleep(0.1)

    my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    my_drive.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
    my_drive.axis0.trap_traj.config.vel_limit = 50
    my_drive.axis0.trap_traj.config.accel_limit = 50
    my_drive.axis0.trap_traj.config.decel_limit = 50
    my_drive.axis0.motor.config.current_lim = 30
    my_drive.axis0.controller.config.vel_limit = 50

    return my_drive
