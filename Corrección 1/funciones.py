
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


def buildgrid_vel(v_0):
    #velocidades
    #plasma frio
    v_0[1:pa.noParticulas] = 0
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
    j = 1#Contador para C_i+1
    #Acorde a la presentacion de plasma del CERN
    k = 0 #Contador de particulas
    vel = 0

    for k in range (pa.noParticulas):
        if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[i + 1]:
            c1 = ((pa.coor_malla[i + 1] - x[k])) #rho_i
            c2 = ((x[k] - pa.coor_malla[i])) #rho_i+1
            E_particula.append((E_malla[i]*c1 + E_malla[i+1] * c2))
            v[k] = v[k] + pa.carga_e*E_particula[k]*pa.dt
            k = k + 1
        elif x[k] > pa.coor_malla[i + 1]:
            i = i + 1
    return v

def FieldParticle (x,E_malla): #Campo aplicado a cada particula
    E_a_particula = []
    i = 0 #Contador para C_i
    j = 1#Contador para C_i+1
    #Acorde a la presentacion de plasma del CERN
    k = 0 #Contador de particulas
    for k in range (pa.noParticulas):
        if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[i + 1]:
            c1 = ((pa.coor_malla[i + 1] - x[k])) #rho_i
            c2 = ((x[k] - pa.coor_malla[i])) #rho_i+1
            E_a_particula.append((E_malla[i]*c1 + E_malla[i+1] * c2))
            #print (k)
            k = k + 1

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



def chargedensity(x,charge_density):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''
    charge_density = np.zeros(pa.noMalla + 1)
    i = 0 #Contador para C_i
    j = 1#Contador para C_i+1
    malla = 0 #Contador de nodos
    #Acorde a la presentacion de plasma del CERN
    k = 0


    while k < (pa.noParticulas):
        if x[k] >= pa.coor_malla[i] and x[k] <= pa.coor_malla[i + 1]:
            c1 = (pa.carga_e*(pa.coor_malla[i + 1] - x[k])) #rho_i
            charge_density[i] = charge_density[i] + c1
            c2 = (pa.carga_e*(x[k] - pa.coor_malla[i])) #rho_i+1
            charge_density[i + 1] = charge_density[i + 1] + c2
            k = k + 1
        elif x[k] > pa.coor_malla[i + 1]:
            i = i + 1
    charge_density[0] = charge_density[0] + charge_density[pa.noMalla]
    charge_density[pa.noMalla] = charge_density[0]

    return charge_density

def Kenergy(v):
    vdrift = sum(v)/pa.noParticulas
    v2 = []
    ki = [0.0 for i in range(len(v))]
    for i in range (len(v)):
        v2.append ((v[i])**2)
        ki[i] = (0.5*(sum(v2))) # masa = 1, por la normalizacion
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
