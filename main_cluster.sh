#!/bin/bash

#SBATCH -o /home/jonas/log_shots.txt
#SBATCH --partition=intel
#SBATCH -N 1
#SBATCH -J devitoJ
module load python-3.6.8-gcc-8.3.0-pfdclbj #modulo com devito


f_start=4 #minha frequência inicial
f_end=50 #frequência final

for frequencia in $(seq $f_start $f_end) #Varrendo todas as frequências
do    

    python3 cluster.py $frequencia 

done
# Nesse script utilizo todos os processadores para gerar os shots records, utilizo os 40 ao mesmo tempo por meio de threads, com isso a execução é mais rápida. Os parâmetros $1 e $2 são respectivamente o modelo inicial e final para cada modelo de velocidade
