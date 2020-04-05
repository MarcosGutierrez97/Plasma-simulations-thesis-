# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:13:12 2020

@author: HP
"""

import parametros as pa
import numpy as np
#################################
# Funciones para el ciclo del PIC
#################################

# Es mas eficiente asi:
"""
puntos_malla = [i for i in range(pa.NoPpC)]

"""
#TODO ESTO LO ESTOY HACIENDO SOLO PARA PLASMA FRIO, PERO LOS DEMAS CASOS SOLO SERIA DE AGREGAR DISTRIBUCIONES

def buildgrid_pos(): 
    #posiciones:
    x_0 = []
    x_i = pa.malla_final-pa.plasma_inicio #Longitud de donde va a cargar la malla
    espacio_particulas = x_i/pa.noParticulas
    carga = -pa.rho*espacio_particulas
    masa = carga/pa.carga_masa
    
    for i in range(pa.noParticulas):
        x_0[i] = pa.plasma_inicio + espacio_particulas*(i+0.5)
        x_0[i] += pa.x0*np.cos(x_0[i])
    return x_0


 def buildgrid_vel():
     #velocidades 
    #plasma frio
    v_0[1:pa.noParticulas] = 0
    return v_0
     
        
    
    

def electricfield(): #Le di por trapecio porque un chingo lo hacian asi.
    rho_neto = pa.rho + pa.rhoE
    rho_N =[rho_neto]
    Ex = []
    Ex[pa.noMalla] = 0
    E_i = 0
    for i in range(pa.noMalla-1,-1,-1):
        Ex[i] = Ex[i+1] - 0.5*(rho_N[i] + rho_N[i+1])*pa.dx
        E_i = E_i + Ex[i]
    
    #Condiciones de frontera
    Ex[0:pa.noMalla] -= E_i/pa.noMalla
    Ex[pa.noMalla] = Ex[0]
    return Ex


def chargevelocity(E):
    '''
    Implementando Ecuacion 8 de Martin.pdf 
    '''
    v = [-pa.dt/2] #Condición necesaria para el método de integración Leap-Frog
    E = electricfield()
    for i in range(pa.noParticulas):
        vel = v[i] + pa.carga_masa * E[i] * pa.dt
        v.append(vel)

    return v




def chargeposition(v_med):
    '''
    Implementando Ecuacion 9 de Martin.pdf 
    '''
    x = [0] #Condición necesaria para el método de integración Leap-Frog
    v_med = chargevelocity()
    for i in range(pa.noParticulas):
        pos = x[i] +  v_med[i] * pa.dt
        x.append(pos)

    return x
def cf(x_cf):
    x = chargeposition()
    for i in range(pa.noParticulas):
        if x[i] < pa.malla_inicio:
            x[i] += pa.malla_final
        elif x[i] > pa.malla_final:
            x[i] -= pa.malla_final
    return True 
            
            

def chargedensity(carga_e, x):
    '''
    Implementando Ecuaciones 20 y 21 de Martin.pdf
    Solo si X[0] = 0 (revisa que esto suceda) YA SUCEDE
    '''
    x = chargeposition()
    q_e = pa.carga_e / pa.dx
    charge_density = [q_e]

    for i in range(pa.noParticulas):
        rho_i_1 = q_e * (x[i] / pa.dx - i) / pa.dx
        charge_density.append(rho_i_1)

    return charge_density


