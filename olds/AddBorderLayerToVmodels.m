clearvars; close all; clc;
origem = '/home/jonas/Desktop/vmodels';
destino = '/home/jonas/Desktop/vmodels_border';

%load vmodels_2000.mat

dims = [251,402,1]; % note: nz MUST be 1 for 2D fields.
elen = 10 ; % size of grid cell
dfdx = 1e-6 ; % decimal fraction representing smoothness
itmax = 1000; % maximum number of iterations to perform

xvec_o = 1:301; 
zvec_o = 1:201; 
[xg_o,zg_o]=meshgrid(xvec_o,zvec_o); 

xvec_n = -50:301+50; 
zvec_n = 1:201+50; 
[xg_n,zg_n]=meshgrid(xvec_n,zvec_n); 

for i = 1 : 2001
    cd (origem);
    nome = strcat('vmodel',num2str(i),'.mat');
    vmodel = load(nome);
    vp_o = vmodel.vmodel;
    % interp old grid onto new using NN interp
    temp = interp2(xg_o,zg_o,vp_o,xg_n,zg_n,'nearest',1486);
    field = 1./temp(:);
    % gradient limit border zone to avoid reflections
    vp = FastHJ( int32(dims), elen, dfdx, int32(itmax), field);
    
    vp_n = reshape(1./vp,[251, 402, 1]);
    
    idx = knnsearch([zg_o(:),xg_o(:)],[zg_n(:),xg_n(:)]); 
    
    % replace the original model 
    vp_n(1:201,51:301+50) = vp_o; 
    
    %vmodels_border{i} = vp_n ; 
    %subplot(1,2,1);imagesc(vp_o);subplot(1,2,2);imagesc(vp_n);
    vmodel = vp_n;
    cd(destino);
    vmodel= vmodel/1000;
    vmodel = single(vmodel);
    save(nome,'vmodel');
 
    i
    %figure; pcolor(vp_n); shading interp;
end