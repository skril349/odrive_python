import paho.mqtt.publish as publish

# Configuración del servidor MQTT
mqtt_host = "tonivivescabaleiro.com"  # Cambia esto al servidor MQTT que desees utilizar
mqtt_port = 1883  # Puerto MQTT
mqtt_topic = "odrive"  # Tópico MQTT

# Obtén el dato que deseas enviar por la terminal
while True:
    dato_a_enviar = input("Introduce el dato que deseas enviar por MQTT: ")

    # Configura las opciones de publicación MQTT
    mqtt_qos = 2  # Calidad de servicio QoS 2
    mqtt_retain = True  # Retain establecido como True

    # Publica el dato en el servidor MQTT
    publish.single(mqtt_topic, dato_a_enviar, hostname=mqtt_host, port=mqtt_port, qos=mqtt_qos, retain=mqtt_retain)

    print(f"Dato '{dato_a_enviar}' enviado a '{mqtt_topic}' con QoS 2 y Retain=True.")
