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
print (x_inicial)
print (len(x_inicial))
v_inicial = f.buildgrid_vel(pa.v_inicial) #Solo se hace una vez
densidad_inicial = f.chargedensity(x_inicial,pa.densidadE)
E_inicial = f.electricfield(densidad_inicial)




#Se empieza a constuir el ciclo


i = 0
p = 0
e = 1
posiciones= []
velocidades = []
densidades = []
camposE = []
camposE_particulas = []
tiempo = [0]


while  i < 4:
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
        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    else:
        posicion = f.chargeposition(velocidades[p])
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posiciones[p], velocidades[p], camposE[p], pa.E_particulaI)
        densidad = f.chargedensity(posiciones[p], densidades[p])
        E = f.electricfield(densidades[p])
        posiciones.append(posicion)
        velocidades.append(velocidad)
        densidades.append(densidad)
        camposE.append(E)
        p = p + 1 #Cuando agrego esto mi tira error:
        """
        #File "C:\Users\HP\Documents\GitHub\Plasma-simulations-thesis-\Correcci�n 1\plasma frio.py", line 56, in <module>
    #velocidad = f.chargevelocity(posiciones[p], velocidades[p], camposE[p], pa.E_particulaI)
  #File "C:\Users\HP\Documents\GitHub\Plasma-simulations-thesis-\Correcci�n 1\funciones.py", line 75, in chargevelocity
    #if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[j]:
    """

        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])

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
for i in range(len(camposE)):
    plt.plot(pa.coor_malla, camposE[i], 'r')
plt.xlim(0,pa.malla_longitud)
plt.show()
