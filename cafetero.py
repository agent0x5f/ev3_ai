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
# y otro para abrir y cerrar la garra, no tenemos más puertos, por lo que el brazo no se moverá lateralmente.
# para ello, el robot deberá posicionarse correctamente frente al fruto.

#motor_3 = LargeMotor(OUTPUT_C)
#motor_4 = LargeMotor(OUTPUT_D)

#sensores de línea, estoy limitado a 4 puertos de sensores, así que usaré sólo 1 sensor de linea al frente.
#ojo_der = ColorSensor('in1')
ojo_frente = ColorSensor('in1')
#ojo_izq = ColorSensor('in3')
#sensor ultrasónico
ojo_ultra = UltrasonicSensor('in2')
#sensor de color para detectar el color del café, montado en la garra
ojo_color = ColorSensor('in3')
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
#1: Black -overripe
#2: Blue -overripe
#3: Green -green
#4: Yellow -ripe
#5: Red -ripe
#6: White
#7: Brown //podria usarse para naranja? que es un -ripe.
# si requiero detectar el color del café naranja, puedo usar los valores de: raw
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
# podemos usar el giroscopio para girar grados especificos.
# turn_right(speed, degrees, brake=True, error_margin=2, sleep_time=0.01)
# Rotate clockwise degrees in place
# el giroscopio nos da: MODE_GYRO_ANG = 'GYRO-ANG' Angle(grados)
giroscopio = GyroSensor('in4')
giroscopio.mode = 'GYRO-ANG'

# definición del problema.
# requimos de un robot autonomo que se traslade de un punto A hacia un punto B, con A siendo 5 posibles lugares conocidos y
# B tres lugares posibles. En el camino, se puede encontrar 0, 1, 2 obstaculos en posiciones posibles conocidas.
# al llegar a un posible punto B, se procede a la identificación y recolección de los frutos.
# una vez terminado una tanda de recolección se procede a regresar a la zona inicial
# al llegar a la zona inicial, se procede a buscar una zona de depósito de color identificable conocido.
#repetir hasta que se acaben los frutos,el tiempo o forzado.


class RobotRecolector:
    def __init__(self):
        """
        Constructor del robot recolector de café.
        """
        self.estados = {
            "ESPERANDO_INICIO", "NAVEGANDO_A_CULTIVO", "EVADIENDO_OBSTACULO",
            "BUSCANDO_GRANO", "IDENTIFICANDO_GRANO", "RECOLECTANDO",
            "NAVEGANDO_A_DEPOSITO", "BUSCANDO_CONTENEDOR", "DEPOSITANDO",
            "COMPLETADO"
        }
        
        self.estado_actual = "ESPERANDO_INICIO"
        self.granos_recolectados = [] # Para almacenar los granos internamente

        # El CEREBRO del robot: las transiciones dependen del estado ACTUAL y del EVENTO que ocurre.
        # Estructura: {'estado_origen': {'evento': 'estado_destino'}}
        self.transiciones = {
            "ESPERANDO_INICIO": {
                "iniciar_recoleccion": "NAVEGANDO_A_CULTIVO"
            },
            "NAVEGANDO_A_CULTIVO": {
                "obstaculo_detectado": "EVADIENDO_OBSTACULO",
                "llegada_a_cultivo": "BUSCANDO_GRANO"
            },
            "EVADIENDO_OBSTACULO": {
                "obstaculo_superado": "NAVEGANDO_A_CULTIVO" # Reanuda la navegación original
            },
            "BUSCANDO_GRANO": {
                "grano_encontrado": "IDENTIFICANDO_GRANO",
                "arbol_limpio": "NAVEGANDO_A_DEPOSITO", # Si ya no hay más granos que recoger en un árbol
                "todos_los_arboles_limpios": "NAVEGANDO_A_DEPOSITO" # O si ya revisó todos los árboles
            },
            "IDENTIFICANDO_GRANO": {
                "grano_maduro_detectado": "RECOLECTANDO",
                "grano_pasado_detectado": "RECOLECTANDO",
                "grano_verde_detectado": "BUSCANDO_GRANO" # Ignora el verde y busca otro
            },
            "RECOLECTANDO": {
                "recoleccion_exitosa": "BUSCANDO_GRANO", # Busca el siguiente grano en el mismo árbol
                "almacenamiento_lleno": "NAVEGANDO_A_DEPOSITO" # Si ya no caben más, va a depositar
            },
            "NAVEGANDO_A_DEPOSITO": {
                "obstaculo_detectado": "EVADIENDO_OBSTACULO_DE_REGRESO", # Podríamos necesitar un estado de evasión diferente para el regreso
                "llegada_a_deposito": "BUSCANDO_CONTENEDOR"
            },
            "EVADIENDO_OBSTACULO_DE_REGRESO":{
                "obstaculo_superado": "NAVEGANDO_A_DEPOSITO"
            },
            "BUSCANDO_CONTENEDOR": {
                "contenedor_maduro_encontrado": "DEPOSITANDO",
                "contenedor_pasado_encontrado": "DEPOSITANDO"
            },
            "DEPOSITANDO": {
                "deposito_finalizado": "NAVEGANDO_A_CULTIVO", # Vuelve por más granos
                "todos_los_granos_depositados": "COMPLETADO" # Si ya no hay más granos en el campo
            },
            "COMPLETADO": {
                # Estado final, no hay transiciones de salida
            }
        }
        print(f"Robot listo en estado: {self.estado_actual}")

    def procesar_evento(self, evento):
        """
        Procesa un evento y cambia el estado del robot si la transición es válida.
        """
        if self.estado_actual in self.transiciones and evento in self.transiciones[self.estado_actual]:
            estado_anterior = self.estado_actual
            self.estado_actual = self.transiciones[self.estado_actual][evento]
            print(f"Evento: '{evento}' | Transición: {estado_anterior} -> {self.estado_actual}")
        else:
            print(f"Evento '{evento}' ignorado en el estado '{self.estado_actual}'")


