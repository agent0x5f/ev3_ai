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
    