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
10000 PARTICULAS, 1000 NODOS, 200 CICLOS, STEP TEMPORAL DE 0.1, PERTURBACION DE 0.0
LONGITUD DE MALLA DE 32 PI. PARA VER COMO SE COMPORTA LA ENERGIA AMPLIE A 1000 CICLOS

PARA LANDAU AMPLIE A 1500 CICLOS, NADA MAS
"""
#Ciclo inicial. Este solo se hace una vez
step = 0
xgrid =pa.dx*np.arange(pa.noMalla + 1) #necesario para graficar
posicion1 = f.buildgrid_pos(pa.x_inicial) #Solo se hace una vez
velocidad1 = f.buildgrid_vel_2bp(posicion1) #Solo se hace una vez
posicion1 = f.leapfrog(posicion1,velocidad1)
posicion1 = f.cf(posicion1)
densidad1 = f.chargedensity(posicion1)
E1 = f.electricfield(densidad1)
K1 = f.Kenergy(velocidad1,0)
U1 = f.Uenergy(E1,0)
T1 = f.totalenergy(K1,U1)

#densidad de carga
path_p = "C:/Users/HP/Documents/graficas tesis/landau_resultados/densidad ts/"
#campo electrico
path_e = "C:/Users/HP/Documents/graficas tesis/landau_resultados/campo electrico ts/"
#diagrama de fase
path_f = "C:/Users/HP/Documents/graficas tesis/landau_resultados/diagrama de fase ts/"
#energias
path_k = "C:/Users/HP/Documents/graficas tesis/landau_resultados/energia ts/"

graf = (np.pi/pa.dt/16)
t = 0
p = 0
e = 1
posiciones= [posicion1]
velocidades = [velocidad1]
densidades = [densidad1]
camposE = [E1]
tiempo = []
energiacinetica = []
energiapotencial = []
energiatotal = []
vmas = []
vmenos = []
xmas = []
xmenos = []



while  t < pa.time_step*pa.dt:
    if t == 0:
        posicion = posicion1
        posicion = f.cf(posicion)
        velocidad = velocidad1
        densidad = densidad1
        E = E1
        K = K1
        U = U1
        T = T1
        """
        plt.scatter(posicion, velocidad)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Inestabilidad Two-stream:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "twostreamDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-8,8)
        plt.xlabel("x")
        plt.ylabel("Ex")
        plt.title("Inestabilidad Two-stream: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "twostreamE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-8,8)
        plt.xlabel("x")
        plt.ylabel("densidad de carga")
        plt.title("Inestabilidad Two-stream: densidad de carga" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_p + "twostreamDC" + str(step) + ".png")
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
        """
        plt.scatter(posicion, velocidad)
        plt.xlim(0,pa.malla_longitud)
        plt.xlabel("x")
        plt.ylabel("v")
        plt.title("Inestabilidad Two-stream:diagrama de fase" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_f + "twostreamDF" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, E)
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-8,8)
        plt.xlabel("x")
        plt.ylabel("Ex")
        plt.title("Inestabilidad Two-stream: campo eléctrico" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_e + "twostreamE" + str(step) + ".png")
        plt.clf()
        plt.scatter(xgrid, (densidad + 1))
        plt.xlim(0,pa.malla_longitud)
        plt.ylim(-8,8)
        plt.xlabel("x")
        plt.ylabel("densidad de carga")
        plt.title("Inestabilidad Two-stream: densidad de carga" + "  tiempo =" + str(round(t,2)))
        plt.savefig(path_p + "twostreamDC" + str(step) + ".png")
        plt.clf()
        """

    t = t + pa.dt
    step = step + 1
    tiempo.append(t)
for  u in range (len(energiacinetica)):
    energiatotal.append(energiacinetica[u] + energiapotencial[u])

#energias
plt.plot(tiempo,energiacinetica, 'r', label = "K")
plt.plot(tiempo, energiapotencial, label = "U")
plt.plot(tiempo, energiatotal,  label = "T")
plt.xlabel("Tiempo")
plt.ylabel("Energía")
plt.xlim(0,pa.malla_longitud)
plt.legend()
plt.savefig(path_k + "energiastwostreamDC" + str(step) + ".png")
plt.clf()
plt.plot(tiempo, energiapotencial, label = "U")
plt.xlabel("Tiempo")
plt.ylabel("Energía")
#plt.xlim(0,pa.malla_longitud)
plt.legend()
plt.savefig(path_k + "potencialTwostreamDC" + str(step) + ".png")

print ("energia K media")
print (sum(energiacinetica)/len(energiacinetica))
