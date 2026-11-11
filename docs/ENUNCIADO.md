# Enunciado do projeto

## Problema

Uma equipe comercial define, para um dia de viagem, um conjunto de X clientes que precisam ser visitados. A partida e o retorno ocorrem no mesmo ponto de apoio (hotel ou aeroporto). Deseja-se determinar a ordem de visita que minimiza a distância total percorrida, visitando cada cliente selecionado exatamente uma vez.

Na literatura de Pesquisa Operacional, trata-se de um caso do Problema do Caixeiro Viajante (PCV) com rota fechada e depósito fixo. O conjunto de decisão é a permutação das visitas. A função objetivo é a soma das distâncias entre consecutivos da rota, incluindo os trechos do depósito até o primeiro cliente e do último cliente até o depósito.

## Dados

Utiliza-se a instância Solomon C102, disponível em `dados/solomon/C102_paradas.csv`. O registro com `cust_no` igual a zero representa o depósito (hotel). Os demais registros formam o conjunto de clientes elegíveis. O grupo escolhe X identificadores e o programa considera somente esses clientes na otimização.

As coordenadas `x` e `y` permitem calcular distâncias euclidianas. No benchmark original existem também janelas de tempo (`ready_time`, `due_date`) e tempo de serviço; a primeira versão do projeto concentra-se na minimização da distância de deslocamento. A verificação de janelas pode ser tratada como extensão.

Dataset obtido no [Kaggle — Solomon benchmark](https://www.kaggle.com/datasets/jaikeerthy/solomon-benchmark). A base foi escolhida por oferecer identificadores e coordenadas estruturadas para calcular distâncias e comparar ordens de visita. O benchmark original de roteamento com frota e janelas é adaptado para uma única rota comercial. Demanda e capacidade também ficam fora do escopo atual.

A demonstração usa **15 clientes, IDs 1 a 15**, definidos em `CLIENTES_SELECIONADOS` no script principal. O recorte favorece a visualização. Os valores de distância estão em unidades do benchmark, sem conversão para quilômetros, tempo ou custos financeiros.

## Método

Conforme a trilha 5 do kickoff da disciplina:

1. Construção da matriz de distâncias entre depósito e clientes selecionados.
2. Geração de uma solução inicial por vizinho mais próximo, partindo do depósito.
3. Melhoria local por intercâmbio 2-Opt até não encontrar redução do custo ou atingir 500 iterações, sem garantia de ótimo global.
4. Comparação com uma ordem ingênua (ordem de entrada dos clientes, crescente por ID na demonstração) para avaliar ganho.

A implementação está em `roteiro_tsp.py` e a execução de exemplo em `executar_roteiro.py`.

## Execução

```powershell
pip install -r requirements.txt
python executar_roteiro.py
```

Os resultados numéricos e os gráficos são gravados na pasta `saida/`.
