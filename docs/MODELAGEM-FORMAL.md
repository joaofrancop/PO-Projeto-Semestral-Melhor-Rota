# Modelagem formal

## Conjuntos

- \(V = \{0\} \cup C\): vértices do grafo do dia, em que \(0\) é o depósito (hotel) e \(C\) é o conjunto de clientes selecionados, com \(|C| = X\).

## Parâmetros

- \(d_{ij} \geq 0\): distância euclidiana entre os pontos \(i\) e \(j\), calculada a partir das coordenadas do CSV.

## Variáveis de decisão

\[
x_{ij} \in \{0, 1\}, \quad i, j \in V, \; i \neq j
\]

\(x_{ij} = 1\) se o deslocamento direto de \(i\) para \(j\) faz parte da rota.

## Função objetivo

\[
\min \sum_{i \in V} \sum_{j \in V, j \neq i} d_{ij}\, x_{ij}
\]

## Restrições

Cada cliente em \(C\) possui grau de entrada e saída igual a 1:

\[
\sum_{j \in V, j \neq i} x_{ji} = 1, \quad \sum_{j \in V, j \neq i} x_{ij} = 1 \quad \forall i \in C
\]

O depósito possui grau 2 (saída na ida e entrada no retorno):

\[
\sum_{j \in C} x_{0j} = 1, \quad \sum_{i \in C} x_{i0} = 1
\]

Eliminação de subciclos que não passam pelo depósito (formulacao completa do PCV; na implementação heuristica garante-se um unico tour).

## Resolução adotada no codigo

Heuristica construtiva (vizinho mais proximo) seguida de melhoria 2-Opt sobre a permutação dos clientes, com custo avaliado na rota fechada \(0 \rightarrow \pi_1 \rightarrow \cdots \rightarrow \pi_X \rightarrow 0\).
