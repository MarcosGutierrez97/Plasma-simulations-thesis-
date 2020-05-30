# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:36:26 2020

@author: HP
"""
import numpy as np
import scipy as sp
from scipy.fftpack import fft2
from scipy.fftpack import fftshift as shift

#Parametros del experimentos (tomados de Brisdall et tal)
def nextpow2(x):
    n = 1
    while n < x: n *= 2
    return n

noParticulas = 10000 #Numero de particulas
noMalla = 1000 #puntos de la malla
carga_e = -1 #electron
carga_i = 1 #ion
time_step = 200 #para beamplasma #150 para two stream
vh = 6 #velocidad media del haz. Para pruebas 2-stream y Beam Stream


#Arrays de la malla

#Variables principales
coor_malla = [float(i) for i in range(noMalla+1)]
#print(coor_malla)
#print (len(coor_malla))
campoEx = np.zeros(noMalla + 1)
x_inicial = np.zeros(noParticulas)
malla_longitud = 32*np.pi #Tamano de la malla espacial #32pi para two stream y beam plasma
plasma_inicio = 0
plasma_final = malla_longitud
dx = malla_longitud/noMalla
dt = 0.1
carga_masa = -1 #relacion carga masa
rho0 = 1 #Densidad del fondo de iones (default)
x0 = 0.1 #perturbacion de amplitud
v0 = 0.0 #perturbacion de velocidad
densidadI = rho0


#Parametros energeticos
ki =[0.0 for i in range (time_step + 1)]
kdrift =[0 for i in range (time_step + 1)]
upot =[0.0 for i in range (time_step + 1)]
totalenergy =[0.0 for i in range (time_step + 1)]
x_i = plasma_final - plasma_inicio #Longitud de donde va a cargar la malla
espacio_particulas = x_i / noParticulas
carga = -rho0 * espacio_particulas
m = carga/carga_e #MASA

#Parametros para la relación de dispersión
w_p = 1
w_pp = w_p*np.ones(noParticulas)
w_min = 2*np.pi/(dt)/2/(time_step/2)
w_max = w_min*(time_step/2)
k_min = 2*np.pi/(noMalla)
k_max = k_min*((noMalla/2)-1)

k_teorica = np.linspace(0,k_max,noParticulas)
k_simulada = np.linspace(-k_max,k_max,nextpow2(noMalla))
w_teorica = np.linspace(0,malla_longitud,noMalla+1)
w_simulada = np.linspace(-w_max,w_max,nextpow2(noMalla))

K , W = np.meshgrid(k_simulada,w_simulada)
