# AUTHOR: KEITH ROBERTS, JONAS MENDONCA AND JAIME FREIRE
# PURPOSE: This script takes a synthetic velocity model describing the P-wave velocity field as an input 
# and runs a forward model of the acoustic wave equation. For each synthetic model, it saves a shot record. 
import threading
import subprocess
import os

def run(frequency,num_model,path,destino):
    subprocess.run(['python3','gen_shot.py', '-f', str(frequency), '-m', str(num_model), '-p', path,  '-d', destino])

if __name__ == "__main__":
    path = './vmodel/' #is mandatory
    base_destino = './shots/freq-'
    num_cores = 63
    start_model = 1
    end_model = 10000
    frequencies=[10,15,20]
    
    for frequency in frequencies:
        destino= base_destino+str(frequency)+ '/' #example ./shots/freq-20/ with 20 hz
        os.makedirs(destino, exist_ok=True)
        contador=start_model
        
        while(contador <= end_model):
            
            threads=[]
            for i in range(num_cores):
                if (contador <= end_model):
                    t1 = threading.Thread(target = run,args=(frequency,contador,path,destino,)) #creating thread and pass args to def run
                    threads.append(t1)
                    t1.start()
                    contador+=1 
                else:
                    break
            
            for t in threads:
                t.join()