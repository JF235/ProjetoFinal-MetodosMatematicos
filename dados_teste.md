Pessoal,

Nessa reta final, vou disponibilizar alguns dados para vocês testarem a segunda parte do programa (projeto D).

Temos 4 satélites, com parâmetros dados por:

a = [15300, 16100, 17800, 16400] # km
e = [.41, .342, .235, .3725]
w = [60, 10, 30, 60] # deg
i = [30, 30, 0, 20] # deg
o = [0, 40, 40, 40] # deg
tp = [4708.5603, 5082.6453, 5908.5511, 5225.3666] # s
TOA = [60000] * 4 # us
TOT = [13581.1080927 , 19719.32768037, 11757.73393255, 20172.46081236] # us

    As unidades são colocadas nos comentários ao lado (depois do #).
    Observe que os sinais foram recebidos pelo receptor de forma sincronizada (TOA é igual para os 4). Não é preciso considerar o caso sem sincronia.
    A resolução na medida de tempo não é realista. No entanto, ela serve para verificar a resposta de forma mais precisa.

As posições resolvidas dos satélites (em km) são

[-17198.94636766, -3357.8884269 , -1938.67778718], 
[-16764.51326576, -188.27453647, 6138.26955927],
[-18646.04514963, -1962.47472564, 0. ],
[-12159.76207073, -13896.76819502, -1029.81652816]

Considerando a velocidade da luz como 300 km/ms, as medidas de distância ρi
são

[13925.66757219, 12084.20169589, 14472.67982024, 11948.26175629] # km

O gradiente da função $J(r)$ sugerida no relatório, avaliado no ponto (0, 0, 0) é

[17588.69754731, 6132.84921939, -1211.75969832]

O algoritmo deve convergir para a posição do drone

[-6420., -6432., 6325.] # km

O gradiente nesse ponto deve ser zero, pois se trata de um de mínimo (por imprecisões numéricas, provavelmente vai ser um valor diferente de zero, mas muito pequeno $∼10^{−10}
$).

Alguns ajustes podem ser feitos para melhorar a precisão do resultado:

- aumentar o número de iterações, 
- multiplicar o gradiente por um valor escalar menor que 1, chamado de learning rate;
- usar técnicas mais avançadas de gradiente descendente, e.g., gradiente descendente com momento.

Obter esses resultados é um ótimo indicativo de que vocês implementaram corretamente o algoritmo! Parabéns :)