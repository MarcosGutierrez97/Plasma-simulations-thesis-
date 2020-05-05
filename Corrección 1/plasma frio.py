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


posicion = f.buildgrid_pos(pa.x_inicial) #Solo se hace una vez
velocidad = f.buildgrid_vel() #Solo se hace una vez
posicion = f.leapfrog(posicion,velocidad)
posicion = f.cf(posicion)
densidad = f.chargedensity(posicion)
E = f.electricfield(densidad)
#E_particulas_inicial = f.FieldParticle(posicion,E)
K = f.Kenergy(velocidad)
#print (len(K_inicial))
#U_inicial = f.Uenergy(E_particulas_inicial,pa.upot)
#print (len(U_inicial))

#Se empieza a constuir el ciclo

xgrid =pa.dx*np.arange(pa.noMalla + 1)
graf = (np.pi/pa.dt/16)
t = 0
p = 0
e = 1
posiciones= [posicion]
velocidades = [velocidad]
densidades = [densidad]
camposE = [E]
#camposE_particulas = [E_particulas_inicial]
tiempo = [0]
energiacinetica = [K]
#energiapotencial = []
#energiatotal = []
#kdrift = []



while  t < 0.6:
    posicion = f.chargeposition( velocidad,posicion)
    posicion = f.cf(posicion)
    velocidad = f.chargevelocity(posicion, velocidad, E)
    densidad = f.chargedensity(posicion)
    E = f.electricfield(densidad)
    K = f.Kenergy(velocidad)
    posiciones = np.append(posiciones, posicion)
    velocidades = np.append(velocidades,velocidad)
    densidades = np.append(densidades, densidad)
    camposE = np.append(camposE, E)
    energiacinetica = np.append(energiacinetica, K)
    f.diagnosticos(densidad, E,t,graf)
    t = t + pa.dt
    tiempo.append(t)
    print(velocidades)

posiciones = [posiciones[i:i + pa.noParticulas] for i in range (0, len(posiciones),pa.noParticulas)]
velocidades = [velocidades[i:i + pa.noParticulas] for i in range (0, len(velocidades),pa.noParticulas)]
camposE = [camposE[i:i+pa.noMalla+1] for i in range(0,len(camposE),pa.noMalla+1)]
densidades = [densidades[i:i+pa.noMalla+1] for i in range(0,len(densidades),pa.noMalla+1)]
energiacinetica = [energiacinetica[i:i+pa.noParticulas] for i in range (0,len(energiacinetica),pa.noParticulas)]
