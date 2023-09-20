import time
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from odrive_setup import setup_odrive
from plotter import update_plot
from collections import deque

# Configuración de ODrive y MQTT
my_drive = setup_odrive()
# Configura tu cliente MQTT
global value

received_message = False  # Bandera para controlar si se ha recibido un mensaje


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("odrive")
    client.subscribe("data")

def on_message(client, userdata, msg):
    global received_message  # Usamos la bandera global
    #print("Mensaje recibido -> " + msg.topic + " " + str(msg.payload))
    global message_payload  # Almacenamos el valor del mensaje
    global setpoint
    message_payload = msg.payload
    if msg.topic == "odrive":
        setpoint = float(message_payload.decode("utf-8"));

        received_message = True  # Cambiamos la bandera a True cuando se recibe un mensaje

client = mqtt.Client("digi_mqtt_test")
client.on_connect = on_connect
client.on_message = on_message

client.connect('tonivivescabaleiro.com', 1883)

client.loop_start()  # Usamos loop_start() en lugar de loop_forever()

# Mantén el bucle hasta que se reciba un mensaje
while received_message == False:
    pass  # Espera hasta que received_message sea True


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

try:
    
    while True: 
        position = my_drive.axis0.encoder.pos_estimate
        position2 = my_drive.axis0.motor.I_bus

        intensity = my_drive.axis0.motor.current_control.Iq_measured
        voltage = my_drive.vbus_voltage
        torque = ((8.27*my_drive.axis0.motor.current_control.Iq_setpoint/150) * 100)
        # Append data to lists
        timestamps.append(time.monotonic() - t0)
        positions.append(position)
        intensities.append(intensity)
        voltages.append(voltage)
        torques.append(torque)
     
        data_queue.append(positions[-1])

        update_plot(timestamps[-max_data_points:], data_queue, intensities[-max_data_points:],
                    voltages[-max_data_points:], torques[-max_data_points:], ax1, ax2, ax3, ax4)
        

        data_to_publish={
        "timestamp":(time.monotonic() - t0),
        "position":position,
        "intensity":intensity,
        "voltage" :voltage,
        "torque" :torque
        }
        client.publish("data", str(data_to_publish))


        plt.pause(0.01)


        
        if received_message == True:
            
            # Update the plot
           
            # Set the position setpoint
            my_drive.axis0.controller.input_pos = setpoint

            current_state = my_drive.axis0.current_state

           
            if my_drive.axis0.controller.trajectory_done:
                received_message = False
                if setpoint == 0:
                    final_data_to_publish={
                    "timestamp":timestamps,
                    "position":positions,
                    "intensity":intensities,
                    "voltage" :voltages,
                    "torque" :torques
                    }
                    client.publish("finalData", str(final_data_to_publish))
                    received_message = False



except KeyboardInterrupt:
    pass