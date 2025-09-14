#!/usr/bin/env python3
"""
Algoritmo para segidor de linea
Se detiene cuando llega a la meta o pasa un tiempo determinado
Genera un csv que contiene los datos de los sensores
"""
#Importamos las librerias
from ev3dev2.auto import *
from time import perf_counter, sleep
#variables globales
apagado = False #detiene el ev3 cuando True
tiempo_inicio = 0
tiempo_actual = 0
tiempo_ejecucion = 0
f = open("data.txt", "w+")

    #conectamos los motores
motor_der = LargeMotor(OUTPUT_A)
motor_izq = LargeMotor(OUTPUT_D)
    #conectamos los sensores de color
ojo_der = ColorSensor('in1')
ojo_med = ColorSensor('in2')
ojo_izq = ColorSensor('in3')
    #assert ojo_der.connected
    #cambiamos el modo del sensor de color
ojo_izq.mode = 'COL-REFLECT'
ojo_der.mode = 'COL-REFLECT'
ojo_med.mode = 'COL-REFLECT'
    #empieza a contar el tiempo de ejecucion
tiempo_inicio = time.perf_counter()

#escribe los datos de este ciclo del loop a file y terminal
def anota():
    print(str(ojo_izq.value()) + "," +
            str(ojo_med.value()) + "," +
            str(ojo_der.value()) + "," +
            str(motor_izq.speed) + "," +
            str(motor_der.speed))

    f.write(str(ojo_izq.value()) + "," +
            str(ojo_med.value()) + "," +
            str(ojo_der.value()) + "," +
            str(motor_izq.speed) + "," +
            str(motor_der.speed) + "\n"
    )

#apaga el ev3 si se apreta el boton
def apagador():
#    if boton.is_pressed == True:
    print("apagando...")
    motor_izq.stop()
    motor_der.stop()

#main loop de ejecucion
def run():
    tiempo_actual = time.perf_counter()
    #tiempo transcurrido
    tiempo_ejecucion = tiempo_actual-tiempo_inicio
    print("runtime: " + tiempo_ejecucion)
    #mientras que no se aprete el boton de stop, corre
    while apagado == False or tiempo_ejecucion < 10:
        #muy pasado de izq, ve a la derecha
        if ojo_izq < 10: 
            print("gira duro a der")
            motor_der.run_forever(speed_sp = 10)
            motor_izq.run_forever(speed_sp = 50)
        #muy pasado de der, ve a la izquierda
        elif ojo_der < 10: 
            print("gira duro izq")
            motor_der.run_forever(speed_sp = 50)
            motor_izq.run_forever(speed_sp = 10)
        #un poco pasado de izq, ve a la derecha
        elif ojo_izq < 30: 
            print("gira der")
            motor_der.run_forever(speed_sp = 30)
            motor_izq.run_forever(speed_sp = 50)
        #un poco pasado de der, ve a la izquierda
        elif ojo_der < 10: 
            print("gira izq")
            motor_der.run_forever(speed_sp = 50)
            motor_izq.run_forever(speed_sp = 30)
        #llegó a la meta parale
        elif ojo_izq < 10 and ojo_der < 10 and ojo_med <10:
            apagado = True
            apagador()
            break
        #esta perfecto siguele    
        else: 
            print("OK")
            motor_der.run_forever(speed_sp = 50)
            motor_izq.run_forever(speed_sp = 50)
        #ya acabaste un loop cycle, escribe tus datos
        anota()
        #epoch, atrasa el ciclo para que los motores tengan tiempo de reaccionar
        sleep(0.1)
        #Ya corrió almenos un ciclo, revisa si hay apagado manual
        if apagado == True
          apagador()

#main
run()
f.close()