"""Simulador de eventos para probar el robot. requiere comentar el codigo de los sensores reales y motores.
# --- Probando el Robot Recolector ---

# 1. Creamos una instancia del robot. Inicia en "ESPERANDO_INICIO".
robot = RobotRecolector()
# 2. Simulamos la ejecución con una secuencia de eventos lógicos.
print("\n--- INICIANDO SIMULACIÓN ---")
robot.procesar_evento("iniciar_recoleccion")      # Presionamos el botón de inicio
# Va de camino y se encuentra un "pool" (obstáculo)
robot.procesar_evento("obstaculo_detectado")
robot.procesar_evento("obstaculo_superado")       # Lo rodea y sigue su camino
robot.procesar_evento("llegada_a_cultivo")        # Llega a la zona de árboles
robot.procesar_evento("grano_encontrado")         # Se alinea con el primer grano
# El sensor de color lo identifica como verde
robot.procesar_evento("grano_verde_detectado")    # Lo ignora y vuelve a buscar
# Encuentra otro grano
robot.procesar_evento("grano_encontrado")
# Esta vez es maduro
robot.procesar_evento("grano_maduro_detectado")
robot.procesar_evento("recoleccion_exitosa")      # Lo guarda y busca el siguiente
# Supongamos que ya no caben más granos
robot.procesar_evento("almacenamiento_lleno")
robot.procesar_evento("llegada_a_deposito")
robot.procesar_evento("contenedor_maduro_encontrado")
robot.procesar_evento("deposito_finalizado")      # Deposita y vuelve por más
# Finalmente, después de muchos ciclos, ya no hay más granos
robot.procesar_evento("llegada_a_cultivo")
robot.procesar_evento("todos_los_arboles_limpios")
robot.procesar_evento("llegada_a_deposito")
robot.procesar_evento("todos_los_granos_depositados")
print(f"\n--- SIMULACIÓN FINALIZADA ---")
print(f"Estado final del robot: {robot.estado_actual}")

"""

"""Ejemplo de la simulación:
--- INICIANDO SIMULACIÓN ---
Evento: 'iniciar_recoleccion' | Transición: ESPERANDO_INICIO -> NAVEGANDO_A_CULTIVO
Evento: 'obstaculo_detectado' | Transición: NAVEGANDO_A_CULTIVO -> EVADIENDO_OBSTACULO
Evento: 'obstaculo_superado' | Transición: EVADIENDO_OBSTACULO -> NAVEGANDO_A_CULTIVO
Evento: 'llegada_a_cultivo' | Transición: NAVEGANDO_A_CULTIVO -> BUSCANDO_GRANO
Evento: 'grano_encontrado' | Transición: BUSCANDO_GRANO -> IDENTIFICANDO_GRANO
Evento: 'grano_verde_detectado' | Transición: IDENTIFICANDO_GRANO -> BUSCANDO_GRANO
Evento: 'grano_encontrado' | Transición: BUSCANDO_GRANO -> IDENTIFICANDO_GRANO
Evento: 'grano_maduro_detectado' | Transición: IDENTIFICANDO_GRANO -> RECOLECTANDO
Evento: 'recoleccion_exitosa' | Transición: RECOLECTANDO -> BUSCANDO_GRANO
Evento 'almacenamiento_lleno' ignorado en el estado 'BUSCANDO_GRANO'
Evento 'llegada_a_deposito' ignorado en el estado 'BUSCANDO_GRANO'
Evento 'contenedor_maduro_encontrado' ignorado en el estado 'BUSCANDO_GRANO'
Evento 'deposito_finalizado' ignorado en el estado 'BUSCANDO_GRANO'
Evento 'llegada_a_cultivo' ignorado en el estado 'BUSCANDO_GRANO'
Evento: 'todos_los_arboles_limpios' | Transición: BUSCANDO_GRANO -> NAVEGANDO_A_DEPOSITO
Evento: 'llegada_a_deposito' | Transición: NAVEGANDO_A_DEPOSITO -> BUSCANDO_CONTENEDOR
Evento 'todos_los_granos_depositados' ignorado en el estado 'BUSCANDO_CONTENEDOR'

--- SIMULACIÓN FINALIZADA ---
Estado final del robot: BUSCANDO_CONTENEDOR
"""