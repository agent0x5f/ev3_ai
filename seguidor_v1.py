#!/usr/bin/env python3
"""
Algoritmo para segidor de linea
Se detiene cuando llega a la meta o pasa un tiempo determinado
Genera un csv que contiene los datos de los sensores
"""
#Importamos las librerias
from ev3dev2.auto import *
from time import perf_counter, sleep
apagado = False #detiene el ev3 cuando True
tiempo_inicio = 0

#inicializa las conecciones a los motores y sensores del ev3
def enciende_ev3():
    #conectamos el push button
#    boton = TouchSensor()
#    assert boton.connected
    #conectamos los motores
    motor_izq = LargeMotor(OUTPUT_D)
    #assert motor_izq.connected
    motor_der = LargeMotor(OUTPUT_A)
    #assert motor_der.connected
    #conectamos los sensores de color
    ojo_izq = ColorSensor('in3')
    #assert ojo_izq.connected
    ojo_med = ColorSensor('in2')
    #assert ojo_med.connected
    ojo_der = ColorSensor('in1')
    #assert ojo_der.connected
    #cambiamos el modo del sensor de color
    ojo_izq.mode = 'COL-REFLECT'
    ojo_der.mode = 'COL-REFLECT'
    ojo_med.mode = 'COL-REFLECT'
    #empieza a contar el tiempo de ejecucion
    tiempo_inicio = time.perf_counter()

#activa la recoleccion de datos en el recorrido
def inicia_recolecta():
    f = open("data.txt", "w+")

#escribe los datos de este ciclo del loop
def anota():
    f.write(str(ojo_izq.value()) + "," +
            str(ojo_der.value()) + "," +
            str(ojo_med.value()) + "," +
            str(motor_izq.speed()) + "," +
            str(motor_der.speed()) + "\n"
    )

#apaga el ev3 si se apreta el boton
def apagador():
#    if boton.is_pressed == True:
    apagado = False

#termina la recoleccion de datos en el recorrido
def termina_recolecta():
    f.close()

#detiene los motores
def apaga_ev3():
    motor_izq.stop()
    motor_der.stop()
#test
#main loop de ejecucion
def run():
    #tiempo actual
    tiempo_actual = time.perf_counter()
    #tiempo transcurrido
    tiempo_ejecucion = tiempo_actual-tiempo_inicio
    #mientras que no se aprete el boton de stop, corre
    while apagado == False or tiempo_ejecucion < 10:
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
        elif ojo_izq < 10 and ojo_der < 10 and ojo_med <10:
            apaga_ev3()
            break
        #esta perfecto siguele    
        else: 
            motor_der.run_forever(speed_sp = 50)
            motor_izq.run_forever(speed_sp = 50)
        #ya acabaste un loop cycle, escribe tus datos
        anota()
        #epoch, atrasa el ciclo para que los motores tengan tiempo de reaccionar
        sleep(0.2)
        #Ya corrió almenos un ciclo, revisa si hay apagado manual
        apagador()

#main
enciende_ev3()
inicia_recolecta()
run()
termina_recolecta()