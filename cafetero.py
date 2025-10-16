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
# motores del brazo recolector, ya que el ev3 solo tiene 4 puertos de motor, usaremos un motor para subir y bajar el brazo
# y otro para abrir y cerrar la garra

#motor_3 = LargeMotor(OUTPUT_C)
#motor_4 = LargeMotor(OUTPUT_D)

#sensores de línea, estoy limitado a 4 puertos de sensores, así que usaré sólo 1 sensor de linea al frente.
#ojo_der = ColorSensor('in1')
ojo_frente = ColorSensor('in1')
#ojo_izq = ColorSensor('in3')
#sensor ultrasónico
ojo_ultra = UltrasonicSensor('in3')
#sensor de color para detectar el color del café, montado en la garra
ojo_color = ColorSensor('in4')
#configuramos los sensores de línea para que usen el modo de reflejo de color
#ojo_izq.mode = 'COL-REFLECT'
#ojo_der.mode = 'COL-REFLECT'
ojo_frente.mode = 'COL-REFLECT'
#configuramos el sensor ultrasónico para que use el modo de distancia en centímetros
# este modo nos da la distancia en cm a un objeto frente al sensor de forma continua
ojo_ultra.mode = 'US-DIST-CM'
#configuramos el sensor de color para que use el modo de color
ojo_color.mode = 'COL-COLOR'
#color  -> Color detected by the sensor, categorized by overall value.
#0: No color
#1: Black
#2: Blue
#3: Green
#4: Yellow
#5: Red
#6: White
#7: Brown
# si requiero detectar el color del café, puedo usar los valores de: raw
# Red, green, and blue components of the detected color, as a tuple.
# Officially in the range 0-1020 but the values returned will never be that high. 
# We do not yet know why the values returned are low, 
# but pointing the color sensor at a well lit sheet of white paper will return values in the 250-400 range.
#ojo_color.mode = 'RGB-RAW'

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
