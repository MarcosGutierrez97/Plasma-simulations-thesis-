# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:02:51 2020

@author: HP
"""

import funciones as f
import parametros as pa
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#Ciclo inicial. Este solo se hace una vez


x_inicial = f.buildgrid_pos(pa.x_inicial) #Solo se hace una vez
#print (len(x_inicial))
v_inicial = f.buildgrid_vel(pa.v_inicial) #Solo se hace una vez
#print (len(v_inicial))
densidad_inicial = f.chargedensity(x_inicial,pa.densidadE)
E_inicial = f.electricfield(densidad_inicial)
E_particulas_inicial = f.FieldParticle(x_inicial,E_inicial)
print (len(E_particulas_inicial))
#K_inicial = f.Kenergy(pa.ki,pa.v_inicial)
#print (len(K_inicial))
#U_inicial = f.Uenergy(E_particulas_inicial,pa.upot)
#print (len(U_inicial))
"""
He tenido problemas con la funcion de energia potencial Uenergy. Me tira un Index error,
pero cuando comparo la cantidad de particulas que analiza la funcion que cree para analizar
los E de cada particula-FieldParticle- entonces aun no se porque tira ese error.
"""




#Se empieza a constuir el ciclo


i = 0
p = 0
e = 1
posiciones= []
velocidades = []
densidades = []
camposE = []
camposE_particulas = []
tiempo = []
energiacinetica = []
#energiapotencial = []
#energiatotal = []
#kdrift = []



while  i <= 5*pa.dt:
    if i == 0:
        posicion = f.chargeposition( v_inicial,x_inicial)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(x_inicial, v_inicial, E_inicial)
        densidad = f.chargedensity(posicion, densidad_inicial)
        E = f.electricfield(densidad)
        K = f.Kenergy(v_inicial)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        energiacinetica.append(K)
        print (len(posicion))
        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    else:
        posicion = f.chargeposition(velocidad, posicion)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posicion, velocidad, E)
        densidad = f.chargedensity(posicion, densidad)
        E = f.electricfield(densidad)
        K = f.Kenergy(velocidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        energiacinetica.append(K)
        p = p + 1 #Cuando agrego esto mi tira error:


        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])

    i = i + pa.dt
    tiempo.append(i)


"""
print ('posiciones')
print ( posiciones)
print (len(posiciones))
print ('velocidades')
print (  velocidades)
print (len(velocidades))
print ('densidades')
print ( densidades)
print (len(densidades))
print ('campos')
print (camposE)
"""
print (len(tiempo))
print (len(energiacinetica))

graf_vel = [] # campo electrico en un solo nodo
for i in range (len(velocidades)):
    print (max(velocidades[i]))
    print (min(velocidades[i]))
    #graf_vel.append(((energiacinetica[i][0])))
    graf_vel.append(((velocidades[i][5]))) #Cambie la grafica de E por la de K. K de una particula en el tiempo

plt.plot(tiempo, graf_vel)
plt.ylim(2.075,2.1)
plt.show()
"""
Cuando veo las graficas del campo de Martin, veo que oscila bien bonito, jaja.
No se si la diferencia sera en que integre por trapecio y Martin uso FFT
o si habre cometido algun error. Tambien, la grafica de K sale exponencial y deberia oscilar.
Tambien, en las pruebas para graficar la velocidad que estaba haciendo arriba, vi que las
velocidades no se estan sumando, y no logre ver porque. 
"""
