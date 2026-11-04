"""
Executa o roteiro: deposito + clientes selecionados, compara ordens e gera figura.
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt

from dados_io import carregar_paradas, deposito, paradas_por_ids
from roteiro_tsp import matriz_distancias, resolver_rota

BASE = Path(__file__).resolve().parent
SAIDA = BASE / "saida"
SAIDA.mkdir(exist_ok=True)

# Clientes escolhidos para o dia (ids do C102). Ajuste X aqui.
CLIENTES_SELECIONADOS = list(range(1, 16))


def plotar_rota(
    pontos: list,
    ordem_local: list[int],
    titulo: str,
    arquivo: Path,
) -> None:
    dep = pontos[0]
    xs = [dep.x]
    ys = [dep.y]
    for idx in ordem_local:
        xs.append(pontos[idx].x)
        ys.append(pontos[idx].y)
    xs.append(dep.x)
    ys.append(dep.y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(xs, ys, "-o", color="#334155", markersize=5, linewidth=1.2)
    ax.scatter([dep.x], [dep.y], s=120, c="#2563EB", zorder=5, label="Deposito (hotel)")
    for idx in ordem_local:
        p = pontos[idx]
        ax.annotate(str(p.cust_no), (p.x, p.y), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_title(titulo)
    ax.set_xlabel("x (Solomon)")
    ax.set_ylabel("y (Solomon)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(arquivo, dpi=150)
    plt.close(fig)


def main() -> None:
    todas = carregar_paradas()
    dep = deposito(todas)
    visitas = paradas_por_ids(todas, CLIENTES_SELECIONADOS)
    pontos = [dep] + visitas
    n = len(visitas)

    dist = matriz_distancias(pontos)
    ingenua, otima, c_ini, c_nn, c_fim = resolver_rota(dist, n)

    ids_otima = [pontos[i].cust_no for i in otima]
    sequencia = [0] + ids_otima + [0]

    linhas = [
        "Relatorio de roteiro (TSP heuristico)",
        f"Clientes selecionados: {len(CLIENTES_SELECIONADOS)} (ids {CLIENTES_SELECIONADOS[0]}..{CLIENTES_SELECIONADOS[-1]})",
        f"Deposito: cust_no={dep.cust_no} em ({dep.x}, {dep.y})",
        "",
        f"Ordem ingenua (1,2,...,n): custo {c_ini:.2f}",
        f"Apos vizinho mais proximo: custo {c_nn:.2f}",
        f"Apos 2-Opt: custo {c_fim:.2f}",
        f"Reducao em relacao a ordem ingenua: {(1 - c_fim / c_ini) * 100:.1f}%",
        "",
        "Sequencia de cust_no (deposito incluido no inicio e fim):",
        " -> ".join(str(x) for x in sequencia),
    ]
    texto = "\n".join(linhas)
    (SAIDA / "relatorio_roteiro.txt").write_text(texto, encoding="utf-8")

    plotar_rota(
        pontos,
        ingenua,
        "Rota na ordem ingenua",
        SAIDA / "rota_ingenua.png",
    )
    plotar_rota(
        pontos,
        otima,
        "Rota apos vizinho mais proximo e 2-Opt",
        SAIDA / "rota_otimizada.png",
    )

    print(texto)
    print(f"\nArquivos em: {SAIDA}")


if __name__ == "__main__":
    main()
