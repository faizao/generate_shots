# AUTHOR: KEITH ROBERTS AND JONAS MENDONÃ‡A
# PURPOSE: This script takes a synthetic velocity model describing the P-wave velocity field as an input 
# and runs a forward model of the acoustic wave equation. For each synthetic model, it saves a shot record. 

import numpy as np
from devito import configuration
from examples.seismic import Model #, plot_velocity, plot_perturbation
from examples.seismic import AcquisitionGeometry
from examples.seismic.acoustic import AcousticWaveSolver
from devito import Function, clear_cache, TimeFunction
from devito import clear_cache
from examples.seismic import Receiver
from examples.seismic import plot_image
from scipy import ndimage
#import matplotlib.pyplot as plt
import scipy.io as sio
from examples.seismic import plot_shotrecord
import os 
from scipy import interpolate
import sys
from scipy.interpolate import interp1d
import numpy as np
configuration['log-level'] = 'WARNING'

path = '/home/jonas/Desktop/vmodel2/'
destino = '/home/jonas/Desktop/georec/'

# all parameters below try to follow Yang and Ma as closely as possible 
# Deep-learning inversion: A next-generation seismic velocity model building method
NumModels  = 2000       # number of synthetic velocity models 
nshots     = 29      # 29 shots equally spaced across top of domain (30 m below the surface)
nreceivers = 301          # One recevier every grid point
t0         = 0.      # Simulation starting time (0 ms)
tn         = 2000.    # Simulation last 2. seconds (2000 ms)
deltat     = 1        # model timestep (in ms)
#f0         = 0.0040    # Source peak frequency is 4.0 Hz(0.0040 kHz)
shape      = (402, 251) # Number of grid point (nx, nz)
spacing    = (10., 10.) # Grid spacing in m. 
origin     = (0., 0.)   # What is the location of the top left corner. This is necessary to define
SPACE_ORDER = 4         # spatial leading order of method 
SPONGE_SIZE  = 40        # sponge layer size in grid points bordering side of grid 
dimension = 2000;
f = 20  #frequency

inicio=int(sys.argv[1])
fim = int(sys.argv[2])



def interpolate_data(matriz,dimension):
    x = np.array(range(matriz.shape[0]))
    
    xnew = np.linspace(x.min(), x.max(), dimension)
    
    # apply the interpolation to each column
    f = interp1d(x, matriz, axis=0)
    aux= (f(xnew))
    return np.float32(aux)


#for nm in range(1,2):

for nm in range(inicio,fim+1):
#    nm=1001
# Define a synthetic "true" velocity profile. The velocity is in km/s
# load in velocity model
    model = 'vmodel'+str(nm)+'.mat'
    modelname = path+model
    print("Frequencia{} Processing model :{}".format(str(f),str(model)))
    v= sio.loadmat(modelname)
    v = v['vmodel']
    v = v.transpose() 
    v = v/1000 #normalizando meu dado para executar mais rÃ¡pido e nÃ£o ficar na escala de gigabytes
    #para os dados do marmousi não precisa normalizar
                
    model = Model(vp=v, origin=origin, shape=shape,
                  spacing=spacing,space_order=SPACE_ORDER,nbpml=SPONGE_SIZE)
    
        # source 
    source_position = np.empty((1,2), dtype=np.float32)
    source_position[0,0] = 0.0
    source_position[0,1] = 0.0 
    
    # Prepare the 29 (nshots) varying source locations sources across the top of the domain
    source_locations = np.empty((nshots, 2), dtype=np.float32)
    source_locations[:,0] = np.linspace(800, 3250, num=nshots)
    source_locations[:,1] = 250.
    
    #plot_velocity(model, source=source_locations)
    
    # Initialize receivers for collection of shot records
    rec_coordinates = np.empty((nreceivers, 2))
    rec_coordinates[:, 0] = np.linspace(800, 3250, num=nreceivers)
    rec_coordinates[:, 1] = 250.
    
    
    f0 = f*0.001
    geometry = AcquisitionGeometry(model, rec_coordinates, source_position,
                                   t0, tn, f0=f0, src_type='Ricker')
    
    solver = AcousticWaveSolver(model, geometry, space_order=SPACE_ORDER)
        
    
    for SHOT_NUM in range(0,29):
        print (nm,'-',SHOT_NUM)
        clear_cache()
        geometry.src_positions[0, :] = source_locations[SHOT_NUM, :]
        true, _, _ = solver.forward(vp=model.vp)
        if SHOT_NUM == 0: 
            rec = np.zeros((true.data.shape[0],nreceivers,nshots))
       
        data = true.data
        rec[:,:,SHOT_NUM] = data
        SHOTRECORDS = 0
    
    rec = interpolate_data(rec,dimension)
    ofname = destino+'georec{}.mat'.format(str(nm))
    print("Saving result to :",ofname)
    sio.savemat(ofname, {'rec': rec})
    
    os.system('chmod 777 %s' %(ofname))
    aws_s3_path = 's3://seismic-data-ml-marmousi_tr_2000/shots/frequency{}/georec{}.mat'.format(f,nm)
    os.system('aws s3 cp %s %s' % (ofname, aws_s3_path))
    os.system('rm -f %s' %(ofname))
    
    
    
