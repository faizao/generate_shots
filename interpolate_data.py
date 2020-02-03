#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 07:08:31 2019

@author: jonas
"""

import scipy.io as sio
#import torch
#
matriz = sio.loadmat('/home/jonas/Desktop/georec/georec1.mat') #load matriz
matriz = matriz['rec'] # Peguei a matriz
dimension = 2000;

from scipy.interpolate import interp1d
import numpy as np


x = np.array(range(matriz.shape[0]))

# define new x range, we need 7 equally spaced values
xnew = np.linspace(x.min(), x.max(), dimension)

# apply the interpolation to each column
f = interp1d(x, matriz, axis=0)

# get final result
aux= (f(xnew))
