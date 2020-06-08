# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:02:51 2020

@author: Marcos Gutierrez
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



E_acumulado = np.empty((pa.noMalla + 1, pa.time_step + 1))
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
#densidad de carga
path_p = "C:/Users/HP/Documents/graficas tesis/plasmafrio_resultados/densidad/"
#campo electrico
path_e = "C:/Users/HP/Documents/graficas tesis/plasmafrio_resultados/campo electrico/"
#diagrama de fase
path_f = "C:/Users/HP/Documents/graficas tesis/plasmafrio_resultados/diagrama de fase/"
#energias
path_k = "C:/Users/HP/Documents/graficas tesis/plasmafrio_resultados/energia/"

plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
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
        for q in range(1,pa.noMalla + 1):
            E_acumulado[q:step] = E[q]
        print (E)
        print (E_acumulado)
        """
        plt.scatter(posicion, velocidad)
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-pa.x0,pa.x0)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Plasma frío:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "plasmafrioDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-pa.x0,pa.x0)
        plt.xlabel("posición malla")
        plt.ylabel("Ex")
        plt.title("Plasma frío: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "plasmafrioE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-pa.x0,pa.x0)
        plt.xlabel("posición malla")
        plt.ylabel("densidad")
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
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
        for q in range(1,pa.noMalla + 1):
            E_acumulado[q:step] = E[q]
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
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-pa.x0,pa.x0)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Plasma frío:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "plasmafrioDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-pa.x0,pa.x0)
        plt.xlabel("posición malla")
        plt.ylabel("Ex")
        plt.title("Plasma frío: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "plasmafrioE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("posición malla")
        plt.ylabel("densidad")
        plt.title("Plasma frío: densidad de carga" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_p + "plasmafrioDC" + str(step) + ".png")
        plt.clf()
        """

    t = t + pa.dt
    step = step + 1
    tiempo.append(t)
for  u in range (len(energiacinetica)):
    energiatotal.append(energiacinetica[u] + energiapotencial[u])

#energias
"""
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
"""
