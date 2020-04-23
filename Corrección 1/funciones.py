
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
    rho_neto = 1 + rho0
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
    for i in range(pa.noParticulas):
        x_dx = pos[i]/pa.dx
        j1 = int(x_dx)
        j2 = j1 + 1
        b2 = x_dx - j1
        b1 = 1.0 - b2
        Ex = b1*E[j1] + b2*E[j2]
        E_particula.append(Ex)
        v[i] = v[i] + pa.carga_masa * Ex * pa.dt
        

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
    q_e = pa.carga_e / pa.dx
    charge_density = np.zeros(pa.noMalla + 1)
    for i in range(pa.noParticulas):
        x_dx = x[i]/pa.dx
        j1 = int(x_dx)
        j2 = j1 + 1
        b2 = x_dx - j1
        b1 = 1.0 - b2
        charge_density[j1] = charge_density[j1] + q_e * b1
        charge_density[j2] = charge_density[j2] + q_e * b2
        
        #Condiciones de frontera
        charge_density[0] += charge_density[pa.noMalla]
        charge_density[0] = charge_density[pa.noMalla]
        

    
    return charge_density
