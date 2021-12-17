from sense_emu import SenseHat
import pandas as pd
import datetime

sense = SenseHat()

class Sensor_air():
    def __init__(self):
        datos = []
        df = pd.read_excel('sensor.xlsx')
        fechas = df['tiempo']
        fecha_hoy = datetime.datetime.now()
        ct = 0
        for fecha in fechas:
            fecha = datetime.datetime.strptime(fecha, '%d-%m-%Y %H:%M')
            if fecha.day == fecha_hoy.day and \
               fecha.hour == fecha_hoy.hour:
                for dato in df: datos.append(df[dato][ct])
                break
            else: ct+=1
        self.id = 1
        self.tipo = "Sensor de Aire"
        self.temperatura = float(datos[1])
        self.humedad = float(datos[2])
        self.presion = float(datos[3])
        self.agua_caida = float(datos[4])
        self.radiacion_uv = float(datos[5])
        
                
class Sensor_soil():
    def __init__(self):
        self.id = 2
        self.tipo = "Sensor de Suelo"
        self.temp = round(sense.temp, 2)
        self.humd = round(sense.humidity, 2)
