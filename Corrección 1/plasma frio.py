# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:02:51 2020

@author: HP
"""

import funciones as f
import parametros as pa
import numpy as np


#Ciclo inicial. Este solo se hace una vez


x_inicial = f.buildgrid_pos()
v_inicial = f.buildgrid_vel()
densidad_inicial = f.chargedensity(x_inicial,pa.densidadE)
E_inicial = f.electricfield(densidad_inicial)
print (f.chargevelocity(x_inicial,v_inicial, E_inicial))
print (len(f.chargevelocity(x_inicial,v_inicial, E_inicial)))



#Se empieza a constuir el ciclo

temp = pa.dt

# while temp < 0.5:  # proba esto despues, primero que te corra una vez

    #Mover particulas
posicion = f.chargeposition(v_inicial)
velocidad = f.chargevelocity(x_inicial,v_inicial, E_inicial)
