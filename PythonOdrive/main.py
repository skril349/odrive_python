import time
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from odrive_setup import setup_odrive
from plotter import update_plot
from collections import deque
from mqtt_setup import setup_mqtt, get_received_message, set_received_message, get_setpoint
import datetime

# Configuración de ODrive y MQTT
my_drive = setup_odrive()
client = setup_mqtt()
plot_or_not = False
# Mantén el bucle hasta que se reciba un mensaje
while get_received_message() == False:
    pass  # Espera hasta que get_received_message() sea True


# Configuración del gráfico en tiempo real
max_data_points = 50
data_queue = deque(maxlen=max_data_points)
timestamps = []
positions = []
intensities = []
voltages = []
torques = []

# Enabling interactive mode for real-time plotting
plt.ion()
# Create a figure for plotting
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(10, 8))

# Main loop for data collection and plotting
t0 = time.monotonic()
i = 0
n = 0
try:
 #infinite loop   
    while True: 
        position = my_drive.axis1.encoder.pos_estimate
        position2 = my_drive.axis1.motor.I_bus

        intensity = my_drive.axis1.motor.current_control.Iq_measured
        voltage = my_drive.vbus_voltage
        torque = ((8.27*my_drive.axis1.motor.current_control.Iq_setpoint/150) * 100)
        # Append data to lists
        timestamps.append(time.monotonic() - t0)
        positions.append(position)
        intensities.append(intensity)
        voltages.append(voltage)
        torques.append(torque)

        data_to_publish={
        "timestamp":(time.monotonic() - t0),
        "position":position,
        "intensity":intensity,
        "voltage" :voltage,
        "torque" :torque
        }
        client.publish("data", str(data_to_publish))
     
        data_queue.append(positions[-1])
        if len(intensities) > max_data_points:
            intensities.pop(0)
            voltages.pop(0)
            torques.pop(0)
            positions.pop(0)
            timestamps.pop(0)

        update_plot(timestamps[-max_data_points:], data_queue, intensities[-max_data_points:],
                        voltages[-max_data_points:], torques[-max_data_points:], ax1, ax2, ax3, ax4)

        plt.pause(0.01)
  
        if get_received_message() == True:
            # Update the plot
            
            # Set the position setpoint
            my_drive.axis1.controller.input_pos = get_setpoint()

            current_state = my_drive.axis1.current_state
           
           
            if my_drive.axis1.controller.trajectory_done:

                set_received_message(False)
                if get_setpoint() == 0:
                    final_data_to_publish={
                    "timestamp":timestamps,
                    "position":positions,
                    "intensity":intensities,
                    "voltage" :voltages,
                    "torque" :torques
                    }
                    client.publish("finalData", str(final_data_to_publish))
                    set_received_message(False)

except KeyboardInterrupt:
    pass