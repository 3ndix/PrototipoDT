import sys, datetime
import funciones as fun
import clases as cl
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QDoubleValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QDialog


class HMI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Plantillas/HMI Digital Twin.ui", self)
        self.setFixedSize(1105,900)
        self.setWindowTitle("HMI Digital Twin")

        self.canvas = cl.Visualizacion()
        self.canvas2 = cl.Visualizacion()
        self.grafico1.addWidget(self.canvas)
        self.grafico2.addWidget(self.canvas2)
        self.data = []
        self.fecha_accion.setMinimumDateTime(datetime.datetime.now())

        self.radio_monitoreo.setChecked(True)
        self.radio_dia.setChecked(True)
        self.btn_limpiar.setEnabled(False)
        self.btn_limpiar2.setEnabled(False)
        self.btn_limpiar3.setEnabled(False)
        self.btn_limpiar4.setEnabled(False)
        self.btn_almacenar.setEnabled(False)
        self.limite2.setEnabled(False)
        self.id_consulta.setEnabled(False)
        self.id_accion.setEnabled(False)
        self.hora2.setEnabled(False)
        self.btn_vermapa.setEnabled(False)

        self.id_consulta.setValidator(QIntValidator())
        self.hora.setValidator(QIntValidator())
        self.id_accion.setValidator(QIntValidator())
        self.hora2.setValidator(QIntValidator())
        self.cant_agua.setValidator(QDoubleValidator())
        self.limite.setValidator(QIntValidator())
        
        self.box_accion.currentIndexChanged.connect(self.bloquear_accion)
        self.box_consulta.currentIndexChanged.connect(self.bloquear_datos)
        self.btn_consulta.clicked.connect(self.data_realtime)
        self.btn_accion.clicked.connect(self.recibe_accion)
        self.btn_limpiar.clicked.connect(self.limpiar_tabla)
        self.btn_limpiar2.clicked.connect(self.limpiar_grafico1)
        self.btn_limpiar3.clicked.connect(self.limpiar_grafico2)
        self.btn_limpiar4.clicked.connect(self.limpiar_accion)
        self.btn_almacenar.clicked.connect(self.almacenar_datos)
        self.check_etc.clicked.connect(self.bloquear_grafico2)
        self.check_agua.clicked.connect(self.bloquear_grafico2)
        self.check_agua2.clicked.connect(self.bloquear_grafico2)
        self.check_etc.clicked.connect(self.verificacion_grafico2)
        self.check_agua.clicked.connect(self.verificacion_grafico2)
        self.check_agua2.clicked.connect(self.verificacion_grafico2)
        self.limite2.textChanged.connect(self.verificacion_grafico2)
        self.limite.textChanged.connect(self.verificacion_grafico)
        self.box_grafico1.currentIndexChanged.connect(self.verificacion_grafico)
        self.hora.textChanged.connect(self.verificacion_grafico)
        self.radio_hora.clicked.connect(self.bloquear_dias)
        self.radio_dia.clicked.connect(self.bloquear_dias)
        self.hora2.textChanged.connect(self.verificacion_grafico)
        self.btn_vermapa.clicked.connect(self.ver_mapa)
        self.box_consulta.currentIndexChanged.connect(lambda: self.btn_vermapa.setEnabled(False))

    def ver_mapa(self):
        winimg = Window_Img()
        if self.box_consulta.currentIndex() == 0:
            self.img = QPixmap("IMGs/hacienda_chada.png")
        else:
            self.img = QPixmap("IMGs/hacienda_chada_sector" + str(self.id_consulta.text()) + ".png")
        winimg.imagen.setPixmap(self.img)
        winimg.show()
        winimg.exec()

    def mensaje_alerta(self, text):
        alerta = QMessageBox()
        alerta.setWindowTitle('¡Atención!')
        alerta.setText(text)
        alerta.exec()

    def verificacion_grafico(self):
        if self.radio_dia.isChecked():
            if self.limite.text():
                self.graficar()
            else:
                self.limpiar_grafico1()
        else:
            if self.hora2.text():
                self.graficar()
            else:
                self.limpiar_grafico1()

    def verificacion_grafico2(self):
        if self.limite2.text():
            self.graficar2()
        else:
            self.limpiar_grafico2()

    def bloquear_accion(self):
        if self.box_accion.currentIndex() == 0:
            self.id_accion.clear()
            self.id_accion.setEnabled(False)
        else:
            self.id_accion.setEnabled(True)

    def bloquear_datos(self):
        if self.box_consulta.currentIndex() == 0:
            self.id_consulta.clear()
            self.id_consulta.setEnabled(False)
        else:
            self.id_consulta.setEnabled(True)
        
    def graficar2(self):
        if self.limite2.text():
            try:
                if int(self.limite2.text()) >= 1 and int(self.limite2.text()) <= 31:
                    x = list(range(1,int(self.limite2.text())+1))
                    x_label = "Días"
                    if self.check_etc.isChecked() and self.check_agua.isChecked() and self.check_agua2.isChecked():
                        y_label = 'ETc, Agua Requerida y Caída'
                        y = fun.select_datos2('est_etc', str(self.limite2.text()))
                        y2 = fun.select_datos2('est_agua_req', str(self.limite2.text()))
                        y3 = fun.select_datos2('est_agua_caida', str(self.limite2.text()))
                        title = "ETc, Agua Requerida y Caída vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        self.canvas2.graficar(x, title, x_label, y_label, label1="ETc", \
                            label2="Agua Req.", label3="Agua Caída", y=y, y2=y2, y3=y3)

                    elif self.check_etc.isChecked() and self.check_agua.isChecked():
                        y_label = 'ETc y Agua Requerida'
                        y = fun.select_datos2('est_etc', str(self.limite2.text()))
                        y2 = fun.select_datos2('est_agua_req', str(self.limite2.text()))
                        title = "ETc y Agua Requerida vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label1="ETc", label2="Agua Req.", y=y, y2=y2)
                        self.canvas2.graficar(x, title, x_label, y_label, label1="ETc", label2="Agua Req.", y=y, y2=y2)

                    elif self.check_etc.isChecked() and self.check_agua2.isChecked():
                        y_label = 'ETc y Agua Caída'
                        y = fun.select_datos2('est_etc', str(self.limite2.text()))
                        y2 = fun.select_datos2('est_agua_caida', str(self.limite2.text()))
                        title = "ETc y Agua Caída vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label1="ETc", label3="Agua Caída", y=y, y3=y2)
                        self.canvas2.graficar(x, title, x_label, y_label, label1="ETc", label3="Agua Caída", y=y, y3=y2)

                    elif self.check_agua.isChecked() and self.check_agua2.isChecked():
                        y_label = 'Agua Requerida y Caídia'
                        y = fun.select_datos2('est_agua_req', str(self.limite2.text()))
                        y2 = fun.select_datos2('est_agua_caida', str(self.limite2.text()))
                        title = "Agua Requerida y Caída vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label2="Agua Req.", label3="Agua Caída", y2=y, y3=y2)
                        self.canvas2.graficar(x, title, x_label, y_label, label2="Agua Req.", label3="Agua Caída", y2=y, y3=y2)

                    elif self.check_etc.isChecked():
                        y_label = 'ETc'
                        y = fun.select_datos2('est_etc', str(self.limite2.text()))
                        title = "ETc vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label1="ETc", y=y)
                        self.canvas2.graficar(x, title, x_label, y_label, label1="ETc", y=y)

                    elif self.check_agua.isChecked():
                        y_label = 'Agua Requerida'
                        y = fun.select_datos2('est_agua_req', str(self.limite2.text()))
                        title = "Agua Requerida vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label2="Agua Req.", y2=y)
                        self.canvas2.graficar(x, title, x_label, y_label, label2="Agua Req.", y2=y)

                    else:
                        y_label = 'Agua Caída'
                        y = fun.select_datos2('est_agua_caida', str(self.limite2.text()))
                        title = "Agua Caída vs Días\nÚltimos " + str(self.limite2.text()) + " Días"
                        #fun.graficar_2(self.canvas2, x, title, x_label, y_label, label3="Agua Caída", y3=y)
                        self.canvas2.graficar(x, title, x_label, y_label, label3="Agua Caída", y3=y)

                    self.btn_limpiar3.setEnabled(True)
                else:
                    self.mensaje_alerta('Cantidad de Días Incorrecta (Límite 31)')
                    self.limite2.clear()
            except ValueError:
                self.mensaje_alerta("Valor Incorrecto")
                self.limite2.clear()
        else:
            self.mensaje_alerta('Debe Ingresar una Cantidad de Días')

    def limpiar_grafico2(self):
        self.canvas2.limpiar()
        self.limite2.clear()
        self.btn_limpiar3.setEnabled(False)

    def bloquear_grafico2(self):
        if self.check_etc.isChecked() or self.check_agua.isChecked() or self.check_agua2.isChecked():
            self.limite2.setEnabled(True)
        else:
            self.limite2.setEnabled(False)
            self.limite2.clear()
            self.limpiar_grafico2()

    def bloquear_dias(self):
        if self.radio_hora.isChecked():
            self.limite.clear()
            self.limite.setEnabled(False)
            self.hora.setEnabled(False)
            self.hora2.setEnabled(True)
            self.limpiar_grafico1()
        else:
            self.limite.setEnabled(True)
            self.hora.setEnabled(True)
            self.hora2.setEnabled(False)
            self.limpiar_grafico1()

    def graficar(self):
        if self.canvas.plot:
            self.canvas.ax.clear()
        if self.radio_dia.isChecked():
            if self.limite.text():
                try:
                    if int(self.limite.text()) <= 31 and int(self.limite.text()) >= 1:
                        x = list(range(1,int(self.limite.text())+1))
                        y_label = fun.medida_grafico(int(self.box_grafico1.currentIndex()), str(self.box_grafico1.currentText()))
                        col = fun.setear_texto(str(self.box_grafico1.currentText()))
                        x_label = "Días"
                        if self.hora.text():
                            if int(self.hora.text()) >= 0 and int(self.hora.text()) <= 23:
                                y = fun.select_datos('mon_'+col, str(self.limite.text()), self.hora.text())
                                title = str(self.box_grafico1.currentText()) + " v/s Días\nÚltimos " + str(self.limite.text()) + \
                                    " Días a las " + str(self.hora.text()) + ":00 Hrs."
                                self.canvas.graficar(x, title, x_label, y_label, label1=self.box_grafico1.currentText(), y=y)
                            else:
                                self.mensaje_alerta('Hora Ingresada Incorrecta (rango = 00 - 23)')
                                self.hora.clear()
                        else:
                            y = fun.select_datos('mon_'+col, str(self.limite.text()), str(datetime.datetime.now().hour))
                            title = str(self.box_grafico1.currentText()) + " v/s Días\nÚltimos " + str(self.limite.text()) + \
                                    " Días a las " + str(datetime.datetime.now().hour) + ":00 Hrs."
                            self.canvas.graficar(x, title, x_label, y_label, label1=self.box_grafico1.currentText(), y=y)
                    else:
                        self.mensaje_alerta('Cantidad de Días Incorrecta (Límite 31)')
                        self.limite.clear()
                except ValueError:
                    self.mensaje_alerta("Valor Incorrecto")
                    self.limite.clear()
                    self.hora.clear()
            else:
                self.mensaje_alerta('Debe Ingresar una Cantidad de Días')
        else:
            if self.hora2.text():
                try:
                    if int(self.hora2.text()) <= 48 and int(self.hora2.text()) >= 1:
                        x = list(range(1,int(self.hora2.text())+1))
                        y_label = fun.medida_grafico(int(self.box_grafico1.currentIndex()), str(self.box_grafico1.currentText()))
                        col = fun.setear_texto(str(self.box_grafico1.currentText()))
                        title = str(self.box_grafico1.currentText()) + " v/s Horas\nÚltimas " + str(self.hora2.text()) + " Horas"
                        x_label = "Horas"
                        y = fun.select_datos('mon_'+col, str(self.hora2.text()))
                        self.canvas.graficar(x, title, x_label, y_label, label1=self.box_grafico1.currentText(), y=y)
                    else:
                        self.mensaje_alerta('Cantidad de Horas Incorrecta (Límite 48)')
                except ValueError:
                    self.mensaje_alerta("Valor Incorrecto")
                    self.hora2.clear()
            else:
                self.mensaje_alerta('Debe Ingresar una Cantidad de Horas')
                self.hora2.clear()
        self.btn_limpiar2.setEnabled(True)

    def limpiar_grafico1(self):
        self.canvas.limpiar()
        self.limite.clear()
        self.hora.clear()
        self.hora2.clear()
        self.btn_limpiar2.setEnabled(False)
    
    def verificar_decision(self, win, fecha_dec):
        dic_decision = {'id_dsipositivo':1, 'cant_agua':float(self.cant_agua.text()), 'momento_riego':str(fecha_dec)}
        fun.enviar_decision(dic_decision)
        win.close()
        
    def recibe_accion(self):
        win_dec = Window_Dec()
        win_dec.setFixedSize(400,240)
    
        fecha_dec = self.fecha_accion.dateTime().toPyDateTime()
        if self.box_accion.currentIndex() == 1 and self.id_accion.text() != '':
            try:
                if int(self.id_accion.text()) == 1:
                    if self.cant_agua.text() != '':
                        if float(self.cant_agua.text()) > 0:
                            if fecha_dec > datetime.datetime.now():
                                win_dec.show()
                                win_dec.label_decision.setText("Riego de " + self.cant_agua.text()+ " Litros en el Sector " + self.id_accion.text() \
                                    + "\nel " + fecha_dec.strftime("%d-%m-%Y") + " a las " + fecha_dec.strftime("%H:%M"))
                                win_dec.btn_aceptar.clicked.connect(lambda: self.verificar_decision(win_dec, fecha_dec))
                                win_dec.btn_salir.clicked.connect(lambda: win_dec.close())
                                self.btn_limpiar4.setEnabled(True)
                            else:
                                self.mensaje_alerta('La fecha ingresada es incorrecta')
                        else:
                            self.mensaje_alerta('Opción Inválida')
                            self.cant_agua.clear()
                    else:
                        self.mensaje_alerta('Debe ingresa la cantidad de agua')
                else:
                    self.mensaje_alerta('Opción Inválida')
                    self.id_accion.clear()
            except ValueError:
                self.mensaje_alerta('Opción Inválida')
                self.id_accion.clear()

        elif self.box_accion.currentIndex() == 0:
            if self.cant_agua.text() != '':
                try:
                    if float(self.cant_agua.text()) > 0:
                        if fecha_dec > datetime.datetime.now():
                            win_dec.show()
                            win_dec.label_decision.setText("Riego de " + self.cant_agua.text()+ " Litros en Todo el cultivo" \
                                + "\nel " + fecha_dec.strftime("%d-%m-%Y") + " a las " + fecha_dec.strftime("%H:%M"))
                            win_dec.btn_aceptar.clicked.connect(lambda: self.verificar_decision(win_dec, fecha_dec))
                            win_dec.btn_salir.clicked.connect(lambda: win_dec.close())
                            self.btn_limpiar4.setEnabled(True)
                        else:
                            self.mensaje_alerta('La fecha ingresada es incorrecta')
                    else:
                        self.mensaje_alerta('Opción Inválida')
                        self.cant_agua.clear()
                except ValueError:
                    self.mensaje_alerta('Opción Inválida')
                    self.cant_agua.clear()
            else:
                self.mensaje_alerta('Debe ingresa la cantidad de agua')
        else:
            self.mensaje_alerta('Debe ingresar un ID')

    def limpiar_accion(self):
        self.id_accion.clear()
        self.cant_agua.clear()
        self.fecha_accion.setDateTime(datetime.datetime.now())
        self.btn_limpiar4.setEnabled(False)

    def data_realtime(self):
        self.tabla_datos.clear()
        if self.radio_monitoreo.isChecked():
            if self.box_consulta.currentIndex() == 0:
                list_data = fun.real_time(1)
                self.data = list_data
                self.tabla_datos.setRowCount(len(list_data)+1)
                col_len = 0
                for dato in list_data:
                    if col_len < len(dato):
                        col_len = len(dato)
                self.tabla_datos.setColumnCount(col_len)
                row = 0
                num = 0
                for dato in list_data:
                    num = 0
                    for key in dato:
                        if row == 0:
                            self.tabla_datos.setItem(row, num, QtWidgets.QTableWidgetItem(str(key).replace('_', ' ').title()))
                            self.tabla_datos.setItem(row+1, num, QtWidgets.QTableWidgetItem(str(dato[key])))
                        else: 
                            self.tabla_datos.setItem(row+1, num, QtWidgets.QTableWidgetItem(str(dato[key])))
                        num+=1
                    row+=1
                self.btn_almacenar.setEnabled(True)
                self.btn_limpiar.setEnabled(True)
                self.btn_vermapa.setEnabled(True)

            elif self.box_consulta.currentIndex() == 1 and self.id_consulta.text() != "":
            # AGREGAR VALIDADOR SOBRE SECTORES DISPONIBLES (Conectar con BD?)
                try:
                    if int(self.id_consulta.text()) == 1:
                        list_data = fun.real_time(1)
                        self.data = list_data
                        self.tabla_datos.setRowCount(len(list_data)+1)
                        col_len = 0
                        for dato in list_data:
                            if col_len < len(dato):
                                col_len = len(dato)
                        self.tabla_datos.setColumnCount(col_len)
                        row = 0
                        num = 0
                        for dato in list_data:
                            num = 0
                            for key in dato:
                                if row == 0:
                                    self.tabla_datos.setItem(row, num, QtWidgets.QTableWidgetItem(str(key).replace('_', ' ').title()))
                                    self.tabla_datos.setItem(row+1, num, QtWidgets.QTableWidgetItem(str(dato[key])))
                                else:
                                    self.tabla_datos.setItem(row+1, num, QtWidgets.QTableWidgetItem(str(dato[key])))
                                num+=1
                            row+=1
                        self.btn_almacenar.setEnabled(True)
                        self.btn_limpiar.setEnabled(True)
                        self.btn_vermapa.setEnabled(True)
                    else:
                        self.mensaje_alerta('Opción Inválida')
                        self.id_consulta.clear()
                except ValueError:
                    self.mensaje_alerta('Opción Inválida')
                    self.id_consulta.clear()
            else:
                self.mensaje_alerta('Debe ingresar un ID')

        elif self.radio_estado.isChecked():
            if self.box_consulta.currentIndex() == 1 and self.id_consulta.text() != "":
                try:
                    if int(self.id_consulta.text()) == 1:
                        list_data = fun.real_time(0)
                        self.data = list_data
                        self.tabla_datos.setRowCount(2)
                        self.tabla_datos.setColumnCount(len(list_data))
                        row = 0
                        num = 0
                        for key in list_data:
                            if row == 0:
                                self.tabla_datos.setItem(0, num, QtWidgets.QTableWidgetItem(str(key).replace('_', ' ').title()))
                                self.tabla_datos.setItem(1, num, QtWidgets.QTableWidgetItem(str(list_data[key])))
                            num+=1
                        self.btn_almacenar.setEnabled(True)
                        self.btn_limpiar.setEnabled(True)
                        self.btn_vermapa.setEnabled(True)
                    else:
                        self.mensaje_alerta('Opción Inválida')
                        self.id_consulta.clear()
                except ValueError:
                    self.mensaje_alerta('Opción Inválida')
                    self.id_consulta.clear()

            elif self.box_consulta.currentIndex() == 0:
                list_data = fun.real_time(0)
                self.data = list_data
                self.tabla_datos.setRowCount(2)
                self.tabla_datos.setColumnCount(len(list_data))
                row = 0
                num = 0
                for key in list_data:
                    if row == 0:
                        self.tabla_datos.setItem(0, num, QtWidgets.QTableWidgetItem(str(key).replace('_', ' ').title()))
                        self.tabla_datos.setItem(1, num, QtWidgets.QTableWidgetItem(str(list_data[key])))
                    num+=1
                self.btn_almacenar.setEnabled(True)
                self.btn_limpiar.setEnabled(True)
                self.btn_vermapa.setEnabled(True)
            else:
                self.mensaje_alerta('Debe ingresa un ID')

    def almacenar_datos(self):
        try:
            if self.radio_monitoreo.isChecked():
                for i in range(len(self.data)):
                    cl.Censado().insert_monitoreo(fun.setear_monitoreo(self.data[i]))
            else:
                cl.Censado().insert_estado(fun.setear_estado(self.data))
            self.mensaje_alerta('Registros Almacenados con Éxito!!')
            self.btn_almacenar.setEnabled(False)
        except:
            self.mensaje_alerta("Hubo un error al intentar almacenar los datos")

    def limpiar_tabla(self):
        self.id_consulta.clear()
        self.tabla_datos.clear()
        self.tabla_datos.setRowCount(0)
        self.tabla_datos.setColumnCount(0)
        self.btn_limpiar.setEnabled(False)

class Window_Dec(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Plantillas/Decision.ui", self)
        self.setWindowTitle("ATENCIÓN!")

class Window_Img(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("Plantillas/Imagen.ui", self)
        self.setWindowTitle("Mapa Hacienda Chada")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    hmi = HMI()
    hmi.show()
    sys.exit(app.exec_())