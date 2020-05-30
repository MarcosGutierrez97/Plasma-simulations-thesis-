
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 14:13:12 2020

@author: HP
"""

import parametros as pa
import numpy as np
import scipy as sp
from scipy import integrate
from scipy.stats import maxwell
from scipy.fftpack import fft2
from scipy.fftpack import fftshift as shift
import matplotlib.pyplot as plt
#################################
# Funciones para el ciclo del PIC
#################################

# Es mas eficiente asi:
"""
puntos_malla = [i for i in range(pa.NoPpC)]

"""
# Todo ESTO LO ESTOY HACIENDO SOLO PARA PLASMA FRIO, PERO LOS DEMAS CASOS SOLO SERIA DE AGREGAR DISTRIBUCIONES

def nextpow2(x):
    n = 1
    while n < x: n *= 2
    return n

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
    pa.campoEx[pa.noMalla] = 0.0
    E_i = 0.0
    for j in range(pa.noMalla-1,-1,-1):
      pa.campoEx[j] = pa.campoEx[j+1] - 0.5*( rho_neto[j] + rho_neto[j+1] )*pa.dx
      E_i = E_i + pa.campoEx[j]


    #Condiciones de frontera
    pa.campoEx[0:pa.noMalla] -= E_i / pa.noMalla
    pa.campoEx[pa.noMalla] = pa.campoEx[0]
    """
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


def cf(x_cf):
    for i in range(pa.noParticulas):
        if x_cf[i] < pa.plasma_inicio:
            while x_cf[i] < pa.plasma_inicio:
                x_cf[i] += pa.plasma_final
        elif x_cf[i] > pa.plasma_final:
            while x_cf[i] > pa.plasma_final:
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

def Kenergy(v,step):
    v2 = [x**2 for x in v]
    pa.ki[step] =  0.5*pa.m*sum(v2)
    return pa.ki

def Uenergy (Ex,step):
    e2 = [x**2 for x in Ex]
    pa.upot[step] = 0.5*pa.dx*sum(e2)
    return pa.upot


def totalenergy (k,u):
    for i in range(pa.time_step):
        pa.totalenergy[i] = k[i] + u[i]
    return pa.totalenergy
def drift(v,step):
    vdrift = sum(v)/pa.noParticulas
    pa.kdrift[step] = 0.5*pa.m*(vdrift**(2))*pa.noParticulas
    return pa.kdrift



#FUNCION PARA INESTABILIDAD TWO STREAM PLASMA
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
#FUNCION PARA INESTABLIDAD BEAM PLASMA
def buildgrid_vel_ibp (x):
    velocidad = []
    v_m = pa.vh
    n_l = pa.noParticulas * 0.9 #90% de las particulas estan a una velocidad menor
    n_m = pa.noParticulas * 0.1 #10% de las particulas van a una velocidad mayor
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

def dispersionfria(k,w,path_k,E_acumulado):

    E_muestreado = E_acumulado[0:pa.noMalla:1,0:pa.time_step:5]
    E_wk = fft2(E_muestreado,(nextpow2(pa.noMalla),nextpow2(pa.noMalla)))/pa.malla_longitud
    E_wk_abs = abs(E_wk)
    E_wk_shift = shift(E_wk_abs)
    print(E_wk_shift)
    plt.plot(k,w, 'k', label = '$\omega_{p}$')
    plt.xlabel('k')
    plt.ylabel('$\omega$')
    #plt.xticks(np.linspace(0,2,8))
    #plt.yticks(np.linspace(0,1,5))
    plt.contourf(pa.K, pa.W,E_wk_shift, 9 ,alpha = 0.75, cmap = 'jet')
    #plt.xlim(0,4)
    plt.ylim(0,2)
    plt.colorbar()
    plt.legend()
    plt.savefig(path_k + "dispersion"  + ".png")
    plt.show()

    return True
