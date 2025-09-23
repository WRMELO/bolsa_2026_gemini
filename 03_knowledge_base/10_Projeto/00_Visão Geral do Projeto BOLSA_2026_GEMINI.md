

Este é para dar a visão clara de todo o jogo, inspirado no tom do primeiro checkpoint.

```markdown
# Visão Geral — Projeto BOLSA_2026_GEMINI

## Identidade

- **Projeto**: BOLSA_2026_GEMINI  
- **Ambiente**: Google Colab Pro + Drive Compartilhado + Gemini  
- **Agente LLM**: Gemini (execução de código sob instrução)  
- **Estrategista**: GPT-5 (planejamento e validação)  
- **Owner**: define objetivos e aprova marcos  

---

## Estrutura do Projeto

```

00_data/  
01_raw/  
02_processed/  
03_final/  
01_notebooks/  
prototyping/  
analysis/  
modeling/  
02_src/  
03_knowledge_base/  
10_Projeto/  
20_Fontes_de_Dados/  
30_Metodologia/  
40_Logs_e_Decisoes/  
50_Resultados/  
Templates/  
04_outputs/  
models/  
reports/  
figures/  
05_checkpoints/

```

- **MEA — Matriz de Endereçamento de Artefatos**: define SSOT de caminhos e donos.  
- **config_paths.yaml**: único arquivo de rotas, usado pelo `utils_paths.py`.  

---

## Regras Operacionais

- **Sequenciamento**: cada instrução recebe identificador (`ORIENTAÇÃO #00X`).  
- **Dry-run → Persistência**: mesma instrução em duas rodadas (primeiro `dry_run=True`, depois `False`).  
- **SSOT absoluto**: nenhuma hard-code fora do `config_paths.yaml`.  
- **Escopo exclusivo**: apenas Drive Compartilhado, sem heranças de VS Code/MinIO/Postgres.  

---

## Fases e Gates

- **F0 — Setup & SSOT**: convenções, logs, manifestos.  
- **F1 — Bronze**: ingestão, sanidade, manifesto.  
- **F2 — Silver**: calendário unificado, features sem opinião.  
- **F3 — Gold**: rotulagem 3-classes, walk-forward, manifesto.  
- **F4 — Modelo & Calibração**.  
- **F5 — Política de Decisão**.  
- **F6 — Overlay de Risco**.  
- **F7 — Backtest & Seleção**.  

Cada gate exige: manifesto, relatório de qualidade, hashes, decisão Go/NoGo.  

---

## Governança

- **Owner**: objetivos e aprovações.  
- **Estrategista**: emite instruções padronizadas, valida outputs.  
- **Agente**: gera código, sem improviso, sempre em `dry_run` na 1ª execução.  
- **Escalonamento**: erro repetido 2x → Agente para e devolve dúvidas objetivas.  

---

## Objetivo Final

Construir um sistema de previsão e decisão **robusto, auditável e disciplinado**, que respeite a preservação vitalícia de capital, atenda à meta de 8% a.a. e mantenha rastreabilidade técnica completa.
```

---

