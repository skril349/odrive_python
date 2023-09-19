import odrive
from odrive.enums import *
import time
import math
import pandas as pd

# Create lists to store data
timestamps = []
positions = []
intensities = []
voltages = []
torques = []
# Find a connected ODrive (this will block until you connect one)
print("Finding an ODrive...")
my_drive = odrive.find_any()

# Calibrate motor and wait for it to finish
print("Starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ

# Main loop for data collection
t0 = time.monotonic()
setpoint = 40
try:
    while True:
        
        position = my_drive.axis0.encoder.pos_estimate
        intensity = my_drive.axis0.motor.current_control.Iq_measured
        voltage = my_drive.vbus_voltage
        torque = ((8.27*my_drive.axis0.motor.current_control.Iq_setpoint/150) * 100)

        # Append data to lists
        timestamps.append(time.monotonic() - t0)
        positions.append(position)
        intensities.append(intensity)
        voltages.append(voltage)
        torques.append(torque)
        # Set the position setpoint
        my_drive.axis0.controller.input_pos = setpoint

        time.sleep(0.01)
        current_state = my_drive.axis0.current_state

        if current_state == AXIS_STATE_CLOSED_LOOP_CONTROL:
            if abs(position - setpoint) < 0.05:
                print("El motor ha llegado a la posición deseada.")
                setpoint=0
            else:
                print("El motor está en control en bucle cerrado pero no ha llegado a la posición deseada.")
        else:
            print("El motor no está en control en bucle cerrado.")

except KeyboardInterrupt:
    pass

# Create a DataFrame to store the data
data = {
    'Timestamp': timestamps,
    'Position': positions,
    'Intensity': intensities,
    'Voltage': voltages
}

df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
file_name = 'odrive_data.xlsx'
df.to_excel(file_name, index=False, engine='openpyxl')
print(f"Data saved to {file_name}")

# Clean up and close the ODrive connection
my_drive.axis0.requested_state = AXIS_STATE_IDLE
my_drive.axis0.controller.input_pos = 0.0
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.input_pos = 0.0
