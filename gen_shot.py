# AUTHOR: KEITH ROBERTS AND JONAS MENDONCA
# PURPOSE: This script takes a synthetic velocity model describing the P-wave velocity field as an input 
# and runs a forward model of the acoustic wave equation. For each synthetic model, it saves a shot record. 
import argparse
import numpy as np
from devito import configuration
from examples.seismic import Model,Receiver,AcquisitionGeometry,plot_shotrecord
from examples.seismic.acoustic import AcousticWaveSolver
from devito import Function, clear_cache, TimeFunction
import scipy.io as sio
from scipy.interpolate import interp1d
configuration['log-level'] = 'WARNING'


parser = argparse.ArgumentParser(description='How to use this program')
parser.add_argument("-f", "--freq", type=int, required=True, help="Frequency")
parser.add_argument("-m", "--model", type=int, required=True, help="Number of the model")
parser.add_argument("-p", "--path", type=str, required=True, help="origin path")
parser.add_argument("-d", "--destino", type=str, required=True, help="Destination path")
args = parser.parse_args()

frequency = args.freq
num_model = args.model
path = args.path
destino = args.destino

# all parameters below try to follow Yang and Ma as closely as possible 
# Deep-learning inversion: A next-generation seismic velocity model building method
#NumModels  = 1001       # number of synthetic velocity models 
nshots     = 29      # 29 shots equally spaced across top of domain (30 m below the surface)
nreceivers = 301      # One recevier every grid point
t0         = 0.      # Simulation starting time (0 ms)
tn         = 2000.    # Simulation last 2. seconds (2000 ms)
deltat     = 1        # model timestep (in ms)
#f0         = 0.0040    # Source peak frequency is 4.0 Hz(0.0040 kHz)
shape      = (301, 201) # Number of grid point (nx, nz)
spacing    = (10., 10.) # Grid spacing in m. 
origin     = (0., 0.)   # What is the location of the top left corner. This is necessary to define
SPACE_ORDER = 4         # spatial leading order of method 
SPONGE_SIZE  = 100        # sponge layer size in grid points bordering side of grid 
dimension = 2000;


def interpolate_data(matriz,dimension):
    x = np.array(range(matriz.shape[0]))
    
    xnew = np.linspace(x.min(), x.max(), dimension)
    
    # apply the interpolation to each column
    f = interp1d(x, matriz, axis=0)
    aux= (f(xnew))
    return np.float32(aux)


model = 'vmodel' + str(num_model) + '.mat'
modelname = path + model
print("Frequencia{} Processing model :{}".format(str(frequency), str(model)))

# loading my data .mat
v = sio.loadmat(modelname)
v = v['vmodel']
v = v.transpose()
v = v / 1000  # normalizando meu dado para executar mais rapido e nao ficar na escala de gigabytes
# para os dados do marmousi não precisa normalizar

model = Model(vp=v, origin=origin, shape=shape,
              spacing=spacing, space_order=SPACE_ORDER, bcs="damp", nbl=SPONGE_SIZE)

# source
source_position = np.empty((1, 2), dtype=np.float32)
source_position[0, 0] = 0.0
source_position[0, 1] = 0.0

# Prepare the 29 (nshots) varying source locations sources across the top of the domain
source_locations = np.empty((nshots, 2), dtype=np.float32)
source_locations[:, 0] = np.linspace(0., 3000, num=nshots)
source_locations[:, 1] = 20.

# Initialize receivers for collection of shot records
rec_coordinates = np.empty((nreceivers, 2))
rec_coordinates[:, 0] = np.linspace(0, model.domain_size[0], num=nreceivers)
rec_coordinates[:, 1] = 20.

f0 = frequency * 0.001
geometry = AcquisitionGeometry(model, rec_coordinates, source_position,
                               t0, tn, f0=f0, src_type='Ricker')

solver = AcousticWaveSolver(model, geometry, space_order=SPACE_ORDER)
clear_cache()
for SHOT_NUM in range(0, 29):
    print(num_model, '-', SHOT_NUM)
    clear_cache()
    geometry.src_positions[0, :] = source_locations[SHOT_NUM, :]
    true, _, _ = solver.forward(vp=model.vp)

    if SHOT_NUM == 0:
        rec = np.zeros((true.data.shape[0], 301, 29))

    data = true.data
    rec[:, :, SHOT_NUM] = data

rec = interpolate_data(rec, dimension)  # interpolo meus dados para a dimensão (201,301)
ofname = destino + 'georec{}.mat'.format(str(num_model))
print("Saving result to :", ofname)
sio.savemat(ofname, {'rec': rec})



