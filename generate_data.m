matriz = load('/home/jonas/Downloads/vmodels_wborder.mat');
matriz = matriz.vmodels_border;

cd ('/home/jonas/Desktop/vmodel2');
for i =1: 2000
    disp (i);
    vmodel = matriz{i};
    %vmodel = uint16(vmodel);
    nome = strcat('vmodel',num2str(i),'.mat');
    vmodel = vmodel(1:201,51:351);
    save(nome,"vmodel");
    
end

