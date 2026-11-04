"""
Executa o pipeline completo: Húngaro, validação, gráficos e relatório textual.
Uso: python run_projeto.py
"""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from hungarian import (
    baseline_rotacao,
    carregar_matriz_csv,
    carregar_metadados,
    custo_alocacao,
    forca_bruta,
    hungarian,
)

BASE = Path(__file__).resolve().parent
DADOS = BASE / "dados"
SAIDA = BASE / "saida"
SAIDA.mkdir(exist_ok=True)


def plot_heatmap(
    mat: list[list[float]],
    row_labels: list[str],
    col_labels: list[str],
    titulo: str,
    destino: Path,
    highlight: list[tuple[int, int]] | None = None,
) -> None:
    arr = np.array(mat)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        arr,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd",
        xticklabels=col_labels,
        yticklabels=row_labels,
        ax=ax,
        cbar_kws={"label": "Custo (h)"},
    )
    if highlight:
        for i, j in highlight:
            ax.add_patch(
                plt.Rectangle((j, i), 1, 1, fill=False, edgecolor="#2563EB", lw=3)
            )
    ax.set_title(titulo)
    ax.set_xlabel("Blocos regionais")
    ax.set_ylabel("Consultores")
    fig.tight_layout()
    fig.savefig(destino, dpi=150)
    plt.close(fig)


def plot_bipartido(
    row_labels: list[str],
    col_labels: list[str],
    pares: list[tuple[int, int]],
    destino: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    n = len(row_labels)
    y_left = np.linspace(1, 0, n)
    y_right = np.linspace(1, 0, n)
    for i, lab in enumerate(row_labels):
        ax.plot(0, y_left[i], "o", color="#2563EB", ms=12)
        ax.text(-0.05, y_left[i], lab, ha="right", va="center", fontsize=10)
    for j, lab in enumerate(col_labels):
        ax.plot(1, y_right[j], "o", color="#059669", ms=12)
        ax.text(1.05, y_right[j], lab, ha="left", va="center", fontsize=10)
    for i, j in pares:
        ax.plot([0, 1], [y_left[i], y_right[j]], "-", color="#64748B", lw=2)
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-0.1, 1.1)
    ax.axis("off")
    ax.set_title("Designação ótima (grafo bipartido)")
    fig.tight_layout()
    fig.savefig(destino, dpi=150)
    plt.close(fig)


def main() -> None:
    meta = carregar_metadados(DADOS / "consultores_blocos.json")
    row_labels, col_labels, custo = carregar_matriz_csv(DADOS / "matriz_custos_designacao.csv")

    res = hungarian(custo)
    fb_pares, fb_custo = forca_bruta(custo)
    base_pares = baseline_rotacao(len(custo), deslocamento=1)
    base_custo = custo_alocacao(custo, base_pares)

    assert abs(res.custo_total - fb_custo) < 1e-6, "Húngaro diverge da força bruta"

    plot_heatmap(
        custo,
        row_labels,
        col_labels,
        "Matriz de custos — viagem externa (Mastercorp)",
        SAIDA / "heatmap_original.png",
    )
    plot_heatmap(
        res.passos[2].matriz,
        row_labels,
        col_labels,
        "Matriz após reduções iniciais (Húngaro)",
        SAIDA / "heatmap_reduzida.png",
    )
    plot_heatmap(
        custo,
        row_labels,
        col_labels,
        "Alocação ótima destacada",
        SAIDA / "heatmap_solucao.png",
        highlight=res.atribuicao,
    )
    plot_bipartido(row_labels, col_labels, res.atribuicao, SAIDA / "grafo_bipartido.png")

    economia = (base_custo - res.custo_total) / base_custo * 100

    linhas = [
        "# Relatório de execução — Projeto A2",
        "",
        f"**Cenário:** {meta['meta']['empresa_narrativa']}",
        "",
        "## Alocação ótima (Método Húngaro)",
        "",
        "| Consultor | Bloco | Custo (h) |",
        "|-----------|-------|-----------|",
    ]
    for i, j in res.atribuicao:
        linhas.append(f"| {row_labels[i]} | {col_labels[j]} | {custo[i][j]:.2f} |")
    linhas.extend(
        [
            "",
            f"- **Custo total ótimo:** {res.custo_total:.2f} h",
            f"- **Baseline (rotação ingênua C_i→R_{{i+1}}):** {base_custo:.2f} h",
            f"- **Economia vs baseline:** {economia:.1f}%",
            f"- **Validação força bruta:** {fb_custo:.2f} h (OK)",
            "",
            "## Passos registrados",
            "",
        ]
    )
    for k, p in enumerate(res.passos, 1):
        linhas.append(f"{k}. **{p.titulo}** — {p.detalhe}")

    (SAIDA / "relatorio.md").write_text("\n".join(linhas), encoding="utf-8")
    print(f"Custo ótimo: {res.custo_total:.2f} h | Economia: {economia:.1f}%")
    print(f"Gráficos e relatório em: {SAIDA}")


if __name__ == "__main__":
    main()
