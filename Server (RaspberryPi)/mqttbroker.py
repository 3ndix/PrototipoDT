import paho.mqtt.client as mqtt
import funciones

DISC = "!DISCONNECT"

data = ''
topic = ''

def wait_data():
    def on_connect(client, userdata, flags, rc):
        client.subscribe("Conexion/#")
    def on_message(client, usserdata, msg):
        global topic
        global data
        topic = msg.topic[9:]
        data = (msg.payload).decode('utf-8')
        print(data)
        
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect('mqtt.eclipseprojects.io', 1883)
    client.loop_start()

    conn = True
    while conn:
        if data != '':
            conn = False
            break
    client.loop_stop()
    client.disconnect()
    
    
while True:
    wait_data()
    if data == DISC:
        print("Servidor desconectado")
        break
    if topic == "Decision":
        print("Acción recibida")
        topic = ''
        data = ''
    else:
        funciones.pub_sensor(data)
        data = ''

