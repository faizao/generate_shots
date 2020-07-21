#!/bin/bash
#SBATCH -o /home/jonas/genshots/log.txt
#SBATCH --partition=intel_large
#SBATCH -N 1
#SBATCH -J jmtFCN
#SBATCH --ntasks-per-node=20
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jonasm.targino@gmail.com


module load py-devito-4.2.1-intel-20.0.166-eiizm6q
#export OMP_NUM_THREADS=20
#export DEVITO_LANGUAGE=openmp
#export OMP_PROC_BIND=close
#export OMP_PLACES=cores
#export DEVITO_ARCH=gcc
#export DEVITO_PLATFORM=skx

DEVITO_LANGUAGE=openmp OMP_NUM_THREADS=20 DEVITO_ARCH=gcc DEVITO_PLATFORM=skx numactl --cpunodebind=1 --membind=1 python3 main_shot.py
