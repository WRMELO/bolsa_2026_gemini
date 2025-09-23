# 

## 1. Fundamentos

- **Objetivo**: prever tendências de curto prazo (D+1, D+3, D+5) para guiar decisões de alocação.  
- **Meta de negócio**: retorno líquido ≥ 8% a.a.  
- **Piso único crescente**: trajetória pró-rata de 8% a.a., sempre preservada.  
- **Viés conservador**: preservação de capital acima de ganho.  
  - Venda = compulsória (alta sensibilidade a ↓).  
  - Compra = opcional (alta precisão exigida para ↑).  

---

## 2. Dados e Camadas

### Bronze
- Ingestão de 8–12 anos de dados.  
- Padronização: timezone único, nomes consistentes, dtypes coerentes.  
- Validação: relatórios de sanidade + manifesto de ingestão.  

### Silver
- Calendário de pregões unificado.  
- Features “sem opinião”: retornos, janelas, volatilidades, regimes.  
- Manifesto Silver com coerência temporal.  

### Gold
- Rotulagem 3-classes (↓, 0, ↑):  
  - D+1: 45–55% neutros  
  - D+3: 38–45% neutros  
  - D+5: 30–38% neutros  
- Neutralidade só na rotulagem.  
- Walk-forward purged/embargoed.  
- Gold particionado em Parquet + manifesto de distribuição.  

### Expansão
- Após validação com IBOV, estender para **24 tickers balanceados** com regras de elegibilidade (ADTV≥p70 IBOV, histórico≥5 anos, 1 papel por emissor/classe).  
- Reservas setoriais documentadas.  
- Revisão trimestral, sem churn intra-trimestre.

---

## 3. Modelagem

- **Modelos-base**: XGBoost, CatBoost, LogReg multinomial (sanity check).  
- Avaliação: MCC macro, acurácia balanceada, F1↑ e F1↓, Brier/NLL.  
- Calibração: Platt ou Isotônica.  
- Congelamento de thresholds por janela; monitor de drift.

---

## 4. Política de Decisão

- **Circuito de proteção (sell-side compulsório)**  
  - Agregador de p(↓) multi-horizonte, com histerese mínima.  
  - Venda se p(↓) ≥ θ↓ ou E[retorno] pós-custos < 0.  

- **Circuito de captura (buy-side opcional)**  
  - Requer concordância entre D+1 e D+3.  
  - Hurdle pró-rata: 0,03% D+1; 0,09% D+3; 0,15% D+5.  
  - Bloqueio se p(↓|D+5) alto.  

- **Neutro** sempre que critérios acima não forem satisfeitos.  

---

## 5. Overlay de Risco

- **CPPI leve** com piso crescente.  
- Almofada = max(Vt − Ft, 0).  
- Exposição = m × Almofada (m = 2–4).  
- Se Vt→Ft, exposição→0.  
- Sizing ∝ Cushion / σh, com stops estatísticos.  
- **Kill switch**: caixa forçada se probabilidade de violar piso > 1%.  
- Overlay tem precedência absoluta.  

---

## 6. Critérios de Aceitação

### Técnicos
- MCC macro > 0 em todos os blocos.  
- Acurácia balanceada > baseline trivial.  
- F1↑ e F1↓ positivos.  
- Distribuição de classes dentro das metas.  

### De Negócio
- Piso nunca violado.  
- Retorno líquido ≥ 8% a.a.  
- Drawdown controlado.  
- Custos/turnover ≤ limites definidos.  

---

## 7. Governança e Papéis

- **Owner**: define objetivos, aprova marcos.  
- **Estrategista**: instrui, valida outputs, mantém SSOT.  
- **Agente**: entrega código auto-contido, 1ª execução sempre `dry_run=True`.  

### Escalonamento
- Erro repetido 2x → Agente para e devolve dúvidas objetivas.  
- Estrategista corrige instrução.  

---

## 8. Entregáveis

- Manifestos (CSV/MD).  
- Logs de qualidade.  
- Hashes de artefatos.  
- Relatórios de métricas.  
- Gold versionado + modelos calibrados + thresholds congelados.  

---

## 9. Próximos Passos

1. **F0 (Setup & SSOT)**: convenções, diretórios, manifestos.  
2. **F1 (Bronze)**: ingestão + manifesto de sanidade.  
3. **F2 (Silver)**: calendário unificado, features básicas.  
4. **F3 (Gold)**: rotulagem, walk-forward, manifesto.  
5. **F4+**: modelagem, calibração, decisão, overlay, backtest.  
