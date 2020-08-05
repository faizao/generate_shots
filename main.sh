#!/bin/bash
#SBATCH -o log_shots.txt
#SBATCH --partition=intel_large
#SBATCH -N 1
#SBATCH -J jmtFCN
#SBATCH --mail-type=ALL
#SBATCH --mail-user=jonasm.targino@gmail.com

module load py-devito-4.2.1-intel-20.0.166-eiizm6q

DEVITO_ARCH=gcc DEVITO_PLATFORM=skx python3 principal.py

