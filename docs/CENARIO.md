# Cenário e dataset

## Problema

Viagem externa: sair da **base** (hotel/aeroporto), visitar clientes selecionados e **voltar** à base, minimizando deslocamento/tempo e respeitando **janelas de horário** quando possível.

## Dataset

Instância pública **Solomon C102** (100 clientes + depósito):

- [`../dados/solomon/C102.txt`](../dados/solomon/C102.txt)
- [`../dados/solomon/C102_paradas.csv`](../dados/solomon/C102_paradas.csv)

O C102 traz **100 clientes + 1 hotel** (pool). No projeto: **escolhemos X clientes** desse pool; o algoritmo calcula a **melhor rota** para visitar **todos os X** saindo e voltando ao hotel (`cust_no = 0`). Ver [`DATASET-C102-GUIA.md`](DATASET-C102-GUIA.md).

## Interpretação das colunas

| Campo | Papel no roteiro |
|-------|------------------|
| `cust_no = 0` | Base (hotel) |
| `x`, `y` | Posição no mapa do benchmark |
| `ready_time` / `due_date` | Janela para **iniciar** a visita |
| `service_time` | Tempo na parada |
