"""
Método Húngaro (Kuhn–Munkres) — implementação didática para o Projeto A2.

Sem uso de scipy.optimize.linear_sum_assignment como solucionador.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from itertools import permutations
from pathlib import Path
from typing import Iterable

EPS = 1e-9


@dataclass
class PassoHungaro:
    titulo: str
    matriz: list[list[float]]
    detalhe: str = ""


@dataclass
class ResultadoHungaro:
    atribuicao: list[tuple[int, int]]  # (i, j) consultor i -> bloco j
    custo_total: float
    passos: list[PassoHungaro] = field(default_factory=list)


def _copia(mat: list[list[float]]) -> list[list[float]]:
    return [linha[:] for linha in mat]


def reduzir_linhas(mat: list[list[float]]) -> list[list[float]]:
    out = _copia(mat)
    for i, linha in enumerate(out):
        m = min(linha)
        out[i] = [v - m for v in linha]
    return out


def reduzir_colunas(mat: list[list[float]]) -> list[list[float]]:
    out = _copia(mat)
    n = len(out)
    if n == 0:
        return out
    m = len(out[0])
    for j in range(m):
        col_min = min(out[i][j] for i in range(n))
        for i in range(n):
            out[i][j] -= col_min
    return out


def _zeros(mat: list[list[float]]) -> list[tuple[int, int]]:
    return [(i, j) for i, row in enumerate(mat) for j, v in enumerate(row) if abs(v) < EPS]


def _matching_maximo_em_zeros(
    mat: list[list[float]], n: int
) -> list[tuple[int, int]]:
    """Matching máximo em arestas (i,j) com mat[i][j] ≈ 0 — DFS para n pequeno."""
    zero_adj: list[list[int]] = [[] for _ in range(n)]
    for i, j in _zeros(mat):
        zero_adj[i].append(j)

    match_col = [-1] * n
    match_row = [-1] * n

    def dfs(i: int, seen: list[bool]) -> bool:
        for j in zero_adj[i]:
            if seen[j]:
                continue
            seen[j] = True
            if match_col[j] == -1 or dfs(match_col[j], seen):
                match_col[j] = i
                match_row[i] = j
                return True
        return False

    for i in range(n):
        dfs(i, [False] * n)

    return [(i, match_row[i]) for i in range(n) if match_row[i] != -1]


def _cobertura_minima_linhas(
    mat: list[list[float]], matching: list[tuple[int, int]], n: int
) -> tuple[list[bool], list[bool]]:
    """
    Cobertura mínima de linhas/colunas que cobre todos os zeros (teorema de König).
    Linhas não cobertas pelo matching alternado + colunas cobertas.
    """
    matched_rows = {i for i, _ in matching}
    matched_cols = {j for _, j in matching}

    # Linhas alternantes a partir de linhas não matched
    alt_rows = set()
    stack = [i for i in range(n) if i not in matched_rows]
    alt_rows.update(stack)
    alt_cols: set[int] = set()

    while stack:
        i = stack.pop()
        for j in range(n):
            if abs(mat[i][j]) >= EPS or j in alt_cols:
                continue
            if j not in matched_cols:
                alt_cols.add(j)
                continue
            i2 = next(ii for ii, jj in matching if jj == j)
            if i2 not in alt_rows:
                alt_rows.add(i2)
                stack.append(i2)

    cover_row = [i not in alt_rows for i in range(n)]
    cover_col = [j in alt_cols for j in range(n)]
    return cover_row, cover_col


def hungarian(
    custo: list[list[float]], registrar_passos: bool = True
) -> ResultadoHungaro:
    n = len(custo)
    if n == 0 or any(len(r) != n for r in custo):
        raise ValueError("Matriz deve ser quadrada e não vazia")

    passos: list[PassoHungaro] = []
    mat = _copia(custo)

    if registrar_passos:
        passos.append(PassoHungaro("Matriz original", _copia(mat)))

    mat = reduzir_linhas(mat)
    if registrar_passos:
        passos.append(
            PassoHungaro(
                "Após redução de linhas (subtrair mínimo de cada linha)",
                _copia(mat),
            )
        )

    mat = reduzir_colunas(mat)
    if registrar_passos:
        passos.append(
            PassoHungaro(
                "Após redução de colunas (subtrair mínimo de cada coluna)",
                _copia(mat),
            )
        )

    iteracao = 0
    while True:
        iteracao += 1
        matching = _matching_maximo_em_zeros(mat, n)
        if len(matching) == n:
            if registrar_passos:
                passos.append(
                    PassoHungaro(
                        f"Solução com {n} zeros independentes (iteração {iteracao})",
                        _copia(mat),
                        detalhe=f"Matching: {matching}",
                    )
                )
            atrib = sorted(matching, key=lambda t: t[0])
            custo_total = sum(custo[i][j] for i, j in atrib)
            return ResultadoHungaro(atrib, custo_total, passos)

        cover_row, cover_col = _cobertura_minima_linhas(mat, matching, n)
        num_linhas = sum(cover_row) + sum(cover_col)

        if registrar_passos:
            passos.append(
                PassoHungaro(
                    f"Iteração {iteracao}: cobertura com {num_linhas} linhas",
                    _copia(mat),
                    detalhe=f"Matching parcial ({len(matching)} pares): {matching}",
                )
            )

        min_uncovered = None
        for i in range(n):
            if cover_row[i]:
                continue
            for j in range(n):
                if cover_col[j]:
                    continue
                v = mat[i][j]
                if min_uncovered is None or v < min_uncovered:
                    min_uncovered = v

        if min_uncovered is None or min_uncovered < EPS:
            raise RuntimeError("Falha na atualização da matriz (valor mínimo inválido)")

        for i in range(n):
            for j in range(n):
                if not cover_row[i] and not cover_col[j]:
                    mat[i][j] -= min_uncovered
                elif cover_row[i] and cover_col[j]:
                    mat[i][j] += min_uncovered

        if registrar_passos:
            passos.append(
                PassoHungaro(
                    f"Iteração {iteracao}: ajuste com h = {min_uncovered:.4f}",
                    _copia(mat),
                )
            )


def forca_bruta(custo: list[list[float]]) -> tuple[list[tuple[int, int]], float]:
    n = len(custo)
    melhor: list[tuple[int, int]] = []
    melhor_z = float("inf")
    for perm in permutations(range(n)):
        z = sum(custo[i][perm[i]] for i in range(n))
        if z < melhor_z:
            melhor_z = z
            melhor = [(i, perm[i]) for i in range(n)]
    return melhor, melhor_z


def custo_alocacao(custo: list[list[float]], pares: Iterable[tuple[int, int]]) -> float:
    return sum(custo[i][j] for i, j in pares)


def carregar_matriz_csv(caminho: Path) -> tuple[list[str], list[str], list[list[float]]]:
    linhas_raw: list[list[str]] = []
    with caminho.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or row[0].startswith("#"):
                continue
            linhas_raw.append(row)

    row_labels = [r[0] for r in linhas_raw[1:]]
    col_labels = linhas_raw[0][1:]
    mat = [[float(x) for x in r[1:]] for r in linhas_raw[1:]]
    return row_labels, col_labels, mat


def carregar_metadados(caminho: Path) -> dict:
    with caminho.open(encoding="utf-8") as f:
        return json.load(f)


def baseline_diagonal(n: int) -> list[tuple[int, int]]:
    return [(i, i) for i in range(n)]


def baseline_rotacao(n: int, deslocamento: int = 1) -> list[tuple[int, int]]:
    """Alocação ingênua: consultor i -> bloco (i + deslocamento) mod n."""
    return [(i, (i + deslocamento) % n) for i in range(n)]
