# Projeto semestral: melhor rota de visitas (PO I)

Otimização da ordem de visitas a clientes selecionados, com partida e retorno no depósito (hotel), usando a instância Solomon C102 e heurísticas de TSP (vizinho mais próximo e 2-Opt).

Repositório: https://github.com/joaofrancop/PO-Projeto-Semestral-Melhor-Rota

## Estrutura

- `docs/ENUNCIADO.md`: problema e método em linguagem da disciplina
- `docs/MODELAGEM-FORMAL.md`: formulacao para o checkpoint
- `dados/solomon/C102_paradas.csv`: dados
- `dados_io.py`, `roteiro_tsp.py`: leitura e algoritmo
- `executar_roteiro.py`: exemplo executável (lista de clientes em `CLIENTES_SELECIONADOS`)

## Como rodar

```powershell
pip install -r requirements.txt
python executar_roteiro.py
```

Saída em `saida/relatorio_roteiro.txt` e figuras `rota_ingenua.png`, `rota_otimizada.png`.

Para alterar quantos clientes entram no dia, edite a lista `CLIENTES_SELECIONADOS` em `executar_roteiro.py`.
