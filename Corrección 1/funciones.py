
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:13:12 2020

@author: Marcos Gutierrez
"""

import parametros as pa
import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
#################################
# Funciones para el ciclo del PIC
#################################


#FUNCION PARA POSICIONES INICIALES
def buildgrid_pos(x_0):
    #posiciones:
    plasma_inicio = 0.0
    plasma_final = pa.malla_longitud
    x_i = plasma_final - plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i / pa.noParticulas
    carga = -pa.rho0 * espacio_particulas
    masa = carga/pa.carga_e

    for i in range(pa.noParticulas):
        x_0[i] =  plasma_inicio + espacio_particulas * (i + 0.5)
        x_0[i] += pa.x0 * np.cos(x_0[i])
    return x_0

def leapfrog(x,v): #Necesaria para que el proceso de Leapfrog sea valido
    for i in range (len(x)):
        x[i] = x[i] + 0.5 * pa.dt * v[i]
    return x

#FUNCION PARA LA VELOCIDAD DE PLASMA FRIO
def buildgrid_vel():
    #velocidades
    #plasma frio
    v_0 = np.zeros(pa.noParticulas)
    v_0[1:pa.noParticulas] = 0.0

    return v_0

#FUNCION PARA LA VELOCIDAD DE LA INESTABILIDAD TWO STREAM PLASMA
def buildgrid_vel_2bp(x):
    velocidad = np.zeros(pa.noParticulas)
    for i in range(pa.noParticulas):
        #Construcción de la distribución Maxwelliana de la velocidad
        f_velmax = 0.5*(1 + sp.exp(-2*(pa.vh**2)))
        vmin = -5 * pa.vh
        vmax = 5*pa.vh
        v_temp = vmin + (vmax-vmin)*(sp.random.random())
        f_vel = 0.5 * (sp.exp(-(v_temp - pa.vh)*(v_temp - pa.vh) / 2.0) + sp.exp(-(v_temp + pa.vh)*(v_temp + pa.vh) / 2.0))
        x_temp = f_velmax*(sp.random.random())
        while x_temp >f_vel:
            f_velmax = 0.5*(1 + sp.exp(-2*pa.vh*pa.vh))
            vmin = (-5) * pa.vh
            vmax = 5*pa.vh
            v_temp = vmin + (vmax-vmin)*(sp.random.random())
            f_vel = 0.5 * (sp.exp(-(v_temp - pa.vh)*(v_temp - pa.vh) / 2.0) + sp.exp(-(v_temp + pa.vh)*(v_temp + pa.vh) / 2.0))
            x_temp = f_velmax*(sp.random.random())
            va_temp = v_temp + pa.v0*np.cos(2*np.pi*x[i]/pa.malla_longitud)
        velocidad[i] = va_temp
    return velocidad
#FUNCION PARA LA VELOCIDAD DE LA INESTABLIDAD BEAM PLASMA
def buildgrid_vel_ibp (x):
    velocidad = []
    v_m = pa.vh
    n_l = pa.noParticulas * 0.9 #90% de las particulas
    n_m = pa.noParticulas * 0.1 #10% de las particulas 
    v_s = (v_m * n_m)/(n_l-n_m)

    for i in range (pa.noParticulas):
        f_velmax =0.5*(1 + sp.exp(-2.0*(v_m**2)))
        vmin = -2*v_m
        vmax = 2*v_m
        v_temp = vmin + (vmax - vmin)*(np.random.random())
        f =  (1-(n_m/n_l))*np.exp(-(v_temp - v_s)*(v_temp - v_s)/1.0) + (n_m/n_l)*np.exp(-(v_temp - v_m)*(v_temp - v_m)/1.0)
        x_temp = f_velmax*(np.random.random())
        while x_temp > f:
            f_velmax =0.5*(1 + sp.exp(-2.0*(v_m**2)))
            vmin = -2*v_m
            vmax = 2*v_m
            v_temp = vmin + (vmax - vmin)*(np.random.random())
            f =  (1-(n_m/n_l))*np.exp(-(v_temp - v_s)*(v_temp - v_s)/1.0) + (n_m/n_l)*np.exp(-(v_temp - v_m)*(v_temp - v_m)/1.0)
            x_temp = f_velmax*(np.random.random())
        velocidad.append(v_temp+ pa.v0*np.cos(2*np.pi*x[i]/pa.malla_longitud) )
    return velocidad

#FUNCION DEL CAMPO ELECTRICO
def electricfield(rho0):
    rho_neto = 1.0 + rho0

    integrante = pa.dx * sp.arange(pa.noMalla + 1)
    Ex = integrate.cumtrapz(rho_neto, integrante, initial=integrante[0])
    E_i = sp.sum(Ex)
    return Ex


#FUNCION QUE ACUTUALIZA VELOCIDADES
def chargevelocity(x,v, E_malla):

    for k in range (pa.noParticulas):
        xa = x[k]/pa.dx
        j1 = int(xa)
        j2 = j1 + 1
        f2 = xa - j1
        f1 = 1.0 - f2
        ex = f1*E_malla[j1] + f2*E_malla[j2]
        v[k] = v[k] + pa.carga_e*pa.dt*ex
    return v


#FUNCION QUE ACUTALIZA POSICIONES
def chargeposition(v_med, x):
#Condición necesaria para el método de integración Leap-Frog
    for i in range(pa.noParticulas):
        x[i] = x[i] +  v_med[i] * pa.dt
    return x

#FUNCION QUE VERIFICA LAS CONDICIONES DE FRONTERA
def cf(x_cf):
    for i in range(pa.noParticulas):
        if x_cf[i] < pa.plasma_inicio:
            while x_cf[i] < pa.plasma_inicio:
                x_cf[i] += pa.plasma_final
        elif x_cf[i] > pa.plasma_final:
            while x_cf[i] > pa.plasma_final:
                x_cf[i] -= pa.plasma_final
    return x_cf


#FUNCION QUE CALCULA LA DENSIDAD DE CARGA
def chargedensity(x):
    j1=np.dtype(np.int32)
    j2=np.dtype(np.int32)
    charge_density = np.zeros(pa.noMalla + 1)
    qe = -pa.rho0*((pa.plasma_final-pa.plasma_inicio)/pa.noParticulas)
    re = (qe/pa.dx)
    for k in range (pa.noParticulas):
        xa = x[k]/pa.dx
        j1 = int(xa)
        j2 = j1 + 1
        f2 = xa - j1
        f1 = 1.0 - f2
        charge_density[j1] = charge_density[j1] + re*f1
        charge_density[j2] = charge_density[j2] + re*f2

    charge_density[0] += charge_density[pa.noMalla]
    charge_density[pa.noMalla] = charge_density[0]


    return charge_density
#ENERGIA CINETICA
def Kenergy(v,step):
    v2 = [x**2 for x in v]
    pa.ki[step] =  0.5*pa.m*sum(v2)
    return pa.ki
#ENERGIA POTENCIAL
def Uenergy (Ex,step):
    e2 = [x**2 for x in Ex]
    pa.upot[step] = 0.5*pa.dx*sum(e2)
    return pa.upot

#ENERGIA TOTAL
def totalenergy (k,u):
    for i in range(pa.time_step):
        pa.totalenergy[i] = k[i] + u[i]
    return pa.totalenergy

#DRIFT DE ENERGIA
def drift(v,step):
    vdrift = sum(v)/pa.noParticulas
    pa.kdrift[step] = 0.5*pa.m*(vdrift**(2))*pa.noParticulas
    return pa.kdrift
