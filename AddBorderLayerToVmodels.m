clearvars; close all; clc;

load vmodels_2000.mat

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

for i = 1 : 2e3
    vp_o = vmodels{i};
    % interp old grid onto new using NN interp
    temp = interp2(xg_o,zg_o,vp_o,xg_n,zg_n,'nearest',1486);
    field = 1./temp(:);
    % gradient limit border zone to avoid reflections
    vp = FastHJ( int32(dims), elen, dfdx, int32(itmax), field);
    
    vp_n = reshape(1./vp,[251, 402, 1]);
    
    idx = knnsearch([zg_o(:),xg_o(:)],[zg_n(:),xg_n(:)]); 
    
    % replace the original model 
    vp_n(1:201,51:301+50) = vp_o; 
    
    vmodels_border{i} = vp_n ; 

    i
    %figure; pcolor(vp_n); shading interp;
end