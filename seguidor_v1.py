#!/usr/bin/env python3
"""
Algoritmo para seguidor de linea con manejo de curvas y pérdida de línea.
Se detiene cuando llega a la meta, se pierde o pasa un tiempo determinado.
Genera un csv que contiene los datos de los sensores.
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

# --- Variables de Umbrales ("VER") y Velocidad --- 
VER_NEGRO = 25 #Si el sensor ve esto, esta totalmente en la linea negra
VER_GRIS = 50
VER_BLANCO = 50 # Si el sensor lee más que esto, es superficie blanca

VEL_ALTA = 80
VEL_MEDIA = 50
VEL_BAJA = 10
VEL_INVERSA = -50

# --- Funciones ---
def anota():
    """Escribe los datos de este ciclo en el archivo y la terminal."""
    datos = (ojo_izq.value(),ojo_med.value(),ojo_der.value(),motor_izq.speed,motor_der.speed)
    print(datos)
    f.write(str(datos) + "\n")

def apagador():
    """Detiene los motores."""
    print("Apagando motores...")
    motor_izq.stop()
    motor_der.stop()

def run():
    """Bucle principal de ejecución."""
    global apagado, tiempo_ejecucion

    while not apagado and tiempo_ejecucion < 60:
        tiempo_ejecucion = perf_counter() - tiempo_inicio

        # Leemos los valores una vez por ciclo para consistencia
        val_izq = ojo_izq.value()
        val_der = ojo_der.value()
        val_med = ojo_med.value()

        # 1. ¿Llegó a la meta?
        #if val_izq < VER_NEGRO and val_der < VER_NEGRO and val_med < VER_NEGRO:
        #   print("Meta alcanzada!")
        #   apagado = True
         #  break

        # 2. ¿Curva de 90° a la derecha?
        if val_izq < VER_NEGRO and val_med < VER_NEGRO:
            print("GIRO 90 -> Derecha")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_INVERSA)

        # 3. ¿Curva de 90° a la izquierda?
        elif val_der < VER_NEGRO and val_med < VER_NEGRO:
            print("GIRO 90 -> Izquierda")
            motor_izq.run_forever(speed_sp=VEL_INVERSA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        # 4. Correcciones de trayectoria normales
        elif val_izq < VER_NEGRO:
            print("Gira duro a la derecha")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_BAJA)

        elif val_der < VER_NEGRO:
            print("Gira duro a la izquierda")
            motor_izq.run_forever(speed_sp=VEL_BAJA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        elif val_izq < VER_GRIS:
            print("Gira a la derecha")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_MEDIA)

        elif val_der < VER_GRIS:
            print("Gira a la izquierda")
            motor_izq.run_forever(speed_sp=VEL_MEDIA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        # 5. ¿Se perdió la línea? (Todos los ojos ven blanco)
        elif val_izq > VER_BLANCO and val_med > VER_BLANCO and val_der > VER_BLANCO:
            print("¡Línea perdida! Deteniendo robot.")
            apagado = True
            break

        # 6. Si todo lo demás falla, avanza recto
        else:
            print("OK")
            motor_izq.run_forever(speed_sp=VEL_ALTA)
            motor_der.run_forever(speed_sp=VEL_ALTA)

        anota()
        sleep(0.1)

# --- Ejecución Principal ---
#print("Iniciando seguidor de línea...")
run()

apagador()
f.close()
#print("Programa finalizado. Runtime total: {tiempo_ejecucion:.2f} segundos.")