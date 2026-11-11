# Projeto Semestral de Pesquisa Operacional: Otimização de Rota de Visitas (TSP)

**Equipe:** Guilherme Caleffi, João Franco e Marcio Henrique <br>
**Tema:** Caixeiro Viajante (TSP) e Roteamento (Heurísticas Construtivas e 2-Opt)

## Resumo do Projeto
Este projeto implementa um motor de otimização em Python (sem uso de bibliotecas de "caixa-preta" para a lógica central) para resolver o Problema do Caixeiro Viajante (TSP) com retorno ao depósito. 

O cenário simula uma equipe comercial em viagem externa que deve sair de uma base (hotel), visitar um conjunto selecionado de $X$ clientes e retornar à base, minimizando a distância total percorrida.

## Dataset
Utilizamos a instância pública clássica **Solomon C102** (100 clientes + 1 depósito).
* A demonstração atual usa **15 clientes (IDs 1 a 15)** e o depósito 0, interpretado como hotel. A seleção é configurada em `CLIENTES_SELECIONADOS`, no script principal.
* Dataset obtido no [Kaggle — Solomon benchmark](https://www.kaggle.com/datasets/jaikeerthy/solomon-benchmark). Trata-se de um benchmark adaptado ao cenário comercial.
* Usamos `cust_no`, `x` e `y` para identificar os pontos e calcular distâncias euclidianas em unidades do benchmark. Horários, duração de atendimento, demanda e capacidade não restringem a rota atual.
* Os dados originais e processados estão disponíveis em [`dados/solomon/`](dados/solomon/).

## Algoritmos Implementados (Do Zero)
1. **Vizinho Mais Próximo (Nearest Neighbor):** Heurística construtiva gulosa para gerar uma rota inicial viável rapidamente.
2. **Melhoria Local 2-Opt:** Busca local que inverte segmentos da rota e aceita reduções de distância. Encerra quando não encontra melhoria ou atinge 500 iterações. Cruzamentos geométricos não são subciclos desconectados.

As heurísticas produzem uma rota melhorada, sem garantia de ótimo global. A comparação usa a ordem de entrada dos clientes (crescente por ID no exemplo atual). As distâncias não representam quilômetros ou trajetos por ruas.

## Estrutura do Repositório
* `docs/`: Documentação completa (Cenário, Modelagem Formal, Guia do Dataset, Roteiro do Vídeo).
* `dados/`: Bases de dados (Solomon C102).
* `roteiro_tsp.py`: Implementação pura das heurísticas TSP e 2-Opt.
* `dados_io.py` / `solomon_io.py`: Módulos de leitura e processamento dos dados.
* `executar_roteiro.py`: Script principal de execução e geração de gráficos.
* `A2_Roteiro_Solomon.ipynb`: Notebook para demonstrar o mesmo fluxo TSP, com instruções para execução local ou Colab.
* `saida/`: Diretório onde os gráficos (PNG) e relatórios gerados são salvos.
* `legado/`: Rascunho antigo do Método Húngaro (trilha 2), fora da entrega atual.

## Como Executar
```bash
pip install -r requirements.txt
python executar_roteiro.py
```
