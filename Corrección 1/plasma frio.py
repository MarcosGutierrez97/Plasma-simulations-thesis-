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
step = 0
xgrid =pa.dx*np.arange(pa.noMalla + 1) #necesario para graficar
posicion1 = f.buildgrid_pos(pa.x_inicial) #Solo se hace una vez
velocidad1 = f.buildgrid_vel() #Solo se hace una vez
posicion1 = f.leapfrog(posicion1,velocidad1)
posicion1 = f.cf(posicion1)
densidad1 = f.chargedensity(posicion1)
E1 = f.electricfield(densidad1)
K1 = f.Kenergy(velocidad1,step)
U1 = f.Uenergy(E1,step)


graf = (np.pi/pa.dt/16)
t = 0
step = 0
p = 0
e = 1
posiciones= [posicion1]
velocidades = [velocidad1]
densidades = [densidad1]
camposE = [E1]
#camposE_particulas = [E_particulas_inicial]
tiempo = [0]
energiacinetica = [K1]
energiapotencial = [U1]




while  t < 5:
    if t == 0:
        posicion = f.chargeposition( velocidad1,posicion1)
        posicion = f.cf(posicion1)
        velocidad = f.chargevelocity(posicion1,velocidad1, E1)
        densidad = f.chargedensity(posicion1)
        E = f.electricfield(densidad1)
        K = f.Kenergy(velocidad1,step)
        U = f.Uenergy(E1,step)
        posiciones = np.append(posiciones, posicion)
        velocidades = np.append(velocidades,velocidad)
        densidades = np.append(densidades, densidad)
        camposE = np.append(camposE, E)
        energiacinetica = np.append(energiacinetica, K)
        energiapotencial = np.append(energiapotencial,U)
        #f.diagnosticos(t)
    elif t > 0:
        posicion = f.chargeposition( velocidad,posicion)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posicion,velocidad, E)
        densidad = f.chargedensity(posicion)
        E = f.electricfield(densidad)
        K = f.Kenergy(velocidad,step)
        U = f.Uenergy(E,step)
        posiciones = np.append(posiciones, posicion)
        velocidades = np.append(velocidades,velocidad)
        densidades = np.append(densidades, densidad)
        camposE = np.append(camposE, E)
        energiacinetica = np.append(energiacinetica, K)
        energiapotencial = np.append(energiapotencial,U)
        #f.diagnosticos(t)


    #f.diagnosticos(densidad, E,t,graf)
    t = t + pa.dt
    step = step + 1
    tiempo.append(t)

posiciones = [posiciones[i:i + pa.noParticulas] for i in range (0, len(posiciones),pa.noParticulas)]
velocidades = [velocidades[i:i + pa.noParticulas] for i in range (0, len(velocidades),pa.noParticulas)]
camposE = [camposE[i:i+pa.noMalla+1] for i in range(0,len(camposE),pa.noMalla+1)]
densidades = [densidades[i:i+pa.noMalla+1] for i in range(0,len(densidades),pa.noMalla+1)]
#energiacinetica = [energiacinetica[i:i+pa.noParticulas] for i in range (0,len(energiacinetica),pa.noParticulas)]
"""
for i in range (len(densidades)):
    plt.subplot(2,2,1)
    plt.plot(xgrid, -(pa.densidadIg + densidades[i]), label = "densidades")
    plt.scatter(xgrid, camposE[i], label ="campos")
    plt.xlim(0,pa.malla_longitud)
plt.show()
"""
#energias
print (step)
print(len(energiacinetica))
print(len(energiapotencial))
