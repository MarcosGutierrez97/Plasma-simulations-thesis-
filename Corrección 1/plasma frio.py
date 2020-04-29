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
v_inicial = f.buildgrid_vel(pa.v_inicial) #Solo se hace una vez
densidad_inicial = f.chargedensity(x_inicial,pa.densidadE)
E_inicial = f.electricfield(densidad_inicial)
"""
print (x_inicial)
print (len(x_inicial))
print (v_inicial)
print (len(v_inicial))
print (densidad_inicial)
print (len(densidad_inicial))
print (E_inicial)
print (len(E_inicial))
"""


#Se empieza a constuir el ciclo


temp = 0 #Contador de tiempo
j = 0 #Contador en listas
e = 1
posiciones= []
velocidades = []
densidades = []
camposE = []
camposE_particulas = []
tiempo = [0]


while  temp < 1:
    if temp == 0:
        posicion = f.chargeposition( v_inicial,x_inicial)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(x_inicial,v_inicial,E_inicial)
        densidad = f.chargedensity(posicion, densidad_inicial)
        E = f.electricfield(densidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    else:
        posicion = f.chargeposition(velocidad,posicion)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posicion,velocidad,E)
        densidad = f.chargedensity(posicion, densidad)
        E = f.electricfield(densidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    temp = temp + pa.dt



"""
print ('lista posiciones')
print (posiciones)
print (len(posiciones))
print (posiciones[0])
print (len(posiciones[0]))
print ('valores de v')
print (velocidades)
print (len(velocidades))
print (velocidades[0])
print (len(velocidades[0]))
print ('valores de E')
print (camposE)
print (len(camposE))
print (camposE[0])
print(len(camposE[0]))
"""

#Densidad Neta (idea tomada del código del Cern)

#plt.plot (pa.coor_malla,  camposE[2])
#plt.xlabel('x')
#plt.xlim(0,pa.malla_longitud)
#plt.show()
