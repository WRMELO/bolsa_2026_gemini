# Plano Mestre v2 — Identificação de Tendências (D+1, D+3, D+5)

## 1. Fundamentos

- **Objetivo**: prever tendências de curto prazo (D+1, D+3, D+5) para auxiliar decisões de alocação.  
- **Meta de negócio**: retorno líquido ≥ 8% a.a.  
- **Piso inegociável**: +3% absoluto no início; opcionalmente migrar para trajetória vinculada à curva 8% a.a.  
- **Viés conservador**: foco em preservação de capital.  
  - Venda = compulsória (sensibilidade máxima a ↓).  
  - Compra = opcional (alta precisão exigida para ↑).  

---

## 2. Dados e Camadas

### Bronze
- Ingestão de 8–12 anos de dados do IBOV (mínimo).  
- Padronização: timezone único, nomes consistentes, dtypes coerentes.  
- Validação: relatórios de sanidade e manifesto de ingestão.  

### Silver
- Normalização de calendário de pregões.  
- Features “sem opinião”: retornos simples, janelas, estatísticas de volatilidade, indicadores básicos.  
- Introdução de variável de regime (bull, bear, lateral).  
- Manifesto Silver com cobertura, dtypes e qualidade.  

### Gold
- Rotulagem 3-classes (↓, 0, ↑) por horizonte:  
  - D+1: 45–55% neutros  
  - D+3: 38–45% neutros  
  - D+5: 30–38% neutros  
- Neutralidade definida **apenas na rotulagem** (sem banda neutra extra na decisão).  
- Particionamento temporal walk-forward (6–8 blocos, embargo ≥ 5 pregões).  
- Gold armazenado em Parquet particionado + manifesto de distribuição de classes.  

### Expansão
- Após validação inicial com IBOV, estender para **24 tickers balanceados** (multivariado).  

---

## 3. Modelagem

- **Modelos-base**:  
  - XGBoost (baseline robusto).  
  - CatBoost (probabilidades estáveis).  
  - LogReg multinomial (sanity check: se empatar, limite é informacional).  
- Avaliação:  
  - MCC macro por bloco.  
  - Acurácia balanceada.  
  - F1↑ e F1↓.  
  - Qualidade das probabilidades (Brier/NLL).  
- Calibração: Platt ou Isotonic.  

---

## 4. Política de Decisão

- **Venda compulsória**  
  - Gatilho: agregador de probabilidades de ↓ (curto + médio prazo).  
  - Venda se p(↓) ≥ θ↓, ajustado para manter risco de violar piso < 1%.  

- **Compra opcional**  
  - Requer consistência entre horizontes (D+1, D+3).  
  - Filtro de hurdle: E[retorno] ≥ meta pró-rata (0,03% D+1; 0,09% D+3; 0,15% D+5).  
  - Bloqueio se p(↓) em D+5 ultrapassar limite.  

- **Neutro**  
  - Sempre que critérios de compra/venda não forem satisfeitos.  

---

## 5. Overlay de Risco

- **CPPI leve**  
  - Piso absoluto Ft = 1,03 × capital inicial.  
  - Almofada Ct = max(Vt − Ft, 0).  
  - Exposição ao risco Et = m × Ct (m = 2–4).  
  - Se Vt → Ft, exposição → 0.  

- **Position sizing por volatilidade**  
  - Peso ∝ Cushion / σh, com limite máximo wmax.  
  - Stops estatísticos para P&L anormal ou gatilho de venda.  

- **Kill switch**  
  - Caixa forçado se probabilidade de violar piso > α (ex.: 1%).  

---

## 6. Critérios de Aceitação

### Técnicos
- MCC macro > 0 em todos os blocos.  
- Acurácia balanceada > baseline trivial.  
- F1(↑) e F1(↓) positivos.  
- Distribuição de classes dentro das metas definidas.  

### De Negócio
- Piso +3% nunca violado.  
- Retorno líquido ≥ 8% a.a. (rolling 12m).  
- Drawdown controlado, underwater sempre ≥ +3%.  
- Turnover e custos efetivos dentro de limites aceitáveis.  

---

## 7. Governança e Papéis

- **Owner**: define objetivos e aprova marcos.  
- **Estrategista**: emite instruções padronizadas (LLM↔LLM, objetivo, requisitos, dry run, checklist) e valida outputs.  
- **Agente**: responde apenas com código auto-contido; primeira execução sempre `dry_run=True`; sem improviso.  

### Escalonamento
- Se erro se repetir 2 vezes consecutivas → Agente deve parar e formular dúvidas objetivas.  
- Estrategista corrige instrução e atualiza SSOT.  

### Entregáveis por fase
- Manifestos (CSV/MD).  
- Logs de qualidade.  
- Hashes de artefatos.  
- Relatórios de métricas.  
- Gold versionado + modelos calibrados + thresholds congelados.  

---

## 8. Próximos Passos

1. **Fase 0 (Setup & SSOT)**: consolidar diretórios, manifestos e convenções.  
2. **Fase 1 (Bronze)**: ingestão IBOV 8–12 anos, validação de sanidade, manifesto.  
3. **Fase 2 (Silver)**: normalização de calendário, features básicas, regimes.  
4. **Fase 3 (Gold)**: rotulagem 3-classes, particionamento temporal, manifesto Gold.  
5. **Fase 4 em diante**: modelagem, calibração, política de decisão, overlay de risco, backtest.  

---
