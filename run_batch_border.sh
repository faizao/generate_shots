#!/bin/bash
python3 main_shot_border.py 1 200 &
python3 main_shot_border.py 201 400 & 
python3 main_shot_border.py 401 600 & 
python3 main_shot_border.py 601 800 &
python3 main_shot_border.py 801 1000 & 
python3 main_shot_border.py 1001 1200 & 
python3 main_shot_border.py 1201 1400 &
python3 main_shot_border.py 1401 1600 & 
python3 main_shot_border.py 1601 1800 &
python3 main_shot_border.py 1801 2001 & 


# Nesse script utilizo 10 processadores para gerar os shots records, utilizo os 10 ao mesmo tempo por meio de threads, com isso a execução é mais rápida. Os parâmetros $1 e $2 são respectivamente o modelo inicial e final para cada modelo de velocidade
