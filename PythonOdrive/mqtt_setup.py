import paho.mqtt.client as mqtt

message_payload = None
setpoint = 0.0  # Puedes inicializarlo con un valor predeterminado
received_message = False  # Inicializa la variable en este módulo

def on_connect(client, userdata, flags, rc):
    print("Connected with result code {0}".format(str(rc)))
    client.subscribe("odrive", qos=2)
    client.subscribe("data", qos=2)

def on_message(client, userdata, msg):
    global message_payload  # Almacenamos el valor del mensaje
    global setpoint
    global received_message
    message_payload = msg.payload
    if msg.topic == "odrive":
        setpoint = float(message_payload.decode("utf-8"));
        received_message = True  # Cambiamos la bandera a True cuando se recibe un mensaje
        #print(received_message)
    
def setup_mqtt():
    client = mqtt.Client("digi_mqtt_test")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('tonivivescabaleiro.com', 1883)
    client.loop_start()

    return client  # Devuelve el cliente MQTT, no la variable received_message

def get_received_message():  # Función para obtener el valor de received_message
    return received_message

def set_received_message(value):  # Función para obtener el valor de received_message
    received_message = value;

def get_setpoint():  # Función para obtener el valor de setpoint
    return setpoint

def set_setpoint(value):  # Función para obtener el valor de setpoint
    setpoint = value;
