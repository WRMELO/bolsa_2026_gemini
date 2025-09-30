

# Qual conjunto de horizontes adotar

   

## Avaliação das alternativas

**A. D+1 & D+5**

- Simples, estável e bem espaçado (dia e semana).  
    − Menos nuance para o RL (4 estados combinados). Pode forçar empates/tie-breaks frequentes.
    

**B. D+1 & D+3**

- Boa para timing tático; D+3 costuma carregar menos ruído que D+1.  
    − Espaçamento curto; maior correlação entre alvos, menor ganho marginal de informação.
    

**C. D+1, D+3 e D+5**

- Conjunto triádico curto-semanal com **9 estados** combinados: aumenta nuance decisória e a capacidade do RL distinguir persistência vs. reversão curto prazo.
    
- Mantém janelas com **densidade de rótulos** e **calibrabilidade** altas; “neutro” tende a diminuir conforme o horizonte alonga (D+1 > D+3 > D+5), o que ajuda a política de histerese.
    
- Embargo/purge moderado (≈ 5–6 pregões) ainda viável para validação temporal.  
    − Complexidade maior que A/B, porém controlada.
    

**D. D+1, D+5 e D+9**

- Escalas bem separadas (1, ~1 semana, ~2 semanas) — excelente para RL multi-escala.  
    − Em D+9 a **calibração degrada** mais (regime drift, custo de embargo ≈ 10 pregões, menor densidade efetiva), o que pode enfraquecer o sell-side compulsório na fase inicial.
    

## Recomendação

**Adotar agora D+1, D+3 e D+5 (opção C)** para o **Gold-Base V1**.  
Motivos: maximiza nuance (9 estados) sem sacrificar calibrabilidade, preserva sensibilidade para proteção (D+1) e adiciona persistência (D+3, D+5) alinhada ao motor e ao Plano v3. O conjunto é o melhor trade-off entre robustez estatística, governança (purge curto) e prontidão para habilitar o RL como camada de política na fase seguinte.

### Observação sobre D+9

Registrar **D+9** como “extensão Fase 1.1” (backlog): só considerar depois que D+1/3/5 estiverem calibrados e com bins prob→edge estáveis. A inclusão precoce tende a custar mais em embargo, drift e variância de estimativa do edge do que agrega em valor decisório.

## Implicações operacionais (sem instruções nem código)

- Rotular e calibrar `P_up/P_down` para **D+1, D+3 e D+5**; mapear bins prob→edge líquido por horizonte; definir **histerese multi-horizonte** (ex.: venda compulsória exige concordância D+1 & D+5, com D+3 como desempate e faixas de “sair/voltar” distintas).
    
- Validação temporal com **purged CV** usando embargo ≥ 5 pregões.
    
- Métricas-alvo: Brier/NLL e ECE por horizonte, F1↑/F1↓ e MCC macro por bloco; checar distribuição “neutro” dentro das bandas estipuladas no plano.
    
- Para RL na fase seguinte: usar o vetor de estado **[regime, bin(P_up_D1), bin(P_up_D3), bin(P_up_D5), edge_bins]**, com limites de risco/turnover impostos pelo overlay.
    

## Decisão e próximo ato do estrategista

**Decisão técnica**: Gold-Base V1 com **D+1, D+3 e D+5**.  
**Próximo ato**: redigir as **instruções normativas** ao Agente para executar o **DRY RUN** do Gold-Base V1 exatamente com esse tripé de horizontes.  
Quando quiser que eu emita essas instruções, diga “vamos fazer”.