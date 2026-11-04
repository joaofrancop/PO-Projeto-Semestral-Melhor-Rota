"""Lê C102.txt (formato Solomon) e exporta CSV para o projeto A2."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOLOMON_DIR = BASE / "dados" / "solomon"
TXT = SOLOMON_DIR / "C102.txt"


@dataclass
class ParadaSolomon:
    cust_no: int
    x: float
    y: float
    demand: int
    ready_time: int
    due_date: int
    service_time: int

    @property
    def rotulo_projeto(self) -> str:
        if self.cust_no == 0:
            return "HOTEL_DEPOSITO"
        return f"VISITA_{self.cust_no:02d}"


def parse_c102(path: Path) -> list[ParadaSolomon]:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("CUST NO."):
            start = i + 2
            break
    if start is None:
        raise ValueError("Cabeçalho CUSTOMER não encontrado")

    out: list[ParadaSolomon] = []
    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 7:
            continue
        out.append(
            ParadaSolomon(
                cust_no=int(parts[0]),
                x=float(parts[1]),
                y=float(parts[2]),
                demand=int(parts[3]),
                ready_time=int(parts[4]),
                due_date=int(parts[5]),
                service_time=int(parts[6]),
            )
        )
    return out


def escrever_csv(paradas: list[ParadaSolomon], destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "cust_no",
                "rotulo",
                "x",
                "y",
                "demand",
                "ready_time",
                "due_date",
                "service_time",
            ]
        )
        for p in paradas:
            w.writerow(
                [
                    p.cust_no,
                    p.rotulo_projeto,
                    p.x,
                    p.y,
                    p.demand,
                    p.ready_time,
                    p.due_date,
                    p.service_time,
                ]
            )


def main() -> None:
    paradas = parse_c102(TXT)
    out = SOLOMON_DIR / "C102_paradas.csv"
    escrever_csv(paradas, out)
    print(f"OK: {len(paradas)} linhas (deposito + {len(paradas)-1} clientes) -> {out.name}")


if __name__ == "__main__":
    main()
