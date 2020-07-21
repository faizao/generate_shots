#!/bin/bash
for i in $(seq 5 7)
do
    python3 main_shot_border.py 1 100 $i &
    python3 main_shot_border.py 101 200 $i & 
    python3 main_shot_border.py 201 300 $i & 
    python3 main_shot_border.py 301 400 $i &
    python3 main_shot_border.py 401 500 $i & 
    python3 main_shot_border.py 501 600 $i & 
    python3 main_shot_border.py 601 700 $i &
    python3 main_shot_border.py 701 800 $i & 
    python3 main_shot_border.py 801 900 $i &
    python3 main_shot_border.py 901 1000 $i & 
    python3 main_shot_border.py 1001 1100 $i & 
    python3 main_shot_border.py 1101 1200 $i & 
    python3 main_shot_border.py 1201 1300 $i &
    python3 main_shot_border.py 1301 1400 $i & 
    python3 main_shot_border.py 1401 1500 $i & 
    python3 main_shot_border.py 1501 1600 $i &
    python3 main_shot_border.py 1601 1700 $i & 
    python3 main_shot_border.py 1701 1800 $i &
    python3 main_shot_border.py 1801 1900 $i &
    python3 main_shot_border.py 1901 2001 $i &  

done

# Nesse script utilizo 10 processadores para gerar os shots records, utilizo os 10 ao mesmo tempo por meio de threads, com isso a execução é mais rápida. Os parâmetros $1 e $2 são respectivamente o modelo inicial e final para cada modelo de velocidade
