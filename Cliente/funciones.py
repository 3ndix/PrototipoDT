import paho.mqtt.client as mqtt
import json, datetime, time, clases

DISC = "!DISCONNECT"
data = ''

def recibir_data():
    def on_connect(client, userdata, flags, rc):
        client.subscribe("Sensores/#")

    def on_message(client, usserdata, msg):
        global data
        data = (msg.payload).decode('utf-8')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(host='mqtt.eclipseprojects.io', port=1883)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
    client.disconnect()

def pedir_data(op):
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883)
    client.publish("Conexion/Opcion", op)
    if op != DISC:
        recibir_data()
        if data != '':
            return json.loads(data)
        else: return 'ERROR'

def real_time(op):
    if op != 0:
        list_data = [pedir_data('1'), pedir_data('2')]
        return list_data
    else:
        dic_estado = pedir_data('3')
        obj = clases.Objeto_Fisico(dic_estado['agua'], dic_estado['eto'])
        etc, agua_req = obj.get_estado()
        return {'agua caida': obj.agua, 'evapo. ref. (ETo)':obj.eto,'evapo. (ETc)':etc, 'agua requerida':agua_req}

def guardar_decision(list_data):
    clases.Censado().insert_decision(clases.Decision(list_data).get_data())
    clases.Censado().close()

def enviar_decision(datos):
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883)
    client.publish("Conexion/Decision", json.dumps(datos))
    client.disconnect()
    list_data = []
    for key in datos:
        list_data.append(datos[key])
    guardar_decision(list_data)

def select_datos(col, limit, hora=''):
    list_data = clases.Censado().select_monitoreo(col, limit, hora)
    list_data2 = []
    for dato in list_data:
        try:
            list_data2.append(float(dato[0]))
        except:
            list_data2.append(dato[0])
    return list_data2

def select_datos2(col, limit):
    list_data = clases.Censado().select_estado(col, limit)
    list_data2 = []
    for dato in list_data:
        try:
            list_data2.append(float(dato[0]))
        except:
            list_data2.append(dato[0])
    return list_data2

def setear_texto(col):
    col = col.lower()
    col = col.replace('á','a')
    col = col.replace('é','e')
    col = col.replace('í','i')
    col = col.replace('ó','o')
    col = col.replace('ú','ú')
    col = col.replace(' ','_')
    return col

def medida_grafico(id_combobox, y_label):
    if id_combobox == 0: return y_label+" (°)"
    elif id_combobox == 1: return y_label+" (%)"
    elif id_combobox == 2: return y_label+" (mbar)"
    elif id_combobox == 3: return y_label+"(mm)"
    else: return y_label+"(W/m2)"

def setear_monitoreo(dict):
    list_data = []
    for key in dict:
        list_data.append(dict[key])
    list_data[1] = datetime.datetime.now()
    if len(list_data) < 7:
        for i in range(len(list_data),7):
            list_data.append('null')
    return list_data
    
def setear_estado(dict):
    list_data = [1, datetime.datetime.now()]
    for key in dict:
        list_data.append(dict[key])
    return list_data
    