
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


def chargevelocity(x0,v0,E0):
    '''
    Implementando Ecuacion 8 de Martin.pdf

    '''
    #Extrapolación del campo eléctrico (no lo había puesto)
    v = v0
    pos = x0
    E = E0
    E_particula = []
    C1 = [] #pa.coor_malla[j+1] - x[i]
    C2 = [] #x[i]-pa.coor_malla[j]
    i = 0 #contador noParticulas
    j = 0 #Contador campo electrico
    q = 0 #segundo contador de noParticulas
    p = 0 #segundo contador de malla
    while i <= pa.noParticulas-1:
        if x[i] >= pa.coor_malla[j] and x[i] >= pa.coor_malla[j+1]:
            E_particula.append((x[i]-pa.coor_malla[j])*E[j] + (pa.coor_malla[j+1]-x[i])*E[j+1])
            i= i + 1
        else:
            j = j + 1

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
    return True



def chargedensity(x0):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''
    x = x0
    charge_density = [0.0 for g in range(pa.noMalla)]

    i = 0 #Contador para particulas en x_i
    k = 1 #Contador para particulas en x_i+1 = i+1
    j = 0#Contador para malla
    while j < (pa.noMalla):
        while i < (pa.noParticulas):
            if x[i] >= pa.coor_malla[j] and x[i] <= pa.coor_malla[j+1]:
                c1 = (pa.carga_e*(pa.coor_malla[j+1] - x[i])) #rho_i
                c2 = (pa.carga_e*(x[i] - pa.coor_malla[j])) #rho_i+1
                if charge_density[i]  != 0.0:
                    charge_density[i] = charge_density[i] + c1
                    charge_density[i+1] = c2
                else:
                    charge_density[i] = c1
                    charge_density[i+1] = c2






                i = i + 1
                k = k + 1
            else:
                j = j+1
    i = 0
    k = 1
    j = 0

    return charge_density
