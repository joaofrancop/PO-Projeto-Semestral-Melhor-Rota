# Cenário e dataset

## Problema

Uma equipe comercial precisa sair da **base** (hotel/aeroporto), visitar cada cliente selecionado uma vez e **voltar** à base. O objetivo atual é minimizar a distância euclidiana total. Janelas de horário, duração de atendimento, demanda e capacidade ficam fora das restrições desta versão.

## Dataset

Instância pública **Solomon C102** (100 clientes + depósito), referenciada em [Kaggle — Solomon benchmark](https://www.kaggle.com/datasets/jaikeerthy/solomon-benchmark):

- [`../dados/solomon/C102.txt`](../dados/solomon/C102.txt)
- [`../dados/solomon/C102_paradas.csv`](../dados/solomon/C102_paradas.csv)

O C102 original traz **100 clientes e 1 depósito**. Interpretamos o depósito como hotel; o benchmark é adaptado ao cenário comercial. A demonstração atual seleciona **15 clientes (IDs 1 a 15)**, além do depósito (`cust_no = 0`), e melhora sua ordem de visita com vizinho mais próximo e 2-Opt, sem garantia de ótimo global.

Escolhemos a base por fornecer identificadores e coordenadas estruturadas, suficientes para calcular distâncias e comparar rotas de forma reproduzível. O recorte de 15 clientes facilita a explicação e a leitura do gráfico. As distâncias estão em unidades do benchmark, não em quilômetros ou percursos por ruas. Ver [`DATASET-C102-GUIA.md`](DATASET-C102-GUIA.md).

## Interpretação das colunas

| Campo | Papel no roteiro |
|-------|------------------|
| `cust_no = 0` | Base (hotel) |
| `x`, `y` | Posição no mapa do benchmark |
| `ready_time` / `due_date` | Janela para **iniciar** a visita |
| `service_time` | Tempo na parada |

Na otimização atual usamos `cust_no`, `x` e `y`. Os campos de horário e serviço são preservados na leitura, mas não influenciam o custo nem a viabilidade da rota. O CSV também preserva `demand`, que não é usado pelo motor TSP.
