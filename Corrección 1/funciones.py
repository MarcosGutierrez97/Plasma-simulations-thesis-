
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:13:12 2020

@author: HP
"""

import parametros as pa
import numpy as np
import scipy as sp
from scipy import integrate
import matplotlib.pyplot as plt
#################################
# Funciones para el ciclo del PIC
#################################

# Es mas eficiente asi:
"""
puntos_malla = [i for i in range(pa.NoPpC)]

"""
# Todo ESTO LO ESTOY HACIENDO SOLO PARA PLASMA FRIO, PERO LOS DEMAS CASOS SOLO SERIA DE AGREGAR DISTRIBUCIONES

def buildgrid_pos(x_0):
    #posiciones:
    x_i = pa.plasma_final - pa.plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i / pa.noParticulas
    carga = -pa.rho0 * espacio_particulas
    masa = carga/pa.carga_masa

    for i in range(pa.noParticulas):
        x_0[i] =  pa.plasma_inicio + espacio_particulas * (i + 0.5)
        x_0[i] += pa.x0 * np.cos(2*np.pi*x_0[i])
    return x_0

def leapfrog(x,v): #Necesaria para que el proceso de Leapfrog sea valido
    for i in range (len(x)):
        x[i] = x[i] + 0.5 * pa.dt * v[i]
    return x


def buildgrid_vel():
    #velocidades
    #plasma frio
    v_0 = np.zeros(pa.noParticulas)
    v_0[1:pa.noParticulas] = 0.0

    return v_0


def electricfield(rho0): #Le di por trapecio porque un chingo lo hacian asi. ✓ virgo
    rho_neto = 1.0 + rho0

    integrante = pa.dx * sp.arange(pa.noMalla + 1)
    Ex = integrate.cumtrapz(rho_neto, integrante, initial=integrante[0])
    E_i = sp.sum(Ex)
    """
    Ex[pa.noMalla] = 0.0
    edc = 0.0
    for j in range(pa.noMalla-1,-1,-1):
      Ex[j] = Ex[j+1] - 0.5*( rho_neto[j] + rho_neto[j+1] )*pa.dx
      edc = edc + Ex[j]
    """

    #Condiciones de frontera
    Ex[0:pa.noMalla] -= E_i / pa.noMalla
    Ex[pa.noMalla] = Ex[0]
    return Ex


def chargevelocity(x,v, E_malla):
    '''
    Implementando Ecuacion 8 de Martin.pdf

    '''
    #Extrapolación del campo eléctrico (no lo había puesto)
    for k in range (pa.noParticulas):
        xa = x[k]/pa.dx
        j1 = int(xa)
        j2 = j1 + 1
        f2 = xa - j1
        f1 = 1.0 - f2
        ex = f1*E_malla[j1] + f2*E_malla[j2]
        v[k] = v[k] + pa.carga_e*pa.dt*ex
    return v



def chargeposition(v_med, x):
    '''
    Implementando Ecuacion 9 de Martin.pdf
    '''
#Condición necesaria para el método de integración Leap-Frog
    for i in range(pa.noParticulas):
        x[i] = x[i] +  v_med[i] * pa.dt
    return x


def cf(x_cf): ### ? Nunca usas x_cf, y no se por que regresar True R/: Las uso despues de moverlas las particulas, pero como aun no ha sucedido, jaja.
    for i in range(pa.noParticulas):
        if x_cf[i] < pa.plasma_inicio:
            #while x_cf[i] < pa.plasma_inicio:
            x_cf[i] += pa.plasma_final
        elif x_cf[i] > pa.plasma_final:
            #while x_cf[i] > pa.plasma_final:
            x_cf[i] -= pa.plasma_final
    return x_cf



def chargedensity(x):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''
    j1=np.dtype(np.int32)
    j2=np.dtype(np.int32)
    charge_density = np.zeros(pa.noMalla + 1)
    qe = -1*((pa.plasma_final-pa.plasma_inicio)/pa.noParticulas)
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

def Kenergy(v,step):
    x_i = pa.plasma_final - pa.plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i / pa.noParticulas
    carga = -pa.rho0 * espacio_particulas
    m = carga/pa.carga_masa
    v2 = [x**2 for x in v]
    pa.ki[step] = pa.ki[step] + 0.5*m*sum(v2)
    return pa.ki

def Uenergy (Ex,step):
    e2 = [x**2 for x in Ex]
    pa.upot[step] =pa.upot[step] + 0.5*pa.dx*sum(e2)
    return pa.upot


def totalenergy (k,u):
    for i in range(pa.noMalla):
        pa.totalenergy[i] = k[i] + u[i]
    return pa.totalenergy


#Funciones para graficar
"""
def diagnosticos(t):
    xgrid =pa.dx*np.arange(pa.noMalla + 1)
    graf = (np.pi/pa.dt/16)
    if t == 0:
        plt.figure('Campos')
        plt.clf()
        if graf > 0:
            if np.fmod(t,graf) == 0:
                #densidad
                plt.subplot(2,2,1)
                if t > 0:
                    plt.cla()
                plt.plot(xgrid, -(pa.densidadI + chargedensity(x)),'r', label = 'densidad')
                plt.xlabel('x')
                plt.xlim(0,pa.malla_longitud)
                #Campo electrico
                plt.subplot(2,2,2)
                if t > 0:
                    plt.cla()
                plt.plot(xgrid, electricfield(rho0), 'b', label = 'Campo electrico')
                plt.xlabel('x')
                plt.xlim(0,pa.malla_longitud)
                plt.show()
    return True
"""
