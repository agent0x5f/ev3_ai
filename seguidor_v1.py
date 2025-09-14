#!/usr/bin/env python3
"""
Algoritmo para seguidor de linea
Se detiene cuando llega a la meta o pasa un tiempo determinado
Genera un csv que contiene los datos de los sensores
"""
# Importamos las librerias
from ev3dev2.auto import *
from time import perf_counter, sleep

# --- Conexiones y configuración ---
motor_der = LargeMotor(OUTPUT_A)
motor_izq = LargeMotor(OUTPUT_D)
ojo_der = ColorSensor('in1')
ojo_med = ColorSensor('in2')
ojo_izq = ColorSensor('in3')

ojo_izq.mode = 'COL-REFLECT'
ojo_der.mode = 'COL-REFLECT'
ojo_med.mode = 'COL-REFLECT'

# --- Variables Globales ---
apagado = False
tiempo_inicio = perf_counter()
tiempo_ejecucion = 0
f = open("data.txt", "w+")

# --- Variables de Velocidad ---
VEL_ALTA = 50
VEL_MEDIA = 30
VEL_BAJA = 10

# --- Funciones ---
def anota():
    """Escribe los datos de este ciclo en el archivo y la terminal."""
    datos = (f"{ojo_izq.value()},{ojo_med.value()},{ojo_der.value()},"
             f"{motor_izq.speed},{motor_der.speed}")
    print(datos)
    f.write(datos + "\n")

def apagador():
    """Detiene los motores."""
    print("Apagando motores...")
    motor_izq.stop()
    motor_der.stop()

def run():
    """Bucle principal de ejecución."""
    global apagado, tiempo_ejecucion

    while not apagado and tiempo_ejecucion < 10:
        tiempo_ejecucion = perf_counter() - tiempo_inicio

        # 1. ¿Llegó a la meta?
        if ojo_izq.value() < 10 and ojo_der.value() < 10 and ojo_med.value() < 10:
            print("¡Meta alcanzada!")
            apagado = True
            break

        # 2. Correcciones de trayectoria
        elif ojo_izq.value() < 10:
            print("Gira duro a la derecha")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_BAJA)

        elif ojo_der.value() < 10:
            print("Gira duro a la izquierda")
            motor_izq.run_forever(speed_sp=VEL_BAJA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        elif ojo_izq.value() < 30:
            print("Gira a la derecha")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_MEDIA)

        elif ojo_der.value() < 30:
            print("Gira a la izquierda")
            motor_izq.run_forever(speed_sp=VEL_MEDIA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        # 3. Avanza recto
        else:
            print("OK")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        anota()
        sleep(0.1)

# --- Ejecución Principal ---
print("Iniciando seguidor de línea...")
run()

apagador()
f.close()
print(f"Programa finalizado. Runtime total: {tiempo_ejecucion:.2f} segundos.")