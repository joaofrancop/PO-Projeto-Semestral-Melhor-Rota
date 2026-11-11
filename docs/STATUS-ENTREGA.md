# Status da entrega (Checkpoint 12/11 e Final 24/11)

## ✅ Pronto no repositório
- [x] Enunciado e modelagem em `docs/`
- [x] Dados Solomon C102 convertidos para CSV e documentados, com referência ao Kaggle
- [x] Leitura do CSV e seleção de clientes configurável no código
- [x] Heurística TSP: vizinho mais próximo + 2-Opt (rota fechada)
- [x] Script `executar_roteiro.py` validado (redução de ~21% vs ordem ingênua)
- [x] Saídas em `saida/relatorio_roteiro.txt` e gráficos PNG

## 🚧 Em Andamento (Foco: Checkpoint 12/11)
- [x] Documentação alinhada ao escopo de distância, sem horários ou capacidade
- [x] Modelagem distingue modelo exato e resolução heurística, sem garantia de ótimo global
- [x] Recorte padrão definido: 15 clientes, IDs 1 a 15, além do depósito 0
- [x] Revisar em grupo a explicação e preencher a autoavaliação da ficha
- [x] Confirmar inscrição dos 3 integrantes no grupo do Blackboard

## 📅 Próximos Passos (Foco: Entrega Final 24/11)
- [x] Substituir conteúdo antigo do notebook pelo fluxo TSP com Solomon e instruções para Colab
- [x] Executar todas as células do notebook no Python local, incluindo geração de gráficos e chamada do script
- [ ] Conferir execução no Colab após enviar o projeto e ajustar o caminho
- [ ] Gravar o vídeo de defesa (10 a 15 minutos) dividindo as falas entre os integrantes
- [ ] Garantir que o gráfico comparativo (Rota Ingênua vs Rota 2-Opt) esteja bem legível

## Validação local dos ajustes

- CSV: 101 registros, IDs únicos de 0 a 100 e coordenadas numéricas finitas; depósito em (40, 50).
- Notebook: células de código com sintaxe válida e execução sequencial concluída. Cada rota contém todos os clientes selecionados uma única vez; o 2-Opt não aumenta o custo da rota inicial.
- Script principal: relatório e gráficos gerados; custos 131,73 (ordem de entrada), 118,54 (vizinho mais próximo) e 103,29 (2-Opt), redução de 21,6% sobre a ordem de entrada.
- Essa validação não comprova ótimo global, horários viáveis ou desempenho no Colab. Inscrição no Blackboard e revisão da ficha dependem do grupo.
