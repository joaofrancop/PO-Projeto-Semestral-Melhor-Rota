# Modelagem Formal — Problema do Caixeiro Viajante (TSP)

## 1. Conjuntos e Índices
*   $V = \{0\} \cup C$: Conjunto de todos os vértices (nós) do grafo do dia.
    *   $0$: Depósito fixo (Hotel / Base de partida e chegada).
    *   $C = \{1, 2, \dots, X\}$: Conjunto de clientes selecionados para a visita, onde $|C| = X$.
*   $S \subset V$: Subconjunto qualquer de vértices (utilizado para a restrição de eliminação de subciclos).

## 2. Parâmetros
*   $d_{ij} \geq 0$: Distância euclidiana entre os pontos $i$ e $j$ ($\forall i, j \in V, i \neq j$), calculada a partir das coordenadas $(x, y)$ fornecidas no dataset Solomon C102. Como a matriz é simétrica, $d_{ij} = d_{ji}$.

## 3. Variáveis de Decisão
$$
x_{ij} \in \{0, 1\}, \quad \forall i, j \in V, \; i \neq j
$$
*   $x_{ij} = 1$ se o deslocamento direto do nó $i$ para o nó $j$ faz parte da rota ótima.
*   $x_{ij} = 0$ caso contrário.

## 4. Função Objetivo
Minimizar a distância total percorrida na rota fechada:
$$
\text{Minimizar } Z = \sum_{i \in V} \sum_{j \in V, j \neq i} d_{ij} x_{ij}
$$

## 5. Restrições

**R1. Grau de saída (cada nó deve ter exatamente uma partida):**
$$
\sum_{j \in V, j \neq i} x_{ij} = 1, \quad \forall i \in V
$$

**R2. Grau de entrada (cada nó deve ter exatamente uma chegada):**
$$
\sum_{i \in V, i \neq j} x_{ij} = 1, \quad \forall j \in V
$$

**R3. Eliminação de Subciclos (Formulação MTZ - Miller-Tucker-Zemlin):**
Para garantir que a solução forme um único ciclo contínuo passando pelo depósito (e não múltiplos ciclos desconectados), introduzimos variáveis contínuas auxiliares $u_i$ (representando a posição de visita do nó $i$ na rota):
$$
u_i - u_j + X \cdot x_{ij} \leq X - 1, \quad \forall i, j \in C, \; i \neq j
$$
$$
1 \leq u_i \leq X, \quad \forall i \in C
$$
*(Nota: Embora a modelagem exata exija MTZ ou Dantzig-Fulkerson-Johnson para evitar subciclos, nossa implementação heurística constrói diretamente uma permutação válida de $C$, garantindo estruturalmente um tour único sem a necessidade de resolver o modelo linear inteiro completo).*

## 6. Resolução Adotada (Abordagem Heurística)
Dado que o TSP é um problema NP-Difícil, a resolução exata torna-se inviável computacionalmente à medida que $X$ cresce. Portanto, adotamos a abordagem exigida pela Trilha 5:
1.  **Heurística Construtiva (Vizinho Mais Próximo):** Gera uma solução inicial viável $\pi$ partindo do depósito $0$.
2.  **Busca Local (2-Opt):** Melhora a permutação $\pi$ iterativamente, revertendo segmentos da rota para eliminar cruzamentos geométricos até que nenhuma melhoria seja possível (ótimo local).
O custo é avaliado na rota fechada: $0 \rightarrow \pi_1 \rightarrow \pi_2 \rightarrow \dots \rightarrow \pi_X \rightarrow 0$.