# OBTENDO OS SHOTS A PARTIR DOS MODELOS DE VELOCIDADE


Esta pasta contém scripts que podem ser utilizados para geração do modelo direto utilizando o software Devito.

Abaixo apresento 3 shots gerados a partir do respectivo código, onde apresentamos os shots gerados a partir de fontes localizadas a 100, 1500 e 2900 metros de distância.

<img src="./figures/shots.png">


Todos os shots foram gerados com o auxílio do devito na versão 4.0, é possível realizar a instalação do mesmo pelo link [https://www.devitoproject.org/]. Também possuo um conteiner com a distribuição utilizada nesse projeto disponível no dockerHub conforme
 o link [https://hub.docker.com/r/jmtargino/devito].

Utilizando o comando "docker pull jmtargino/devito" você pode utilizar a distribuição a distribuição mais conveniente para o seu uso.



Um exemplo de um modelo de velocidade utilizado para gerar os shots pode ser visualizado logo abaixo, o mesmo apresenta as dimensões (201,301)


<img src="./figures/vmodel.png">


# COMO EXECUTAR A SIMULAÇÃO


Como executamos todos os nossos experimentos em um servidor, o software utilizado no mesmo para submissão de jobs é chamado Slurm. Logo, nessa pasta temos o arquivo ```main.sh``` que é responsável por estabelecer a versão paralela desse código, assim como também estabelecer as diretrizes de submissão do job de acordo com o nó mais apropriado para tal tipo de aplicação.

Enquanto o arquivo ```main_shot.py``` contém o Script de execução do modelo no devito.

Logo temos o seguinte fluxo:

1 - Leitura do modelo de velocidade (201,301) 

2 - Aplicação do respectivo modelo de velocidade no devito e obtenção do modelo direto.

3 - Após a obtenção dos shotRecords com dimensão (2000,29), todos os conjuntos de shots são salvos na pasta georec/.


Dentro dessa pasta também dispomos de um código que pode ser utilizado para adição de borda, entretanto, não o utilizamos, visto que o devito nos fornece um parâmetro chamado `sponge_size` que é responsável por adicionar a borda no modelo de velocidade.

* Caso você queira utilizar nosso método de adição de borda ao modelo de velocidade, utilize o código presente em olds/HamJacobi/. Tal código também pode ser encontrado no github [https://github.com/krober10nd/HamJacobi].


# INSTALAÇÃO

Para estes experimentos nós estamos utilizando o python na versão `3.8`

Após isso, siga os passos abaixo: 

### Instalando o Virtualenv
```
pip install virtualenv
```

### Criando e ativando o virtualenv, nesse caso chamamos nosso virtualenv de devito
```
virtualenv -p python3 venv-devito
source venv-devito/bin/activate
```
### Vá para a pasta do venv-devito
```
cd venv-devito/
```
### Instale o Requirements 
```
pip install -r requirements.txt

