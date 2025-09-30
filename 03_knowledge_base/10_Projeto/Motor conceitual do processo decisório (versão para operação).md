
## 1) Camadas de dados (já implantadas) → insumos do motor

- **Bronze**: dados brutos (OHLCV, dividendos, splits) por ativo/índice, sem tratamento.
    
- **Silver**: “tabelões” canônicos por métrica (Close, Adj Close, Volume, etc.), alinhados ao calendário B3; sem imputação, sem features.
    
- **Gold (a construir)**: **features** derivadas e **sinais** prontos para decisão (retornos, volatilidades, momentum, regimes, betas, etc.).
    
    - Observações-chave:
        
        - Tudo em **retornos** (não preço); evita efeito de “escala”.
            
        - **Defasagens coerentes** (lags) para internacionais (S&P, VIX, DXY, UST10, Brent, EWZ) respeitando horário/fuso → zero look-ahead.
            

---

## 2) Diagnóstico de regime (filtro de contexto)

**Por que antes?** A mesma regra funciona diferente em regimes diferentes (tendência vs. reversão; alta vs. baixa volatilidade).

- **Ferramentas**:
    
    - **Volatilidade de mercado**: VIX e vol implícita/realizada do IBOV (ex.: janelas 21/63).
        
    - **Regime discreto** (2–3 estados): _low vol / normal / high vol_. Pode ser simples (limiares de VIX) ou HMM (Markov) se quisermos refinar depois.
        
- **Uso**: Regime controla **histerese** (faixas de gatilho) e agressividade (tamanho de posição, limites de risco).
    

> _Histerese_: duas faixas de decisão para reduzir “vai e volta”; ex.: entrar acima de 0,60 e só sair abaixo de 0,50.

---

## 3) Sinais de **tendência** (classificação)

**Alvo**: probabilidade de “alta” vs. “baixa” em **D+1** e **D+5** (dois horizontes).  
**Por quê 2 horizontes?** D+1 dá timing, D+5 entrega persistência; exigimos **consistência** entre eles para ações contundentes (ex.: venda compulsória só com concordância).

- **Features de base** (por ativo):
    
    - **Retornos**: D-1, D-5, D-21, cumulativos, e retornos normalizados por vol (z-score).
        
    - **Momentum**: médias/médias-exponenciais, MACD simples (versões sem “indicador mágico”: são só diferenças de médias).
        
    - **Volatilidade**: janelas 21/63/252 (anualizada).
        
    - **Eventos**: flags de ex-div, splits (efeitos pontuais).
        
- **Features macro (internacionais)**:
    
    - S&P500, VIX, DXY, UST10, Brent, EWZ — **sempre defasados** para evitar vazamento.
        
    - **Seleção/compactação**:
        
        - **PLS/LASSO** (_prioridade_) — escolhem variáveis mais úteis ao alvo, mantendo interpretabilidade.
            
        - **PCA rolling** (_plano B_) — reduz colinearidade, mas perde interpretabilidade.
            
- **Modelos**:
    
    - **Baseline interpretável**: _Logistic Regression_ (com Elastic Net) — rápido, auditável.
        
    - **Boosted Trees** (XGBoost/LightGBM) — capturam não-linearidades; usar **calibração** depois (Platt/Isotônica).
        
    - **Saídas**: `P_up_D1`, `P_up_D5` calibradas (probabilidades confiáveis).
        
- **Métricas de validação**:
    
    - **Brier Score** (qualidade de probabilidade), **ECE** (calibração), **PR-AUC** (classe desbalanceada).
        

> _Calibração_: mapeamento que ajusta a “confiança” do modelo para bater a frequência real observada.

---

## 4) Magnitude **condicional** (opcional, para sizing)

Não prevemos preços; estimamos **retorno esperado** **condicionado** à classe (sobe/caiv).

- **Ferramentas**:
    
    - **Regressão quantílica** (ex.: estimar Q10/Q50/Q90 de retorno) ou regressão simples com _winsorization_ (cortar extremos).
        
- **Uso**: quando `P_up` (ou `P_down`) é alta, a magnitude estimada ajuda no **tamanho da posição** (não na direção).
    

---

## 5) Tradução de probabilidade → **edge** (valor esperado líquido)

Transforma probabilidade em dinheiro esperado **depois de custos**.

- **Como**:
    
    - **Binning** histórico das probabilidades (ex.: decílios) e cálculo do retorno médio por bin.
        
    - **Edge líquido** = retorno esperado do bin – custos – slippage.
        
- **Por quê**: evita comprar porque `P_up=0,55` se o bin 0,55–0,60 não paga custos no histórico.
    

---

## 6) Regras de decisão (política operacional)

### 6.1 Venda **compulsória** (risk-first)

- **Gatilho** (exemplo):
    
    - Se regime ≠ _high-noise_, `P_down_D1 ≥ 0,60` **E** `P_down_D5 ≥ 0,55` → **sair** (zerar ou reduzir conforme edge).
        
- **Histerese**: só reverter se `P_down_D1 ≤ 0,50` **E** `P_down_D5 ≤ 0,50`.
    
