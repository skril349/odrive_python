import tkinter as tk
from tkinter import ttk
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configuración MQTT
mqtt_host = "tonivivescabaleiro.com"
mqtt_port = 1883
mqtt_topic_odrive = "odrive"
mqtt_topic_data = "data"

# Función para enviar el texto por MQTT
def enviar_a_odrive():
    texto = texto_input.get()
    publish.single(mqtt_topic_odrive, texto, hostname=mqtt_host, port=mqtt_port, qos=2, retain=True)

# Función de callback cuando se recibe un mensaje MQTT en el tópico "data"
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode("utf-8")
        data_dict = eval(data)
        if isinstance(data_dict, dict) and "timestamp" in data_dict and "position" in data_dict and "intensity" in data_dict and "voltage" in data_dict and "torque" in data_dict:
            timestamps.append(data_dict["timestamp"])
            positions.append(data_dict["position"])
            intensities.append(data_dict["intensity"])
            voltages.append(data_dict["voltage"])
            torques.append(data_dict["torque"])
            
            # Actualiza los gráficos en tiempo real
            actualizar_graficos()
    except Exception as e:
        print("Error al procesar mensaje MQTT:", str(e))

# Función para actualizar los gráficos en tiempo real
def actualizar_graficos():
    ax_posicion.clear()
    ax_posicion.plot(timestamps, positions)
    ax_posicion.set_xlabel("Tiempo")
    ax_posicion.set_ylabel("Posición")
    ax_posicion.set_title("Posición en Tiempo Real")
    
    ax_intensidad.clear()
    ax_intensidad.plot(timestamps, intensities)
    ax_intensidad.set_xlabel("Tiempo")
    ax_intensidad.set_ylabel("Intensidad")
    ax_intensidad.set_title("Intensidad en Tiempo Real")
    
    ax_voltaje.clear()
    ax_voltaje.plot(timestamps, voltages)
    ax_voltaje.set_xlabel("Tiempo")
    ax_voltaje.set_ylabel("Voltaje")
    ax_voltaje.set_title("Voltaje en Tiempo Real")
    
    ax_torque.clear()
    ax_torque.plot(timestamps, torques)
    ax_torque.set_xlabel("Tiempo")
    ax_torque.set_ylabel("Torque")
    ax_torque.set_title("Torque en Tiempo Real")
    
    canvas.draw()

# Configuración del cliente MQTT
mqtt_client = mqtt.Client("tkinter_mqtt_client")
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_host, mqtt_port)
mqtt_client.subscribe(mqtt_topic_data)
mqtt_client.loop_start()

# Creación de la interfaz de usuario con Tkinter
root = tk.Tk()
root.title("Envío a ODrive y Gráficos en Tiempo Real")

frame = ttk.Frame(root)
frame.grid(row=0, column=0)

texto_label = ttk.Label(frame, text="Texto a enviar a ODrive:")
texto_label.grid(row=0, column=0)

texto_input = ttk.Entry(frame)
texto_input.grid(row=0, column=1)

enviar_button = ttk.Button(frame, text="Enviar a ODrive", command=enviar_a_odrive)
enviar_button.grid(row=0, column=2)

download_button = ttk.Button(frame, text="descargar datos")
download_button.grid(row=0, column=3)

# Configuración para los gráficos en tiempo real
fig, axs = plt.subplots(4, 1, figsize=(6, 8), sharex=True)
fig.subplots_adjust(hspace=0.5)

ax_posicion = axs[0]
ax_intensidad = axs[1]
ax_voltaje = axs[2]
ax_torque = axs[3]

timestamps = []
positions = []
intensities = []
voltages = []
torques = []

# Integrar los gráficos en la ventana de Tkinter usando FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0)

# Inicia la interfaz gráfica
root.mainloop()
