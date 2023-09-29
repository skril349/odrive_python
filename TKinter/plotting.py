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
    publish.single(mqtt_topic_odrive, str(texto), hostname=mqtt_host, port=mqtt_port, qos=2, retain=True)

# Función de callback cuando se recibe un mensaje MQTT en el tópico "data"
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode("utf-8")
        data_dict = eval(data)
        if isinstance(data_dict, dict) and "timestamp" in data_dict and "position" in data_dict:
            timestamps.append(data_dict["timestamp"])
            positions.append(data_dict["position"])
            # Actualiza el gráfico en tiempo real
            grafico.clear()
            grafico.plot(timestamps, positions)
            grafico.set_xlabel("Tiempo")
            grafico.set_ylabel("Posición")
            grafico.set_title("Gráfico en Tiempo Real")
            canvas.draw()
    except Exception as e:
        print("Error al procesar mensaje MQTT:", str(e))

# Configuración del cliente MQTT
mqtt_client = mqtt.Client("tkinter_mqtt_client")
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_host, mqtt_port)
mqtt_client.subscribe(mqtt_topic_data)
mqtt_client.loop_start()

# Creación de la interfaz de usuario con Tkinter
root = tk.Tk()
root.title("Envío a ODrive y Gráfico en Tiempo Real")

frame = ttk.Frame(root)
frame.grid(row=0, column=0)

texto_label = ttk.Label(frame, text="Texto a enviar a ODrive:")
texto_label.grid(row=0, column=0)

texto_input = ttk.Entry(frame)
texto_input.grid(row=0, column=1)

enviar_button = ttk.Button(frame, text="Enviar a ODrive", command=enviar_a_odrive)
enviar_button.grid(row=0, column=2)

# Configuración para el gráfico en tiempo real
fig, grafico = plt.subplots()
grafico.set_xlabel("Tiempo")
grafico.set_ylabel("Posición")
grafico.set_title("Gráfico en Tiempo Real")
timestamps = []
positions = []

# Integrar el gráfico en la ventana de Tkinter usando FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0)

# Inicia la interfaz gráfica
root.mainloop()
