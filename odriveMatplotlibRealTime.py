import odrive
from odrive.enums import *
import time
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt

# Configura tu cliente MQTT
global value

received_message = False  # Bandera para controlar si se ha recibido un mensaje



# Find a connected ODrive (this will block until you connect one)
print("Finding an ODrive...")
my_drive = odrive.find_any()


# Calibrate motor and wait for it to finish
print("Starting calibration...")
my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

while (my_drive.axis0.current_state) != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.config.input_mode = INPUT_MODE_TRAP_TRAJ
my_drive.axis0.trap_traj.config.vel_limit = 100
my_drive.axis0.trap_traj.config.accel_limit = 50
my_drive.axis0.trap_traj.config.decel_limit = 50
my_drive.axis0.motor.config.current_lim = 30
my_drive.axis0.controller.config.vel_limit = 100


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("Odrive")

def on_message(client, userdata, msg):
    global received_message  # Usamos la bandera global
    print("Mensaje recibido -> " + msg.topic + " " + str(msg.payload))
    global message_payload  # Almacenamos el valor del mensaje
    message_payload = msg.payload
    received_message = True  # Cambiamos la bandera a True cuando se recibe un mensaje
client = mqtt.Client("digi_mqtt_test")
client.on_connect = on_connect
client.on_message = on_message

client.connect('tonivivescabaleiro.com', 1883)

client.loop_start()  # Usamos loop_start() en lugar de loop_forever()

# Mantén el bucle hasta que se reciba un mensaje
while not received_message:
    pass  # Espera hasta que received_message sea True

print("Valor del mensaje recibido: "+ str(message_payload.decode("utf-8")) )

setpoint = float(message_payload.decode("utf-8"));

# Enabling interactive mode for real-time plotting
plt.ion()

# Create lists to store data for plotting
timestamps = []
positions = []
intensities = []
voltages = []
torques = []
positions2=[]


# Create a figure for plotting
fig, (ax1, ax2, ax3, ax4,ax5) = plt.subplots(5, 1, figsize=(10, 8))

# Main loop for data collection and plotting
t0 = time.monotonic()
i = 0


try:
    while i<2:
        position = my_drive.axis0.encoder.pos_estimate
        position2 = my_drive.axis0.motor.I_bus

        intensity = my_drive.axis0.motor.current_control.Iq_measured
        voltage = my_drive.vbus_voltage
        torque = ((8.27*my_drive.axis0.motor.current_control.Iq_setpoint/150) * 100)
        # Append data to lists
        timestamps.append(time.monotonic() - t0)
        positions.append(position)
        positions2.append(position2)
        intensities.append(intensity)
        voltages.append(voltage)
        torques.append(torque)

        # Update the plot
        ax1.clear()
        ax1.plot(timestamps, positions, label='Position')
        ax1.set_ylabel('Position')
        ax1.legend()

        ax2.clear()
        ax2.plot(timestamps, intensities, label='Intensity')
        ax2.set_ylabel('Intensity')
        ax2.legend()

        ax3.clear()
        ax3.plot(timestamps, voltages, label='Voltage')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Voltage')
        ax3.legend()

        ax4.clear()
        ax4.plot(timestamps, torques, label='Torque')
        ax4.set_xlabel('Time')
        ax4.set_ylabel('Torque (N.cm)')
        ax4.legend()
        
        ax5.clear()
        ax5.plot(timestamps, positions2, label='Position2')
        ax5.set_ylabel('Position2')
        ax5.legend()

        plt.pause(0.01)

        # Set the position setpoint
        my_drive.axis0.controller.input_pos = setpoint

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

# Clean up and close the ODrive connection
my_drive.axis0.requested_state = AXIS_STATE_IDLE
my_drive.axis0.controller.input_pos = 0.0
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
my_drive.axis0.controller.input_pos = 0.0
plt.ioff()
plt.show()
