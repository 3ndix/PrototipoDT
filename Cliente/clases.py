import pymysql, datetime
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FG
import matplotlib.pyplot as plt

class Censado:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='Censado'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def insert_monitoreo(self, datos):
        sql = "INSERT INTO monitoreo (fk_sensor, mon_fecha, mon_temperatura, mon_humedad, mon_presion, mon_agua_caida, mon_radiacion_uv) \
            VALUES ({}, '{}', {}, {}, {}, {}, {});".format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5],datos[6])#datetime.datetime.now(),datos[1],datos[2],datos[3],datos[4],datos[5])
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise
    
    def insert_estado(self, datos):
        sql = "INSERT INTO estado (fk_sector, est_fecha, est_agua_caida, est_eto, est_etc, est_agua_req) \
            VALUES ({}, '{}', {}, {}, {}, {});".format(datos[0],datos[1],datos[2],datos[3],datos[4],datos[5])
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

    def insert_decision(self, datos):
        sql = "INSERT INTO decision (fk_sensor, dec_fecha, dec_tipo, dec_cant_agua, dec_fecha_riego) \
            VALUES ({}, '{}', '{}', {}, '{}');".format(datos[0], datos[1], datos[2], datos[3], datos[4])
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

    def select_monitoreo(self, col, limit, hora):
        if hora!='':
            sql = "SELECT " + col + " FROM monitoreo WHERE HOUR(mon_fecha) = " + hora + " AND fk_sensor = 1 ORDER BY id_monitoreo DESC LIMIT " + limit
        else:
            sql = "SELECT " + col + " FROM monitoreo WHERE fk_sensor = 1 ORDER BY id_monitoreo DESC LIMIT " + limit
        try:
            self.cursor.execute(sql)
            return list(self.cursor.fetchall())[::-1]
        except Exception as e:
            raise

    def select_estado(self, col, limit):
        sql = "SELECT " + col + " FROM estado ORDER BY id_estado DESC LIMIT " + limit
        try:
            self.cursor.execute(sql)
            return list(self.cursor.fetchall())[::-1]
        except Exception as e:
            raise

class Objeto_Fisico():
    def __init__(self, agua, eto):
        self.kc = 0.45
        self.agua = agua
        self.eto = eto #0.0023 * self.raduv * (self.tempMid + 17.8) * ((self.tempMax - self.tempMin)**(1/2))

    def get_estado(self):
        etc = round(self.eto * self.kc, 2)
        agua_req = round((etc - self.agua) / 0.9, 2)
        if agua_req <= 0:
            return etc, 0
        else:
            return etc, agua_req

class Decision():
    def __init__(self, list_data):
        self.fk_sensor = list_data[0]
        self.dec_fecha = datetime.datetime.now()
        self.dec_tipo = "Riego"
        self.dec_cant_agua = list_data[1]
        self.dec_fecha_riego = list_data[2]

    def get_data(self):
        return [self.fk_sensor, self.dec_fecha, self.dec_tipo, \
            self.dec_cant_agua, self.dec_fecha_riego]

class Visualizacion(FG):
    def __init__(self):
        self.fig, self.ax = plt.subplots(1, dpi=100, \
            figsize=(5,4), sharey=True, facecolor='white')
        super().__init__(self.fig)
        FG.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, \
            QtWidgets.QSizePolicy.Expanding)
        
        self.ax.grid(linestyle='--', alpha=0.5)
        self.ax.spines['top'].set_alpha(0.0)
        self.ax.spines['right'].set_alpha(0.0)
        self.plot = None

    def graficar(self, x, title, x_label, y_label, label1='', label2='', label3='', y='', y2='', y3=''):
        self.ax.clear()
        if y != '':
            self.ax.plot(x, y, marker='o', label=label1)
        if y2 != '':
            self.ax.plot(x, y2, marker='o', color='r', label=label2)
        if y3 != '':
            self.ax.plot(x, y3, marker='o', color='g', label=label3)
        self.ax.legend(loc='upper left')
        self.ax.grid(linestyle='--', alpha=0.5)
        self.ax.set_title(title, fontsize=10)
        self.ax.set_xlabel(x_label, fontsize=9)
        self.ax.set_ylabel(y_label, fontsize=9)
        self.ax.tick_params(axis='both', which='major', labelsize=7.5)
        self.ax.tick_params(axis='both', which='minor', labelsize=7.5)
        self.draw()

    def limpiar(self):
        self.ax.clear()
        self.ax.grid(linestyle='--', alpha=0.5)
        self.draw()
