import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error

with open('data1.txt', 'r') as archivo:
    full_content= archivo.read()


# --- 1. Cargar y Preprocesar los Datos ---
data_list = []
# Usamos expresiones regulares para encontrar todos los grupos de números entre paréntesis.
matches = re.findall(r'\((.*?)\)', full_content)
for match in matches:
    try:
        # Limpiamos y convertimos cada número a entero
        cleaned_nums = [int(num.strip()) for num in match.split(',') if num.strip()]
        if len(cleaned_nums) == 5: # Nos aseguramos de que cada fila tenga 5 valores
            data_list.append(cleaned_nums)
    except ValueError:
        pass # Ignora las filas que no se puedan convertir a números

# Convertimos la lista de Python a un array de NumPy para cálculos eficientes
data = np.array(data_list)

# --- 2. Separar Características (X) y Objetivos (y) ---
# X son las primeras 3 columnas (sensores)
X = data[:, :3]
# y son las últimas 2 columnas (motores)
y = data[:, 3:]

print(f"Datos cargados exitosamente. Total de registros: {len(data)}")
print(f"Dimensiones de X (características): {X.shape}")
print(f"Dimensiones de y (objetivos): {y.shape}\n")

# --- 3. Dividir en Datos de Entrenamiento y Prueba ---
# Usaremos 80% para entrenar y 20% para probar el modelo.
# random_state=42 asegura que la división sea siempre la misma para que los resultados sean reproducibles.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Datos de entrenamiento: {len(X_train)} registros")
print(f"Datos de prueba: {len(X_test)} registros\n")

# --- 4. Crear y Entrenar el Modelo KNN ---
# Elegimos K=5. Este es un hiperparámetro que puedes ajustar.
#Con k=5, MAE=15.09
#Con k=9, MAE=14.55
#Con k=3, MAE=14.62
#Con k=21, MAE=15.02
k = 21
model = KNeighborsRegressor(n_neighbors=k)

# "Entrenamos" el modelo (en KNN, esto es simplemente almacenar los datos).
model.fit(X_train, y_train)

print(f"Modelo KNN para regresión creado y entrenado con K={k}\n")

# --- 5. Hacer Predicciones ---
# Predecimos las velocidades para el conjunto de prueba que el modelo nunca ha visto.
y_pred = model.predict(X_test)

# --- 6. Evaluar el Modelo ---
# El "Error Absoluto Medio" (MAE) nos dice, en promedio, por cuánto se equivocan las predicciones.
mae = mean_absolute_error(y_test, y_pred)
print("--- Evaluación del Modelo ---")
print(f"Error Absoluto Medio (MAE): {mae:.2f}")
print(f"Esto significa que, en promedio, la predicción de la velocidad de cada motor se desvía en {mae:.2f} unidades del valor real.\n")

# --- 7. Ejemplo de Predicción con Nuevos Datos ---
# Imagina que tu robot lee nuevos valores de los sensores.
# Por ejemplo: [sensor_izq=50, sensor_medio=0, sensor_der=50]
nuevas_lecturas = np.array([[50, 0, 50]]) # Debe tener el mismo formato (un array 2D)

# El modelo predice las velocidades de los motores
velocidades_predichas = model.predict(nuevas_lecturas)

print("--- Ejemplo de Predicción en Tiempo Real ---")
print(f"Lectura de sensores (Izq, Med, Der): {nuevas_lecturas[0]}")
print(f"Velocidad predicha para los motores (Izq, Der): ({int(velocidades_predichas[0][0])}, {int(velocidades_predichas[0][1])})")

#print(full_content)
