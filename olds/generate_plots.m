close all;
origem= pwd;
modelos = [1,10,100];
% modelos=[1];
pos_sources = [1,10,20,29];

main(origem,modelos,pos_sources)


function savefig()
    fig=gcf;                                     % your figure
    fig.PaperPositionMode='auto';

    print(fig, '-dpsc', '-append', 'file.ps')
    close all;
end


function get_shots(pos,pos_sources)
    f_init=4;
    f_fim =60;
    passo=3;
    
    for i = f_init: passo:f_fim
        disp(strcat('Frequencia:', num2str(i)));
        pasta = strcat('shots/georec',num2str(i),'/');
        shot = load(strcat(pasta,'georec',num2str(pos), '.mat'));
        shot = shot.rec;
        
        for k =1: size(pos_sources,2)
            subplot(1,size(pos_sources,2),k);
            shot_i = shot(:,:,pos_sources(k));
            imshow(shot_i);
            title(strcat('F:',num2str(i),'hz | P:',num2str(pos_sources(k))));
        
            
        end
        savefig()
        
        
    end


end

function main(origem,modelos,pos_sources)
    qtd_modelos= size(modelos,2);
    for i =1: qtd_modelos
        cd (origem);
        pos = modelos(i);
        nome = strcat('vmodels/vmodel',num2str(pos),'.mat');
        vmodel = load(nome);
        vmodel = vmodel.vmodel;
        imagesc(vmodel);
        title(strcat('vmodel',num2str(i)))
        savefig()
        
        get_shots(pos,pos_sources);
        
    end
end
