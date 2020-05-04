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
print(len(x_inicial))
v_inicial = f.buildgrid_vel() #Solo se hace una vez
print(len(v_inicial))
x_inicial = f.leapfrog(x_inicial,v_inicial)
densidad_inicial = f.chargedensity(x_inicial)
E_inicial = f.electricfield(densidad_inicial)
E_particulas_inicial = f.FieldParticle(x_inicial,E_inicial)
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



while  i < 0.3:
    if i == 0:
        posicion = f.chargeposition( v_inicial,x_inicial)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(x_inicial, v_inicial, E_inicial)
        densidad = f.chargedensity(posicion)
        E = f.electricfield(densidad)
        K = f.Kenergy(v_inicial)
        posiciones = np.append(posiciones, posicion)
        velocidades = np.append(velocidades,velocidad)
        densidades = np.append(densidades, densidad)
        camposE = np.append(camposE, E)
        energiacinetica = np.append(energiacinetica, K)
        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])
    else:
        posicion = f.chargeposition(velocidad, posicion)
        posicion = f.cf(posicion)
        velocidad = f.chargevelocity(posicion, velocidad, E)
        densidad = f.chargedensity(posicion)
        E = f.electricfield(densidad)
        K = f.Kenergy(velocidad)
        posiciones = np.append(posiciones, posicion)
        velocidades = np.append(velocidades, velocidad)
        densidades = np.append(densidades, densidad)
        camposE = np.append(camposE, E)
        energiacinetica = np.append(energiacinetica, K)
        p = p + 1 #Cuando agrego esto mi tira error:


        #camposE_particulas.append([v/(pa.carga_e*pa.dt) for v in velocidades[j]])

    i = i + pa.dt
    tiempo.append(i)

posiciones = [posiciones[i:i + pa.noParticulas] for i in range (0, len(posiciones),pa.noParticulas)]
velocidades = [velocidades[i:i + pa.noParticulas] for i in range (0, len(velocidades),pa.noParticulas)]
camposE = [camposE[i:i+pa.noMalla+1] for i in range(0,len(camposE),pa.noMalla+1)]
densidades = [densidades[i:i+pa.noMalla+1] for i in range(0,len(densidades),pa.noMalla+1)]
energiacinetica = [energiacinetica[i:i+pa.noParticulas] for i in range (0,len(energiacinetica),pa.noParticulas)]
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

#Campo electrico en el tiempo
"""
grafE = []
for i in range(len(camposE)):
    grafE.append(camposE[i][0]) #nodo 0
plt.plot(tiempo,grafE)
plt.show()
"""
"""
grafK = []
for i in range(len(energiacinetica)):
    grafK.append(energiacinetica[i][i])
plt.plot(tiempo, grafK)
plt.show()
"""

#Diagramas de fase de la particula 0
x = []
y = []

#xgrid = pa.dx*np.arange(pa.noMalla + 1)
#plt.scatter(xgrid, -(pa.densidadI + densidades[3]))

#plt.scatter(xgrid, camposE[1])
#plt.xlim(0,pa.malla_longitud)
#plt.ylim(-1,-0.75)
#plt.show()
print (len(densidades))
print (posiciones[1])
print(velocidades[1])
