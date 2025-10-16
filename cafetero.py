#!/usr/bin/env python3
"""
Algoritmo para recolector de café.
Se detiene cuando termina de recolectar o pasa un tiempo determinado.
Sistema de navegación basado en conocimiento previo del terreno y uso de sensores.
"""
# Importamos las librerias
from ev3dev2.auto import *
from time import perf_counter, sleep

# --- Conexiones y configuración ---
# usaremos un sensor de linea en cada lado y uno al frente para detectar los limites del cafetal
# además de los 4 motores para mover la plataforma y el brazo recolector
# igual usaremos un sensor ultrasónico para detectar obstáculos
# así como un sensor de color para detectar el color del café para saber si está maduro o no
# igual requerimos las interfaces de los motores del brazo 
# y un sensor giroscópico para mantener la orientación del robot  //opcional
# igual de un sensor táctil para iniciar y detener el proceso //opcional

#motores de movimiento
motor_1 = LargeMotor(OUTPUT_A)
motor_2 = LargeMotor(OUTPUT_B)
motor_3 = LargeMotor(OUTPUT_C)
motor_4 = LargeMotor(OUTPUT_D)
#sensores de línea
ojo_der = ColorSensor('in1')
ojo_frente = ColorSensor('in2')
ojo_izq = ColorSensor('in3')
ojo_izq.mode = 'COL-REFLECT'
ojo_der.mode = 'COL-REFLECT'
ojo_frente.mode = 'COL-REFLECT'
# --- Constantes de Umbrales ("VER") ---
# Estos valores pueden necesitar ajustes según las condiciones de iluminación y el color del suelo. 
VER_NEGRO = 25 #Si el sensor ve esto, esta totalmente en la linea negra
VER_GRIS = 50
VER_BLANCO = 50 # Si el sensor lee más que esto, es superficie blanca
# --- Constantes de Velocidad ---
# Se requerirán posibles ajustes para asegurar giros estables para evitar tocar obstaculos y limites.
VEL_TERCERA = 80
VEL_SEGUNDA = 50
VEL_PRIMERA = 10
VEL_REVERSA = -50



def run():
           sleep(0.1)

# --- Main Loop ---

run()
