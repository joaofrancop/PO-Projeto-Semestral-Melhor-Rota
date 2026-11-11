# C102 completo — como usar (hotel + 100 clientes)

## O que é cada linha

| Campo | Cliente 0 (depósito) | Clientes 1–100 |
|--------|----------------------|----------------|
| **`cust_no`** | **0 = hotel/base** | Ficha de visita |
| **`x`, `y`** | Posição fixa da base: **(40, 50)** | Posição da parada no mapa Solomon |
| **`demand`** | **0** (não consome carga) | Carga fictícia do benchmark (10–40) |
| **`ready_time`** | **0** | Earliest time — **não antes disso** para **iniciar** a visita |
| **`due_date`** | **1236** (= horizonte do dia) | Latest time para **iniciar** a visita |
| **`service_time`** | **0** | Tempo na parada (**90** na quase totalidade) |

Na interpretação temporal do benchmark, distância e deslocamento podem ser relacionados na mesma escala. **O motor TSP atual usa apenas distância euclidiana** e não calcula horários, duração de rota ou quilômetros reais.

## “Hotel” no projeto

Use **sempre** a linha `cust_no == 0`:

- Rotulo no CSV: `HOTEL_DEPOSITO`
- **Partida** e **retorno** da rota fechada TSP
- **Não** entra como “visita” (service 0, demand 0)
- Coordenadas **(40, 50)** = ponto de referência central no mapa C102 (tipo centro da região metropolitana fictícia)

No código: `depot = df[df.cust_no == 0].iloc[0]`; paradas = `df[df.cust_no > 0]` → **100 visitas**.

## Fluxo do projeto: **selecionar X clientes** → melhor rota

1. **Hotel fixo:** linha `cust_no == 0` (partida e retorno).  
2. **Seleção:** lista com **X** ids (ex. `[3, 7, 12, 15, 20]` ou `range(1, 16)` para 15 clientes).  
3. **Grafo do dia:** hotel + **somente** esses X pontos → matriz **(X+1)×(X+1)**.  
4. **Saída:** ordem otimizada hotel → visitas → hotel (**vizinho mais próximo + 2-Opt**).

O arquivo CSV completo (101 linhas) é o **cadastro**; no dia real / no notebook vocês não precisam usar os 100 — só **X escolhidos**.

**Recorte atual da apresentação:** X = 15, IDs 1 a 15, definidos em `CLIENTES_SELECIONADOS` no arquivo `executar_roteiro.py`. O notebook importa essa configuração. Outros recortes podem ser usados em experimentos.

**O que ignorar no básico (sem sair do que a aula pede):**

| Campo do C102 | Motivo |
|---------------|--------|
| `VEHICLE 25`, `CAPACITY 200` | Benchmark é **vários caminhões**; vocês modelam **1 vendedor / 1 rota** |
| `demand` | Só faz sentido com frota e capacidade |
| `ready_time` / `due_date` | **VRPTW** — fase 2 ou menção no vídeo; ver abaixo |

### Honestidade no vídeo (importante)

- Só **tempo de serviço** já daria 100 × 90 = **9000** unidades, e o horizonte do depósito é **1236**.  
- Ou seja: o C102 **original** não é “100 visitas num único dia realista”; é instância clássica multi-veículo.

Para o projeto ficar **correto e simples**:

- **Entrega núcleo:** dado **X clientes escolhidos**, otimizar a **ordem** (TSP fechado no hotel).  
- **Narrativa:** igual ao trabalho — “puxamos X fichas do sistema / do pool C102 e o motor sugere a rota.”  
- **Opcional:** checar `ready_time`/`due_date` **só nos X** após montar a rota (viola janela?).

## Clientes com janela apertada (exemplos)

Vale citar no checkpoint que nem todo cliente aceita qualquer horário:

- Ex.: `cust_no = 13` → `ready_time = 30`, `due_date = 92` (janela curta para **iniciar**).
- Ex.: `cust_no = 4` → só entre 727 e 782.

Na **só-TSP** esses campos não mudam a ordem; na **história empresa** (“margem de horário”) eles explicam por que no futuro a rota precisa de VRPTW, não só 2-Opt.

## Arquivos

- Fonte: [`../dados/solomon/C102.txt`](../dados/solomon/C102.txt)
- Trabalho: [`../dados/solomon/C102_paradas.csv`](../dados/solomon/C102_paradas.csv) (**101 linhas**)

Dataset obtido no [Kaggle — Solomon benchmark](https://www.kaggle.com/datasets/jaikeerthy/solomon-benchmark). São dados de benchmark adaptados para visitas comerciais. O benchmark original é multi-veículo, mas o projeto usa somente uma rota e não garante ótimo global.

Regenerar CSV: `python solomon_io.py` na raiz do projeto.

## Repo GitHub

[PO-Projeto-Semestral-Melhor-Rota](https://github.com/joaofrancop/PO-Projeto-Semestral-Melhor-Rota)
