#!/usr/bin/env python3
"""
Algoritmo para segidor de linea
Se detiene cuando llega a la meta o pasa un tiempo determinado
Genera un csv que contiene los datos de los sensores
"""

#Importamos las librerias
from ev3dev2.auto import *
from time import *

#inicializa las conecciones a los motores y sensores del ev3
def enciende_ev3():

    #conectamos el push button
    apagador = TouchSensor()
    assert apagador.connected
    #conectamos los motores
    motor_izq = LargeMotor(OUTPUT A)
    assert motor_izq.connected
    motor_der = LargeMotor(OUTPUT B)
    assert motor_der.connected
    #conectamos los sensores de color
    ojo_izq = ColorSensor('in1')
    assert ojo_izq.connected
    ojo_med = ColorSensor('in2')
    assert ojo_med.connected
    ojo_der = ColorSensor('in3')
    assert ojo_der.connected
    #cambiamos el modo del sensor de color
    ojo_izq.mode = 'COL-REFLECT'
    ojo_der.mode = 'COL-REFLECT'
    ojo_med.mode = 'COL-REFLECT'

#activa la recoleccion de datos en el recorrido
def recolecta():
    f = open("data.txt", "w+")

#escribe los datos de este ciclo del loop
def anota():
    f.write(str(ojo_izq.value()) + "," +
            str(ojo_der.value()) + "," +
            str(ojo_med.value()) + "," +
            str(motor_izq.speed()) + "," +
            str(motor_der.speed()) + "\n+
    )

#termina la recoleccion de datos en el recorrido
def termina_recolecta():
    f.close()

#detiene los motores
def apaga_ev3():
    motor_izq.stop()
    motor_der.stop()

#main loop de ejecucion
def run():
    #muy pasado de izq, ve a la derecha
    if ojo_izq < 10: 
        motor_der.run_forever(speed_sp = 10)
        motor_izq.run_forever(speed_sp = 50)
    #muy pasado de der, ve a la izquierda
    elif ojo_der < 10: 
        motor_der.run_forever(speed_sp = 50)
        motor_izq.run_forever(speed_sp = 10)
    #un poco pasado de izq, ve a la derecha
    elif ojo_izq < 30: 
        motor_der.run_forever(speed_sp = 30)
        motor_izq.run_forever(speed_sp = 50)
    #un poco pasado de der, ve a la izquierda
    elif ojo_der < 10: 
        motor_der.run_forever(speed_sp = 50)
        motor_izq.run_forever(speed_sp = 30)
    #llegó a la meta parale
    elif ojo_izq < 10 and ojo_der < 10 and ojo_med <10
        apaga_ev3()
    #esta perfecto siguele    
    elif 
        motor_der.run_forever(speed_sp = 50)
        motor_izq.run_forever(speed_sp = 50)

    #ya acabaste un loop cycle, escribe tus datos
    