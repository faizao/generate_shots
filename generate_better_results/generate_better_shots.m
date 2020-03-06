close all; clear;

aux= load('recdata.mat').rec;
aux= aux(1:25:end,1:2:end); %reduzi para uma dimensão legal (837,674);


shot2 = make_better_shots(aux);

function shot2 = make_better_shots(shot)
    limiar = 1e-7;
    positions = shot <= limiar; %this variable is logical
    shot2 = shot;
    
    shot2(positions) = shot2(positions) +0.6;
    
    
    figure(1);imshow(shot);
    figure(2);imshow(shot2);
    
end