- **De-risk progressivo**: reduzir 25/50/75/100% da posição conforme _score_ sobe.
    

### 6.2 Compra **opcional** (seleção)

- **Ranking** de candidatos: **edge_up líquido por risco** (edge_up / vol prevista), respeitando:
    
    - **Limites de concentração** (setor, correlação, top-k por cluster).
        
    - **Exposição agregada** (beta IBOV alvo).
        
- **Entrada** só em bins onde o **backtest** mostrou edge positivo pós-custos.
    

### 6.3 Tamanho da posição (sizing)

- **Vol-targeting**: ajustar o lote para que a **vol de contribuição** por ativo fique dentro do alvo (ex.: 1%/dia portfólio).
    
- **Kelly-lite**: fração reduzida (ex.: 25–50% da Kelly) usando **edge/variance**; sempre capado por risco/regime.
    

### 6.4 Execução e custos

- **Modelo simples de slippage** (spread + impacto por volume).
    
- **Turnover control**: não trocar posição por variações pequenas de probabilidade (deadband).
    

---

## 7) Portfólio e risco agregados

- **Budget por fator/cluster**: não deixar todos os “bons sinais” em elétricas, por ex.
    
- **Beta e correlação**: controlar **exposição ao IBOV** (neutralizar/limitar conforme objetivo).
    
- **Stops/targets do portfólio**: _drawdown_ máximo, VaR approximado, cortes de risco por regime.
    

---

## 8) Validação e governança (anti-overfit)

- **Backtest temporal** com **Purged K-Fold** / **Walk-forward** (anchors) com _purge gap_ (evita contaminação).
    
- **Métricas de trading**: Sharpe/Sortino, Max Drawdown, hit rate, turnover, _capacity_ (liquidez).
    
- **Monitoração contínua**: drift de dados/sinais, spikes de NaN, “quebra” de calibração (ECE ↑).
    
- **Manifestos** (Silver/Gold) e **logs de atualização** (faixas de datas, hashes, custos estimados).
    

---

## 9) Onde entra **RL** (Reinforcement Learning) — _quando e como_

RL **não** substitui os sinais; ele otimiza a **política** (quando/quanto agir) sob restrições de risco/custos.

- **Fase 2 (após supervisão robusta)**:
    
    - **Contextual bandits** para **sizing** e **ordem de execução** (exploração controlada das intensidades).
        
    - **Offline RL** para política em janelas específicas (com _off-policy evaluation_ cuidado para não “alucinar” edge).
        
- **Por que depois?** Precisamos primeiro de **probabilidades calibradas** e **edge por bin** estáveis; RL em cima de sinal frágil vira overfit sofisticado.
    

---

## 10) Decisões do Owner que parametrizam o motor

1. **Limiar de elegibilidade Silver-pleno** (cobertura) — sug.: ≥90% (IPOs ≥60% com flag).
    
2. **Horizontes oficiais** de tendência — D+1 e D+5 (obrigatórios).
    
3. **Janelas padrão** (21/63/252) e _opcionais_ (10/120).
    
4. **Regime filter**: limiares de VIX/vol para _low/normal/high_ e quanto isso altera histerese/sizing.
    
5. **Bins de probabilidade** que serão operáveis (onde o histórico paga custos).
    
6. **Limites de concentração** (setor/corr/ativo) e **alvo de beta** vs. IBOV.
    
7. **Cadência operacional** D+0 ou D+1 (recomendo D+1 para estabilidade inicial).
    
8. **Entrada de RL**: somente após 1º ciclo Gold estável (sim/não, e onde: sizing/execução).
    

---

## 11) Glossário rápido

- **Calibração**: ajustar a probabilidade prevista para refletir frequência real observada.
    
- **Brier/ECE**: métricas que avaliam se “0,60” realmente acerta ~60% das vezes.
    
- **Histerese**: gatilhos diferentes para entrar e sair, reduzindo “zig-zag”.
    
- **Edge**: retorno esperado **após custos**; o que justifica a operação.
    
- **Purge gap**: janela removida entre treino e teste para impedir vazamento temporal.
    
- **PLS/LASSO**: técnicas que selecionam features relevantes ao alvo; PCA compacta, mas tira interpretabilidade.
    

---

## 12) Linha do tempo operacional (sem instruções ainda)

1. **Fechar critérios Silver-pleno** e flags de elegibilidade.
    
2. **Gold-Base V1 (DRY RUN)**: gerar `P_up_D1/D5` calibradas, bins e mapa prob→edge; definir regimes e histerese.
    
3. **Gold-Base V1 (PERSIST)** + manifesto Gold.
    
4. **Backtest governança** (purged CV) com custos realistas.
    
5. **Operacional D+1** com monitoramento/alertas.
    
6. **Fase 2**: RL para sizing/execução, se (e só se) a fase 1 estiver estável.
    

---

Quando você voltar, uso este motor como base e converto em **instruções normativas** na ordem correta (DRY RUN → validação → PERSIST), já com os parâmetros que você cravar nos itens de decisão.