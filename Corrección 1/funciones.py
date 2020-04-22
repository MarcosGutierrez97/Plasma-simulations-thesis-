
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
    x_0 = []
    x_i = pa.plasma_final-pa.plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i/pa.noParticulas
    carga = -pa.rho*espacio_particulas
    masa = carga/pa.carga_masa # ? NO SE USA

    for i in range(pa.noParticulas):
        x_0.append(pa.plasma_inicio + espacio_particulas*(i+0.5))
        x_0[i] += pa.x0*np.cos(x_0[i])
    return x_0

###### Para que se necesita esta funcion?
def buildgrid_vel():
    #velocidades
    #plasma frio
    v_0 = []
    for i in range(pa.noParticulas):
        v_0.append(0) # ??? Hay que definir antes a v_0
    return v_0


def electricfield(rho0): #Le di por trapecio porque un chingo lo hacian asi. ✓ virgo
    rho_neto = pa.densidadI + rho0 #Corregido
    rho_N =[rho_neto]
    integrante = pa.dx * sp.arange(pa.noMalla + 1)
    Ex = integrate.cumtrapz(rho_neto,integrante,initial = integrante[0])
    E_i = sp.sum(Ex)

#Condiciones de frontera
    Ex[0:pa.noMalla] = E_i/pa.noMalla
    Ex[pa.noMalla] = Ex[0]
    return Ex


def chargevelocity(x0,E0):
    '''
    Implementando Ecuacion 8 de Martin.pdf

    '''
    #Extrapolación del campo eléctrico (no lo había puesto)
    pos = x0
    E = E0
    E_particula = []
    for i in range(pa.noParticulas):
        Ep = (1-(pos[i]/pa.dx-i))*E[i] +  (pos[i]/pa.dx-i)*E[i+1]
        E_particula.append(Ep)



    v = [-pa.dt/2] #Condición necesaria para el método de integración Leap-Frog

    for i in range(pa.noParticulas):
        vel = v[i] + pa.carga_masa * E_particula[i] * pa.dt
        v.append(vel)

    return v




def chargeposition(v0):
    '''
    Implementando Ecuacion 9 de Martin.pdf
    '''
    x = [0] #Condición necesaria para el método de integración Leap-Frog
    v_med = v0
    for i in range(pa.noParticulas):
        pos = x[i] +  v_med[i] * pa.dt
        x.append(pos)

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
    charge_density = [q_e]

    for i in range(pa.noMalla):
        rho_i_1 = q_e * (x[i] / pa.dx - i) / pa.dx
        charge_density.append(rho_i_1)

    return charge_density
