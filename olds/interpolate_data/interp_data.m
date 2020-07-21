% 
% a = [7,15,20,25,29];
dimensao = [2000,301];
origem = '/home/jonas/Desktop/';
destino = '/home/jonas/Desktop/';

% for i=1: size(a,2)
%     pasta = a(i);
%     cd (strcat('/home/jonas/Desktop/georec_train20',num2str(pasta),'/'));

for k=1001: 1002
    cd (origem);
    disp (k);
%     disp(strcat(num2str(pasta),num2str(k)));
    nome = strcat('georec',num2str(k),'.mat');
    data = load(nome);% /home/jonas/Desktop/georec_train15/georec1.mat
    data = data.rec;
    
    delete(nome);
    
    L  = size(data, 1);
    rec = interp1(1:L, data, linspace(1, L, dimensao(1)));
    cd (destino);
    save(nome,'rec');
    
    
end
% end
