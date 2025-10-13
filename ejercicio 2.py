#Reporte sobre cada uno de los inscisos
#tenemos tres conjuntos de estudintes segun las actividades en la que participan
#1 ¿Que estudiantes estan inscritos en total en los tres talleres?
#2 ¿Listado de alumnos que estan inscritos en robotica o programacion?
#3 ¿Que estudiantes estan en las tres actividades?
#4 ¿Que estudiantes estan unicamente en el taller de IA y en ninguna otra actividad?
#5 ¿Qué estudiantes no están inscritos en el Taller de Robótica?

#A: Estudiantes inscritos en Taller de Robótica
A={"Carlos", "Diana", "Elena", "José", "Mariana", "Pedro"}
#B: Estudiantes inscritos en Taller de Programación
B={"Diana", "José", "Laura", "Pedro", "Santiago"}
#C: Estudiantes inscritos en Taller de Inteligencia Artificial
C={"Carlos", "Elena", "Laura", "Mariana", "Roberto"}

R1=A.union(B).union(C)
R2=A.union(B)
R3=A.intersection(B).intersection(C)
R4=C.difference(A).difference(B)
R5=R1.difference(A)
print("1. Estudiantes inscritos en total en los tres talleres:", R1)
print("2. Listado de alumnos que estan inscritos en robotica o programacion:", R2)
print("3. Estudiantes que estan en las tres actividades:", R3)
print("4. Estudiantes unicamente en el taller de IA y en ninguna otra actividad:", R4)
print("5. Estudiantes que no están inscritos en el Taller de Robótica:", R5)