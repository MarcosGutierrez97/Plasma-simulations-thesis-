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
print (len(x_inicial))
v_inicial = f.buildgrid_vel(pa.v_inicial) #Solo se hace una vez
print (len(v_inicial))
densidad_inicial = f.chargedensity(x_inicial,pa.densidadE)
E_inicial = f.electricfield(densidad_inicial)
print (len(E_inicial))




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


while  i < 50*pa.dt:
    if i == 0:
        posicion = f.chargeposition( v_inicial,x_inicial)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(x_inicial, v_inicial, E_inicial)
        densidad = f.chargedensity(posicion, densidad_inicial)
        E = f.electricfield(densidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        print (len(posicion))
        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    else:
        posicion = f.chargeposition(velocidad, posicion)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posicion, velocidad, E)
        densidad = f.chargedensity(posicion, densidad)
        E = f.electricfield(densidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
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
print (len(velocidades))
graf_vel = [] # campo electrico en un solo nodo
for i in range (len(velocidades)):
    graf_vel.append(camposE[i][0])

plt.plot(tiempo, graf_vel)
plt.show()
