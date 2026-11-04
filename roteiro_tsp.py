"""
Heuristica para o problema do caixeiro viajante com deposito (rota fechada).
Vizinho mais proximo + melhoria 2-Opt. Implementacao manual para o A2.
"""

from __future__ import annotations

import math

from dados_io import Parada


def distancia_euclidiana(a: Parada, b: Parada) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def matriz_distancias(pontos: list[Parada]) -> list[list[float]]:
    n = len(pontos)
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                m[i][j] = distancia_euclidiana(pontos[i], pontos[j])
    return m


def custo_rota_fechada(dist: list[list[float]], ordem: list[int]) -> float:
    """ordem: indices locais 1..n-1 (clientes). Indice 0 = deposito."""
    if not ordem:
        return 0.0
    total = dist[0][ordem[0]]
    for i in range(len(ordem) - 1):
        total += dist[ordem[i]][ordem[i + 1]]
    total += dist[ordem[-1]][0]
    return total


def vizinho_mais_proximo(dist: list[list[float]], n_clientes: int) -> list[int]:
    nao_visitados = list(range(1, n_clientes + 1))
    ordem: list[int] = []
    atual = 0
    while nao_visitados:
        proximo = min(nao_visitados, key=lambda j: dist[atual][j])
        ordem.append(proximo)
        nao_visitados.remove(proximo)
        atual = proximo
    return ordem


def otimizar_2opt_fechado(
    dist: list[list[float]], ordem_inicial: list[int], max_iter: int = 500
) -> list[int]:
    n = len(ordem_inicial)
    if n < 2:
        return ordem_inicial
    melhor = ordem_inicial[:]
    melhor_custo = custo_rota_fechada(dist, melhor)
    melhorou = True
    iteracao = 0
    while melhorou and iteracao < max_iter:
        melhorou = False
        iteracao += 1
        for i in range(n - 1):
            for k in range(i + 1, n):
                nova = melhor[:i] + list(reversed(melhor[i : k + 1])) + melhor[k + 1 :]
                c = custo_rota_fechada(dist, nova)
                if c + 1e-9 < melhor_custo:
                    melhor = nova
                    melhor_custo = c
                    melhorou = True
                    break
            if melhorou:
                break
    return melhor


def ordem_ingenua(n_clientes: int) -> list[int]:
    return list(range(1, n_clientes + 1))


def resolver_rota(
    dist: list[list[float]], n_clientes: int
) -> tuple[list[int], list[int], float, float, float]:
    ingenua = ordem_ingenua(n_clientes)
    c_ingenua = custo_rota_fechada(dist, ingenua)
    nn = vizinho_mais_proximo(dist, n_clientes)
    c_nn = custo_rota_fechada(dist, nn)
    otima_heuristica = otimizar_2opt_fechado(dist, nn)
    c_final = custo_rota_fechada(dist, otima_heuristica)
    return ingenua, otima_heuristica, c_ingenua, c_nn, c_final
