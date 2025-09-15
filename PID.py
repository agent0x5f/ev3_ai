#!/usr/bin/env python3
"""
Algoritmo para seguidor de linea con controlador PID.
Se detiene cuando llega a la meta, se pierde o pasa un tiempo determinado.
Genera un csv que contiene los datos de los sensores.

Empieza solo con Kp: Establece Ki y Kd en 0.

Aumenta Kp: Sube Kp poco a poco hasta que el robot siga la línea, aunque lo haga "temblando" u oscilando de lado a lado. Si Kp es muy alto, las oscilaciones serán violentas.

Añade Kd para suavizar: Ahora, empieza a aumentar Kd. Verás que las oscilaciones se reducen. El derivativo funciona como un amortiguador. Busca un valor que elimine el temblor sin hacer que el robot sea demasiado lento para reaccionar.

Añade Ki si es necesario: Si notas que en curvas largas el robot siempre se queda un poco fuera del centro, aumenta Ki muy lentamente. El integral ayudará a eliminar ese error persistente, pero si es muy alto, puede causar inestabilidad.
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

# --- Constantes de Umbrales (para casos extremos) ---
VER_NEGRO = 18
VER_BLANCO = 30

# --- Constantes del Controlador PID --- 🧠
# ¡ESTOS VALORES REQUIEREN AJUSTE FINO (TUNING)!
Kp = 0.8  # Proporcional: La fuerza de reacción principal.
Ki = 0.02 # Integral: Elimina errores pequeños y persistentes.
Kd = 0.5  # Derivativo: Amortigua y previene oscilaciones.

SETPOINT = 28       # El valor ideal del sensor_med (borde de la línea).
VELOCIDAD_BASE = 40 # Velocidad a la que el robot intentará moverse.

# --- Funciones ---
def anota(f):
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

def run(f):
    """Bucle principal de ejecución con PID."""
    global apagado, tiempo_ejecucion

    # Variables para el cálculo PID
    integral = 0
    last_error = 0

    while not apagado and tiempo_ejecucion < 20: # Aumenté el tiempo para pruebas
        tiempo_ejecucion = perf_counter() - tiempo_inicio

        val_izq = ojo_izq.value()
        val_der = ojo_der.value()
        val_med = ojo_med.value()

        # 1. ¿Llegó a la meta? (Caso extremo)
        if val_izq < VER_NEGRO and val_der < VER_NEGRO and val_med < VER_NEGRO:
            print("¡Meta alcanzada!")
            apagado = True
            break

        # 2. ¿Se perdió la línea? (Caso extremo)
        elif val_izq > VER_BLANCO and val_med > VER_BLANCO and val_der > VER_BLANCO:
            print("¡Línea perdida! Deteniendo robot.")
            apagado = True
            break

        # 3. Si no hay casos extremos, se ejecuta la lógica PID
        else:
            # --- CÁLCULO PID ---
            # El error nos dice qué tan lejos estamos del setpoint
            error = SETPOINT - val_med

            # El integral acumula el error para corregir desviaciones persistentes
            integral += error
            # Opcional: Limitar el integral para evitar que crezca demasiado
            if abs(integral) > 200: integral = 200 if integral > 0 else -200

            # El derivativo calcula la "velocidad" del error para anticipar y suavizar
            derivativo = error - last_error

            # La salida final del PID es la suma de los tres componentes
            correccion = (Kp * error) + (Ki * integral) + (Kd * derivativo)

            # Actualizamos el último error para el siguiente ciclo
            last_error = error

            # --- APLICAR CORRECCIÓN A MOTORES ---
            velocidad_izq = VELOCIDAD_BASE - correccion
            velocidad_der = VELOCIDAD_BASE + correccion

            # Enviamos la velocidad calculada a los motores
            motor_izq.run_forever(speed_sp=velocidad_izq)
            motor_der.run_forever(speed_sp=velocidad_der)

        anota(f)
        sleep(0.01) # Un ciclo más rápido puede mejorar la respuesta del PID

# --- Ejecución Principal ---
print("Iniciando seguidor de línea con PID...")
with open("data_pid.txt", "w+") as f:
    run(f)

apagador()
print(f"Programa finalizado. Runtime total: {tiempo_ejecucion:.2f} segundos.")
