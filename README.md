# Projeto Semestral de Pesquisa Operacional: Otimização de Rota de Visitas (TSP)

**Equipe:** Guilherme Caleffi, João Franco e Marcio Henrique <br>
**Tema:** Caixeiro Viajante (TSP) e Roteamento (Heurísticas Construtivas e 2-Opt)

## Resumo do Projeto
Este projeto implementa um motor de otimização em Python (sem uso de bibliotecas de "caixa-preta" para a lógica central) para resolver o Problema do Caixeiro Viajante (TSP) com retorno ao depósito. 

O cenário simula uma equipe comercial em viagem externa que deve sair de uma base (hotel), visitar um conjunto selecionado de $X$ clientes e retornar à base, minimizando a distância total percorrida.

## Dataset
Utilizamos a instância pública clássica **Solomon C102** (100 clientes + 1 depósito).
* Para manter a didática e a clareza visual, o algoritmo permite selecionar um subconjunto de $X$ clientes (ex: 15 clientes) para calcular e exibir a rota ótima.
* Os dados originais e processados estão disponíveis em [`dados/solomon/`](dados/solomon/).

## Algoritmos Implementados (Do Zero)
1. **Vizinho Mais Próximo (Nearest Neighbor):** Heurística construtiva gulosa para gerar uma rota inicial viável rapidamente.
2. **Melhoria Local 2-Opt:** Algoritmo de busca local que elimina cruzamentos de arestas (subciclos ineficientes) invertendo segmentos da rota até atingir um ótimo local.

## Estrutura do Repositório
* `docs/`: Documentação completa (Cenário, Modelagem Formal, Guia do Dataset, Roteiro do Vídeo).
* `dados/`: Bases de dados (Solomon C102).
* `roteiro_tsp.py`: Implementação pura das heurísticas TSP e 2-Opt.
* `dados_io.py` / `solomon_io.py`: Módulos de leitura e processamento dos dados.
* `executar_roteiro.py`: Script principal de execução e geração de gráficos.
* `A2_Roteiro_Solomon.ipynb`: Notebook interativo para demonstração.
* `saida/`: Diretório onde os gráficos (PNG) e relatórios gerados são salvos.

## Como Executar
```bash
pip install -r requirements.txt
python executar_roteiro.py
```
