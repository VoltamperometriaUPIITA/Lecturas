# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 22:08:30 2020

@author: ADOLFO
"""
import spidev
import time 
import RPi.GPIO as GPIO
import numpy as np

spi = spidev.SpiDev()
spi.open(0,0)
ev1 = 12
ev2 = 13
bom= 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(ev1, GPIO.OUT)
GPIO.setup(ev2, GPIO.OUT)
GPIO.setup(bom, GPIO.OUT)

def analogRead(pin):
    spi.max_speed_hz = 1350000
    adc = spi.xfer2([1,(8+pin) << 4,0])
    lec = ((adc[1]&3) << 8) + adc[2]
    return lec
# while True:
#     lectura = analogRead(0)
#     if lectura > 850:
#         GPIO.output(led, 1)
#     else:
#         GPIO.output(led, 0)
         
#     print(lectura)
#     sleep(0.1)
class Circuito_Hidraulico:
    def __init__(self):
        self.activo=True
        time.sleep(0.2)
        
    def Llenar(self):
        print("Llenando contenedores ...")
        
        GPIO.output(bom, 1)          # ACTIVA BOMBA
        GPIO.output(ev1, 1)         # ABRE ELECTROVALVULA INTERMEDIA
        GPIO.output(ev2, 0)          # CIERRA ELECTROVALVULA FINAL
        time.sleep(float(5))
        GPIO.output(bom, 0)          # DESACTIVA BOMBA
        GPIO.output(ev1, 0)          # CIERRA ELECTROVALVULA INTERMEDIA
        GPIO.output(ev2, 0)          # CIERRA ELECTROVALVULA FINAL
        print("Los contenedores estan llenos ...")
    def Drenar(self):
        print("Los contenedores se estan drenando ...")
        GPIO.output(bom, 0)          # DESACTIVA BOMBA
        GPIO.output(ev1, 1)          # ABRE ELECTROVALVULA INTERMEDIA
        GPIO.output(ev2, 1)          # ABRE ELECTROVALVULA FINAL
        time.sleep(float(7))
        print("¡ Listo ! Los contenedores estan vacios")
        GPIO.output(ev1, 0)          # CIERRA ELECTROVALVULA INTERMEDIA
        GPIO.output(ev2, 0)          # CIERRA ELECTROVALVULA FINAL
    def Automatico(self):
        self.Llenar()
        print("Se estan trazando los voltagramas ...")
        time.sleep(float(1))
        print("Se estan midiendo los parametros fiscoquimicos ...")
        time.sleep(float(1))
        print("Espere unos segundos ...")
        time.sleep(float(10))
        print("¡ LISTO ! Ya puede visualizar los resultados ...")
        time.sleep(float(2))
        self.Drenar()
        time.sleep(float(2))
        print("\n")
    def Voltagrama_Automatico(self):
        circuito.Llenar()
        time.sleep(float(1))
        print("Se estan trazando los voltagramas ...")
        print("Espere unos segundos ...")
        time.sleep(float(10))
        print("¡ LISTO ! Ya puede visualizar los VOLTAGRAMAS ...")
        time.sleep(float(2))
        circuito.Drenar()
        time.sleep(float(2))
        print("\n")
    def Parametros_Automatico(self):
        circuito.Llenar()
        print("Se estan midiendo los Parametros fiscoquimicos ...")
        print("Espere unos segundos ...")
        time.sleep(float(10))
        print("¡ LISTO ! Ya puede visualizar los valores de los sensores ...")
        time.sleep(float(21))
        circuito.Drenar()
        time.sleep(float(2))
        print("\n")
    def Cerrar_Sesion(self):
        circuito.activo=False
        print("CERRANDO SESION ...")
        time.sleep(float(5))
        print("¡ HASTA PRONTO !")
        time.sleep(float(5))
    
    #####    FIN DE LA CLASE      ######### 
class Parametros_Fisicoquimicos:
    def __init__(self):
        self.activo=True  
        self.pH=0
        self.ORP=0
        self.ce=0       
        time.sleep(0.2)
    def medir_pH(self):
        self.volt_ph=[]
        self.t_ph=[]
        ti=0
        for i in range(21):
            p=analogRead(0)*(5/1023)
            self.t_ph.append(ti)
            self.volt_ph.append(p)
            print("%.1f %.3f" %(ti,p))
            time.sleep(0.2)
            ti += 0.2
        self.pH=sum(self.volt_ph)/len(self.volt_ph)
        time.sleep(1.0)

    def medir_ORP(self):
        self.volt_ORP=[]
        self.t_ORP=[]
        ti=0
        for i in range(21):
            p=analogRead(1)*(5/1023)
            self.t_ORP.append(ti)
            self.volt_ORP.append(p)
            print("%.1f %.3f" %(ti,p))
            time.sleep(0.2)
            ti += 0.2
        self.ORP=sum(self.volt_ORP)/len(self.volt_ORP)
        time.sleep(1.0)
    def medir_Conductividad(self):
        self.volt_ce=[]
        self.t_ce=[]
        ti=0
        for i in range(21):
            p=analogRead(2)*(5/1023)
            self.t_ce.append(ti)
            self.volt_ce.append(p)
            print("%.1f %.3f" %(ti,p))
            time.sleep(0.2)
            ti += 0.2
        self.ce=sum(self.volt_ce)/len(self.volt_ce)
        time.sleep(1.0)
    #####    FIN DE LA CLASE      ######### 
    
circuito= Circuito_Hidraulico()
parametros=Parametros_Fisicoquimicos()
while (circuito.activo ==True):
    print("¿ Que desea hacer ? \n"+
                   "1. Comenzar medicion automatica\n"+
                   "2. Obtener voltagramas\n"+
                   "3. Medir parametros fisicoquimicos\n"+ 
                   "4. Terminar mediciones\n")
    decision=int(input())
    if decision ==1:
        circuito.Automatico()
        time.sleep(float(2))
        print("\n")
    if decision ==2:
        circuito.Voltagrama_Automatico()
        time.sleep(float(2))
        print("\n")
    if decision ==3:
        circuito.Llenar()
        print("Se estan midiendo los Parametros fiscoquimicos ...")
        print("Espere unos segundos ...")
        print("Midiendo pH ...")
        parametros.medir_pH()
        print("Mediciones \n",parametros.volt_ph)
        time.sleep(float(1))
        print("\n Midiendo ORP...")
        parametros.medir_ORP()
        print("Mediciones \n",parametros.volt_ORP)
        time.sleep(float(1))
        print("\n Midiendo Conductividad Electrica ...")
        parametros.medir_Conductividad()
        print("Mediciones \n",parametros.volt_ce)
        time.sleep(float(1))
        
        print("¡ LISTO ! Ya puede visualizar los valores de los sensores ...")
        print("El valor de pH medido es: ",parametros.pH)
        print("El valor de ORP medido es: ",parametros.ORP)
        print("El valor de Conductividad medida es: ",parametros.ce)
        time.sleep(float(3))
        circuito.Drenar()
        time.sleep(float(4))
        print("\n")
        time.sleep(float(1))
        print("\n")
    if decision ==4:
        circuito.Cerrar_Sesion()
        time.sleep(float(5))
