
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
    masa = carga/pa.carga_masa ### no se usa

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
    v_0 = [0.0 for i in range (pa.noParticulas)]
    return v_0


def electricfield(rho0): #Le di por trapecio porque un chingo lo hacian asi. ✓ virgo
    rho_neto = pa.densidadI + rho0
    integrante = pa.dx * sp.arange(pa.noMalla + 1)
    Ex = integrate.cumtrapz(rho_neto, integrante, initial=integrante[0])
    E_i = sp.sum(Ex)

    #Condiciones de frontera
    Ex[0:pa.noMalla] = E_i / pa.noMalla
    Ex[pa.noMalla] = Ex[0]
    return Ex


def chargevelocity(x,v,E_malla):
    '''
    Implementando Ecuacion 8 de Martin.pdf

    '''
    #Extrapolación del campo eléctrico (no lo había puesto)

    E_particula = []
    i = 0 #Contador para C_i
    for k in range (pa.noParticulas):
        xa = x[k]/pa.dx
        j1 = int(xa)
        print (j1)
        j2 = j1 + 1
        print (j2)
        f2 = xa - j1
        f1 = 1.0 - f2
        ex = f1*E_malla[j1] + f2*E_malla[j2]
        v[k] = v[k] + pa.carga_e*pa.dt*ex
    '''
    for k in range (pa.noParticulas):
        if int(x[k]/pa.dx) >= pa.coor_malla[i] and int(x[k]/pa.dx) <= pa.coor_malla[i + 1]:
            E_particula.append((E_malla[i]*(1-(int(x[k]/pa.dx)-i)) + E_malla[i+1] *(int(x[k]/pa.dx)-i)))
            v[k] = v[k] + pa.carga_e*E_particula[k]*pa.dt
        elif x[k] > pa.coor_malla[i + 1]:
            i = i + 1
    '''
    return v

def FieldParticle (x,E_malla): #Campo aplicado a cada particula
    E_a_particula = []
    i = 0 #Contador para C_i
    #Acorde a la presentacion de plasma del CERN
    for k in range (pa.noParticulas):
        if (x[k]/pa.dx) >= pa.coor_malla[i] and (x[k]/pa.dx) <= pa.coor_malla[i + 1]:
            E_a_particula.append((E_malla[i]*(1-((x[k]/pa.dx)-i)) + E_malla[i+1] *((x[k]/pa.dx)-i)))

        elif x[k] > pa.coor_malla[i + 1]:
            i = i + 1
    return E_a_particula






def chargeposition(v_med, x):
    '''
    Implementando Ecuacion 9 de Martin.pdf
    '''
#Condición necesaria para el método de integración Leap-Frog
    """
    El error de la línea 64 de plasma frío igual salía si quitaba x = [0 for pos in range (pa.noParticulas)]
    para hacer chargeposition(v,x) y así sumar el cambio a la posición anterior. No he podido descifrar porqué.
    """
    for i in range(pa.noParticulas):
        x[i] = x[i] +  v_med[i] * pa.dt
    return x


def cf(x_cf): ### ? Nunca usas x_cf, y no se por que regresar True R/: Las uso despues de moverlas las particulas, pero como aun no ha sucedido, jaja.
    for i in range(pa.noParticulas):
        if x_cf[i] < pa.plasma_inicio: ### Faltan malla_inicio y malla_final en parametros.py #R/: era plasma_algo
            x_cf[i] += pa.plasma_final
        elif x_cf[i] > pa.plasma_final:
            x_cf[i] -= pa.plasma_final
    return x_cf



def chargedensity(x):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''
    charge_density = np.zeros(pa.noMalla + 1)
    re = pa.carga_e/pa.dx
    i = 0 #Contador para C_i
    j = 1#Contador para C_i+1
    malla = 0 #Contador de nodos
    #k = 0
    #Acorde a la presentacion de plasma del CERN
    for k in range (pa.noParticulas):
        xa = x[k]/pa.dx
        j1 = int(xa)
        j2 = j1 + 1
        f2 = xa - j1
        f1 = 1.0 - f2
        charge_density[j1] = charge_density[j1] + re*f1
        charge_density[j2] = charge_density[j2] + re*f2
        """
        if int(x[k]/pa.dx)>= pa.coor_malla[i] and int(x[k]/pa.dx) <= pa.coor_malla[i + 1]:
            charge_density[i] = charge_density[i] + pa.carga_e*(1-i-int(x[k]/pa.dx))
            charge_density[i + 1] = charge_density[i + 1] + pa.carga_e*(int(x[k]/pa.dx)-i)
            k = k + 1
        elif x[k] > pa.coor_malla[i + 1]:
            i = i + 1
    charge_density[0] = charge_density[0] + charge_density[pa.noMalla]
    charge_density[pa.noMalla] = charge_density[0]
    """

    return charge_density

def Kenergy(v):
    vdrift = sum(v)/pa.noParticulas
    #v2 = []
    ki = [0.0 for i in range(len(v))]
    for i in range (len(v)):
        #v2.append ((v[i])**2)
        ki[i] = (0.5*((v[i])**2)) # masa = 1, por la normalizacion
        #kdrift[i] = 0.5*vdrift*vdrift*pa.noParticulas #esta y la siguiente linea puede ser utiles
        #therm[i] = ki[i]-kdrift[i]
    return ki

def Uenergy (Ex,upot):
    e2 = []
    Emax = max(Ex)
    for i in range (pa.noParticulas):
        e2.append((Ex[i])**2)
        upot[i] = 0.5*pa.dx*sum(e2)

    return upot

def totalenergy (totalenergy,k,u):
    for i in range(pa.noParticulas):
        totalenergy[i] = k[i] + u[i]
    return totalenergy


#Funciones para graficar

def diagnosticos(densidad, E, t, graf):
    xgrid =pa.dx*np.arange(pa.noMalla + 1)
    if t == 0:
        plt.figure('Campos')
        plt.clf()
        if graf > 0:
            if np.fmod(t,graf) == 0:
                #densidad
                plt.subplot(2,2,1)
                if t > 0:
                    plt.cla()
                plt.plot(xgrid, -(pa.densidadI + densidad),'r', label = 'densidad')
                plt.xlabel('x')
                plt.xlim(0,pa.malla_longitud)
                #Campo electrico
                plt.subplot(2,2,2)
                if t > 0:
                    plt.cla()
                plt.plot(xgrid, E, 'b', label = 'Campo electrico')
                plt.xlabel('x')
                plt.xlim(0,pa.malla_longitud)
                plt.show()
    return True
