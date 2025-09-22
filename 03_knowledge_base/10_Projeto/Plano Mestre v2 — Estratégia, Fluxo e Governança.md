Perfeito. Vou restabelecer o **Plano Mestre** em nível estratégico, acoplado ao nosso protocolo (Owner ↔ Estrategista ↔ Agente), incorporando o conteúdo validado do plano anterior e os pontos críticos levantados ontem. O texto abaixo é **agnóstico de projeto** (serve para qualquer iniciativa) e pode ser colado como documento de referência.

# Plano Mestre v2 — Estratégia, Fluxo e Governança

## 1) Visão e princípios

- **Objetivo**: construir um pipeline previsível, auditável e reprodutível, que gere dados/artefatos confiáveis para validação e decisão.
    
- **Princípios**: separação de papéis (Owner/Estrategista/Agente), camadas de dados (Bronze → Silver → Gold), critérios de aceite explícitos, escalonamento disciplinado, memória perene (SSOT).
    
- **Escopo-base de dados e entregáveis** seguem o arcabouço do plano anterior (engenharia de features, rótulos em D+1/D+3/D+5, particionamento temporal, modelo-base tabular e entregáveis padronizados), preservado como referência técnica.
    

## 2) Arquitetura por camadas (agnóstica de domínio)

- **Bronze**: ingestão + padronização mínima (carimbos de tempo, nomes, tipos), **sem** efeitos colaterais na 1ª execução (dry run).
    
- **Silver**: limpeza, normalização de calendários, alinhamento de granularidade, criação de variáveis derivadas “sem opinião” (ex.: retornos simples, janelas, contagens).
    
- **Gold**: dataset analítico com **rótulos de decisão** definidos por regra explícita (ex.: 3 classes com “zona neutra” parametrizada), particionamento temporal e manifesto reprodutível (schema, datas, contagens, qualidade).
    

## 3) Diretrizes estratégicas incorporadas das críticas

- **Amplitude de dados / regimes**: evitar “visão estreita” — trabalhar com janelas longas para cobrir múltiplos regimes (euforia, lateral, bear). Expandir horizonte histórico quando possível e **não** limitar a um único agregado ao longo de todo o desenvolvimento.
    
- **Rótulos e neutralidade**: manter **3 classes no dataset** (↑, 0, ↓). A zona neutra é configurada **na rotulagem**, não na regra de decisão final, para não “contaminar” inferência.
    
- **Separação compra vs venda**: compra é **opcional** (exige alta precisão e hurdle mínimo), venda é **compulsória** quando o risco sobe (sensibilidade maior a ↓). Os limiares são **parâmetros de negócio** e passam por calibração.
    
- **Camada de risco sobreposta (overlay)**: proteção de piso (ex.: +3% ou curva-alvo), _position sizing_ por volatilidade e “kill switch” para preservar capital, **independente** da qualidade do modelo.
    
- **Critérios de avaliação**: métricas técnicas por bloco temporal (ex.: MCC, acurácia balanceada, F1↑/F1↓) **+** métricas de negócio sob custos e overlay (sem violar piso; trajetória comparada à meta anual).
    

## 4) Fases e _stage-gates_ (aceite por fase)

**Fase 0 — Setup & SSOT**

- Consolidar diretórios/manifestos/nomes, registrar convenções e logs.
    
- **Gate**: documento de convenções aprovado + estrutura de logs/manifestos definida.
    

**Fase 1 — Bronze (Ingestão & Sanidade)**

- Ingestão com padronização mínima, timezone único, nomes consistentes, sem colunas não utilizadas.
    
- **Gate**: schema idêntico ao esperado, percentuais mínimos de não-nulos, relatório de qualidade e **proibição de persistência** se qualquer critério falhar.
    

**Fase 2 — Silver (Normalização & Features “sem opinião”)**

- Calendário unificado, janelas e estatísticas básicas, sem decisões “de negócio” embutidas.
    
- **Gate**: manifesto Silver (datas, linhas, dtypes, cobertura por campo) + testes de coerência temporal.
    

**Fase 3 — Gold (Rotulagem & Particionamento)**

- Rotulagem 3-classes por horizontes, metas de proporção neutra por horizonte, walk-forward/embargo, Parquet particionado, manifesto Gold.
    
- **Gate**: distribuição de classes válida por bloco, splits temporais corretos e reprodutibilidade confirmada.
    

**Fase 4 — Modelo-base & Calibração**

- Benchmark focado em robustez tabular e probabilidades estáveis; calibração (Platt/Isotônica).
    
- **Gate**: MCC macro > 0 e acurácia balanceada > baseline em todos os blocos (com relatório comparável).
    

**Fase 5 — Regras de Decisão (Compra opcional / Venda compulsória)**

- Limiarização coerente entre horizontes, _hurdle_ de retorno esperado, consistência de sinais.
    
- **Gate**: matriz de custos aplicada, _tuning_ justificado, estabilidade por bloco.
    

**Fase 6 — Overlay de Risco**

- Piso/almofada, sizing por vol, kill switch; validação de que o piso **não é violado**.
    
- **Gate**: simulações com custos mostrando preservação do piso e _underwater_ controlado.
    

**Fase 7 — Backtest & Seleção**

- Política consolidada (compra/venda/neutro) com custos; comparação a benchmark relevante.
    
- **Gate**: seleção final baseada em critérios de negócio e estabilidade; congelamento de versão (modelos + thresholds + Gold).
    

## 5) Papéis, comunicação e escalonamento (aplicação do protocolo)

- **Owner**: define objetivos e prioriza; não entra em detalhe técnico.
    
- **Estrategista**: emite instruções padronizadas (LLM↔LLM, objetivo, requisitos, dry-run, checklist), valida relatórios e decide Go/NoGo.
    
- **Agente**: responde **apenas** com bloco único de código auto-contido; 1ª execução sempre em `dry_run=True`; **sem** narrativas fora do bloco.
    
- **Escalonamento**: se **o mesmo erro** ocorrer **duas vezes seguidas**, o Agente deve **parar** e devolver **dúvidas objetivas**; o Estrategista ajusta a instrução e atualiza o SSOT.
    

## 6) Entregáveis e rastreabilidade

- **Por fase**: manifesto (CSV/MD), logs de qualidade, _artifact report_ (datas, volumes, dtypes, gaps), _diff_ de schema e _hashes_ dos artefatos relevantes.
    
- **Ao final**: Gold versionado + modelos calibrados + thresholds de decisão + relatório de backtest e métricas por bloco + documentação de execução.
    

## 7) Métricas-chave de sucesso do plano

- **Técnicas**: reprodutibilidade (hashes/manifestos), qualidade (não-nulos, coerência temporal), métricas por bloco > baseline, estabilidade sob walk-forward.
    
- **De negócio**: preservação do piso; trajetória alinhada à meta de retorno sob custos e overlay; _turnover_ e custos dentro de limites; ausência de violações materiais em períodos críticos.
    

---

## Próximo passo (já no fluxo protocolo)

Sem entrar em domínio/especificidade agora: quando disser “vamos fazer”, eu (Estrategista) **emito a Instrução 1 — Bronze: Ingestão & Sanidade (genérica)** no formato LLM↔LLM, com critérios de aceite e checklist. O Agente responderá com **um** bloco de código auto-contido em `dry_run=True`; você executa, traz o relatório, e eu valido o gate para avançarmos.