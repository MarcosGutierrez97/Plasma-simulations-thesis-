# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:36:26 2020

@author: HP
"""
import numpy as np

#Parametros del experimentos (tomados de Brisdall et tal)

noParticulas = 10000 #Numero de particulas
noMalla = 1000 #puntos de la malla
carga_e = -1 #electron
carga_i = 1 #ion

#Arrays de las particulas

posiciones = np.zeros(noParticulas)
velocidades = np.zeros(noParticulas)

#Arrays de la malla

densidadE = np.zeros(noMalla + 1) #Densidad de electrones
densidadI = np.zeros(noMalla + 1) #Densidad de iones (el fondo de la malla)
#print(densidadE)
CampoEx = np.zeros(noMalla + 1)     #Campo electrico
potencialM = np.zeros(noMalla + 1)   #Potencial Magnetico

#Variables principales
E_particulaI = [0 for a in range (noParticulas)] #Campo individual aplicado a cada particula
coor_malla = [i for i in range(noMalla+1)]
#print(coor_malla)
#print (len(coor_malla))
x_inicial = np.zeros(noParticulas)
v_inicial = np.zeros(noParticulas)
malla_longitud = 1 #Tamano de la malla espacial
plasma_inicio = 0
plasma_final = malla_longitud
dx = malla_longitud/noMalla
dt = 0.05
carga_masa = -1 #relacion carga masa
rho0 = 1 #Densidad del fondo de iones (default)
velocidad_termica = 0.02
x0 = 0.01 #perturbacion de amplitud
v0 = 0.0 #perturbacion de velocidad
densidadI = rho0
print (densidadI)
