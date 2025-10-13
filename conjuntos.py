A={"Ana", "Luis", "Pedro", "Marta"}
B={"Pedro", "Marta", "Carlos", "Sofia"}
C=A.union(B)#|
print(C)
C1=A.intersection(B)#&
print(C1)
C2=A.difference(B)#-
print(C2)
C3=A.symmetric_difference(B)#^
print(C3)
U=A.union(B)
C4=U - A
print("C4=")
print(C4)
#producto cartesiano
F={(x,y) for x in A for y in B}
print(F)
#Obtener el conjunto de todos los estudiantes que cursan al menos una 
#de las dos materias: Matematicas o Fisica
Mate={"Ana", "Luis", "Pedro", "Maria", "Jose"} #Matematicas
Fisi={"Luis", "Maria", "Carmen", "Jose", "Raul"} #Fisica
incA=Mate.union(Fisi)
print("incA=")
print(incA)
#Obtener el conjunto de todos los estudiantes que cursan ambas materias
incB=Mate.intersection(Fisi)
print("incB=")
print(incB)
#Obtener el conjunto de todos los estudiantes que cursan Matematicas pero no Fisica
incC=Mate.difference(Fisi)
print("incC=")
print(incC)

