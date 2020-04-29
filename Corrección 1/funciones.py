
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:13:12 2020

@author: HP
"""

import parametros as pa
import numpy as np
import scipy as sp
from scipy import integrate
#################################
# Funciones para el ciclo del PIC
#################################

# Es mas eficiente asi:
"""
puntos_malla = [i for i in range(pa.NoPpC)]

"""
# TODO ESTO LO ESTOY HACIENDO SOLO PARA PLASMA FRIO, PERO LOS DEMAS CASOS SOLO SERIA DE AGREGAR DISTRIBUCIONES

#Necesaria para rho y E
def closed_range(start, stop, step=1):
  dir = 1 if (step > 0) else -1
  return range(start, stop + dir, step)

def buildgrid_pos():
    #posiciones:
    x_0 = np.array([])
    x_i = pa.plasma_final - pa.plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i / pa.noParticulas
    carga = -pa.rho * espacio_particulas
    masa = carga/pa.carga_masa ### no se usa

    for i in range(pa.noParticulas):
        x_0 = np.append(x_0, pa.plasma_inicio + espacio_particulas * (i + 0.5))
        x_0[i] += pa.x0 * np.cos(x_0[i])
    return x_0


def buildgrid_vel():
    #velocidades
    #plasma frio
    v_0 = np.array([])
    for i in range(pa.noParticulas):
        v_0 = np.append(v_0, 0)
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


def chargevelocity(x,v,E):
    '''
    Implementando Ecuacion 8 de Martin.pdf

    '''
    #Extrapolación del campo eléctrico (no lo había puesto)
    E_particula = [0 for a in range (pa.noParticulas)]
    i = 0 #Contador para C_i
    j = 1#Contador para C_i+1
    #Acorde a la presentacion de plasma del CERN
    k = 0 #Contador de particulas
    vel = 0
    while k < (pa.noParticulas):
        if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[j]:
            c1 = (pa.carga_e*(pa.coor_malla[j] - x[k])) #rho_i
            c2 = (pa.carga_e*(x[k] - pa.coor_malla[i])) #rho_i+1
            E_particula[k] = E_particula[k] + (E[i]*c2 + E[j] * c1)
            v[k] = v[k] - E_particula[k]*pa.dt  #pa.carga_e*E_particula[vel]*pa.dt
            k = k + 1
        else:
            k = k + 1
            i = i + 2
            j = j + 2

    #while vel < (pa.noParticulas):
        #v[vel] = v[vel] + pa.carga_e*E_particula[vel]*pa.dt

    return v






def chargeposition(v_med):
    '''
    Implementando Ecuacion 9 de Martin.pdf
    '''
    x = np.array([0.0]) #Condición necesaria para el método de integración Leap-Frog
    # v_med = v0
    for i in range(pa.noParticulas):
        pos = x[i] +  v_med[i] * pa.dt
        x = np.append(x, pos)

    return x


def cf(x_cf): ### ? Nunca usas x_cf, y no se por que regresar True R/: Las uso despues de moverlas las particulas, pero como aun no ha sucedido, jaja.
    x = chargeposition()
    for i in range(pa.noParticulas):
        if x[i] < pa.plasma_inicio: ### Faltan malla_inicio y malla_final en parametros.py #R/: era plasma_algo
            x[i] += pa.plasma_final
        elif x[i] > pa.plasma_final:
            x[i] -= pa.plasma_final
    return x



def chargedensity(x,charge_density):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''

    i = 0 #Contador para C_i
    j = 1#Contador para C_i+1
    malla = 0 #Contador de nodos
    #Acorde a la presentacion de plasma del CERN
    k = 0


    while k < (pa.noParticulas):
        if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[j]:
            c1 = (pa.carga_e*(pa.coor_malla[j] - x[k])) #rho_i
            charge_density[i] = charge_density[i] + c1
            c2 = (pa.carga_e*(x[k] - pa.coor_malla[i])) #rho_i+1
            charge_density[j] = charge_density[j] + c2
            k = k + 1
        else:
            k = k + 1
            i = i + 2
            j = j + 2

    return charge_density
