"""Leitura das paradas Solomon a partir do CSV do projeto."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

BASE = Path(__file__).resolve().parent
CSV_PADRAO = BASE / "dados" / "solomon" / "C102_paradas.csv"


@dataclass(frozen=True)
class Parada:
    cust_no: int
    x: float
    y: float
    ready_time: int
    due_date: int
    service_time: int

    @property
    def eh_deposito(self) -> bool:
        return self.cust_no == 0


def carregar_paradas(caminho: Path = CSV_PADRAO) -> list[Parada]:
    with caminho.open(encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        out: list[Parada] = []
        for row in leitor:
            out.append(
                Parada(
                    cust_no=int(row["cust_no"]),
                    x=float(row["x"]),
                    y=float(row["y"]),
                    ready_time=int(row["ready_time"]),
                    due_date=int(row["due_date"]),
                    service_time=int(row["service_time"]),
                )
            )
    return out


def deposito(paradas: list[Parada]) -> Parada:
    for p in paradas:
        if p.eh_deposito:
            return p
    raise ValueError("Deposito (cust_no=0) nao encontrado")


def paradas_por_ids(paradas: list[Parada], ids_clientes: list[int]) -> list[Parada]:
    indice = {p.cust_no: p for p in paradas}
    if 0 in ids_clientes:
        raise ValueError("Nao inclua o deposito na lista de clientes selecionados")
    faltando = [i for i in ids_clientes if i not in indice]
    if faltando:
        raise ValueError(f"Ids inexistentes no dataset: {faltando}")
    return [indice[i] for i in ids_clientes]
