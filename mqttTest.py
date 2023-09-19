import paho.mqtt.client as mqtt

received_message = False  # Bandera para controlar si se ha recibido un mensaje

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("Temperatura")

def on_message(client, userdata, msg):
    global received_message  # Usamos la bandera global
    print("Mensaje recibido -> " + msg.topic + " " + str(msg.payload))
    received_message = True  # Cambiamos la bandera a True cuando se recibe un mensaje

client = mqtt.Client("digi_mqtt_test")
client.on_connect = on_connect
client.on_message = on_message

client.connect('tonivivescabaleiro.com', 1883)

client.loop_start()  # Usamos loop_start() en lugar de loop_forever()

# Mantén el bucle hasta que se reciba un mensaje
while not received_message:
    pass  # Espera hasta que received_message sea True

print("Hola")  # Imprime "Hola" cuando se recibe un mensaje
