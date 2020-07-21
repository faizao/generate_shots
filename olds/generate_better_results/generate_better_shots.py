#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:15:01 2020

@author: jonas
"""

import scipy.io as sio
import matplotlib.pyplot as plt


shot = sio.loadmat('recdata.mat');
shot = shot['rec']; #dimensão (20904,1348)
shot = shot[1:-1:25,1:-1:2] # dimensão (837,673)



def generate_better_results(shot):
        
    limiar = 1e-7
    
    
    positions = shot <= limiar; #this variable is logical
    
    shot[positions] = shot[positions] +0.6;
    
    
    plt.imshow(shot, cmap='binary')



generate_better_results(shot)