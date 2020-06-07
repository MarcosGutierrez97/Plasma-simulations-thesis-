# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:36:26 2020

@author: Marcos Gutierrez
"""
import numpy as np
import scipy as sp
#################################
# Parametros para el ciclo del PIC
#################################

#Parametros principales
noParticulas = 20000 #Numero de particulas
noMalla = 1024 #puntos de la malla
carga_e = -1 #electron
carga_i = 1 #ion
time_step = 2000 #para beamplasma #150 para two stream
vh = 6 #velocidad media del haz. Para pruebas 2-stream y Beam Stream


#Parametros de la malla
coor_malla = [float(i) for i in range(noMalla+1)]
campoEx = np.zeros(noMalla + 1)
x_inicial = np.zeros(noParticulas)
malla_longitud = 32*np.pi #Tamano de la malla espacial #32pi para two stream y beam plasma
plasma_inicio = 0
plasma_final = malla_longitud

#Parametros operacionales
dx = malla_longitud/noMalla
dt = 0.1

#Parametros de las particulas
carga_masa = -1 #relacion carga masa
rho0 = 1 #Densidad del fondo de iones (default)
x0 = 0.0 #perturbacion de amplitud
v0 = 0.0 #perturbacion de velocidad
densidadI = rho0 #densidad ionica


#Parametros energeticos
ki =[0.0 for i in range (time_step + 1)]
kdrift =[0 for i in range (time_step + 1)]
upot =[0.0 for i in range (time_step + 1)]
totalenergy =[0.0 for i in range (time_step + 1)]
x_i = plasma_final - plasma_inicio #Longitud de donde va a cargar la malla
espacio_particulas = x_i / noParticulas
carga = -rho0 * espacio_particulas
m = carga/carga_e #masa
