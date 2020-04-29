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




#Se empieza a constuir el ciclo


i = 0
j = 0
e = 1
posiciones= [x_inicial]
velocidades = [v_inicial]
densidades = [densidad_inicial]
camposE = [E_inicial]
camposE_particulas = [pa.E_particulaI]
tiempo = [0]


while  i < 10:
    if i == 0:
        posicion = f.chargeposition( v_inicial)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(x_inicial, v_inicial, E_inicial,pa.E_particulaI)
        densidad = f.chargedensity(posicion, densidad_inicial)
        E = f.electricfield(densidad)
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
        j = j + 1
    else:
        posicion = f.chargeposition(velocidades[j])
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posiciones[j], velocidades[j], camposE[j], pa.E_particulaI)
        densidad = f.chargedensity(posiciones[j], densidades[j])
        E = f.electricfield(densidades[j])
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    i = i + pa.dt


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

plt.plot(posiciones[3], velocidades[3])
plt.show()
