import paho.mqtt.client as mqtt
import clases, json, datetime
import pandas as pd

def pub_sensor(op):    
    client = mqtt.Client()
    client.connect('mqtt.eclipseprojects.io', 1883)
    if op == '3':
        client.publish("Sensores/"+op, get_dataETC())
    else:
        client.publish("Sensores/"+op, get_data(int(op)))

def get_data(tipo):
    if tipo == 1:
        sensor = clases.Sensor_air()
        sensor_dic = vars(sensor)
        return json.dumps(sensor_dic)
    
    if tipo == 2:
        sensor = clases.Sensor_soil()
        sensor_dic = vars(sensor)
        return json.dumps(sensor_dic)

def get_dataETC():
    etc = {}
    df = pd.read_excel('calculo_etc.xlsx')
    fechas = df['tiempo']
    fecha_hoy = datetime.datetime.now()
    ct = 0
    for fecha in fechas:
        fecha = datetime.datetime.strptime(fecha, '%d-%m-%Y')
        if fecha.day == fecha_hoy.day:
            etc['eto'] = df['Eto'][ct]
            etc['agua'] = df['agua'][ct-1]
            break
        else: ct+=1
    return json.dumps(etc)