# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:02:51 2020

@author: HP
"""

import funciones as f
import parametros as pa
import numpy as np
import matplotlib.pyplot as plt

"""
PARAMETROS: 1000 PARTICULAS, 100 NODOS, 300 CICLOS, STEP TEMPORAL DE 0.001, PERTURBACION 0.001
PARA VER BIEN LA GRAFICA DE LAS ENERGIAS AMPLIE A 1500 CICLOS, PERO SOLO PARA
VER LA ENERGIA
"""
#Ciclo inicial. Este solo se hace una vez
step = 0
xgrid =pa.dx*np.arange(pa.noMalla + 1) #necesario para graficar
posicion1 = f.buildgrid_pos(pa.x_inicial) #Solo se hace una vez
velocidad1 = f.buildgrid_vel() #Solo se hace una vez
posicion1 = f.leapfrog(posicion1,velocidad1)
posicion1 = f.cf(posicion1)
densidad1 = f.chargedensity(posicion1)
E1 = f.electricfield(densidad1)
K1 = f.Kenergy(velocidad1,0)
U1 = f.Uenergy(E1,0)
drift1 = f.drift(velocidad1,0)
T1 = f.totalenergy(K1,U1)



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
energiacinetica = []
energiapotencial = []
energiatotal = []
DRIFT = []
#densidad de carga
path_p = "C:/Users/HP/Documents/GitHub/Plasma-simulations-thesis-/Corrección 1/plasmafrio_resultados/densidad/"
#campo electrico
path_e = "C:/Users/HP/Documents/GitHub/Plasma-simulations-thesis-/Corrección 1/plasmafrio_resultados/campo electrico/"
#diagrama de fase
path_f = "C:/Users/HP/Documents/GitHub/Plasma-simulations-thesis-/Corrección 1/plasmafrio_resultados/diagrama de fase/"
#energias
path_k = "C:/Users/HP/Documents/GitHub/Plasma-simulations-thesis-/Corrección 1/plasmafrio_resultados/energia/"
while  t < pa.time_step*pa.dt:
    if t == 0:
        posicion = posicion1
        posicion = f.cf(posicion)
        velocidad = velocidad1
        densidad = densidad1
        E = E1
        K = K1
        drift = drift1
        U = U1
        T = T1
        """
        plt.scatter(posicion, velocidad)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Plasma frío:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "plasmafrioDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("Ex")
        plt.title("Plasma frío: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "plasmafrioE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("densidad de carga")
        plt.title("Plasma frío: densidad de carga" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_p + "plasmafrioDC" + str(step) + ".png")
        plt.clf()
        """
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
        energiacinetica = K
        energiapotencial = U
        DRIFT = drift
        """
        plt.scatter(posicion, velocidad)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Plasma frío:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "plasmafrioDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("Ex")
        plt.title("Plasma frío: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "plasmafrioE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("densidad de carga")
        plt.title("Plasma frío: densidad de carga" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_p + "plasmafrioDC" + str(step) + ".png")
        plt.clf()
        """

        #f.diagnosticos(t)


    #f.diagnosticos(densidad, E,t,graf)
    t = t + pa.dt
    step = step + 1
    tiempo.append(t)
for  u in range (len(energiacinetica)):
    energiatotal.append(energiacinetica[u] + energiapotencial[u])

#posiciones = [posiciones[i:i + pa.noParticulas] for i in range (0, len(posiciones),pa.noParticulas)]
#velocidades = [velocidades[i:i + pa.noParticulas] for i in range (0, len(velocidades),pa.noParticulas)]
#camposE = [camposE[i:i+pa.noMalla+1] for i in range(0,len(camposE),pa.noMalla+1)]
#densidades = [densidades[i:i+pa.noMalla+1] for i in range(0,len(densidades),pa.noMalla+1)]
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
plt.plot(tiempo,energiacinetica, 'r', label = "K")
plt.plot(tiempo, energiapotencial, label = "U")
plt.plot(tiempo, energiatotal,  label = "T")
plt.plot(tiempo, DRIFT, label = " Drift")
plt.xlabel("Tiempo")
plt.ylabel("Energía")
plt.xlim(0,pa.malla_longitud)
plt.legend()
plt.savefig(path_k + "plasmafrioDC" + str(step) + ".png")
plt.show()
