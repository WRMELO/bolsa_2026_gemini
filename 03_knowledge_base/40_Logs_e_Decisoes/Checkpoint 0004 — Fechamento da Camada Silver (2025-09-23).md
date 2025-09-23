
## 0) Objetivo

Encerrar a camada **Silver** com evidências de persistência e manifesto, e preparar o debate sobre **Gold**/adequações em Silver.

---

## 1) Evidências de persistência (SSOT)

- **Pasta**: `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/00_data/02_silver/`
    
- **Artefatos gravados (2025-09-23)**:
    
    - `silver_close_20250923.parquet` _(versão ativa: `_v2` conforme execução)_
        
    - `silver_adj_close_20250923.parquet` _(_v2_)_
        
    - `silver_volume_20250923.parquet` _(_v2_)_
        
    - `silver_dividends_20250923.parquet` _(_v2_)_
        
    - `silver_splits_20250923.parquet` _(_v2_)_
        
    - `dim_symbols_20250923.parquet` _(_v2_)_
        
    - `map_symbol_alias.csv` _(_v2_)_
        
- **Manifesto Silver**: `silver_manifest_20250923_v2.csv` (inventário de 15 artefatos)
    

---

## 2) Qualidade dos Tabelões (resumo de QC)

- **Shape por tabelão**: (3409 × 31). Índice temporal: **2012‑01‑02 → 2025‑09‑19**.
    
- **Cobertura macros (non‑NaN %)**: `_bvsp 99.74%`, `_gspc 97.36%`, `_tnx 97.33%`, `_vix 97.36%`, `dx‑y.nyb 97.39%`, `ewz 97.36%`, `bz=f 96.86%`.
    
- **Colunas com mais NaNs** (motivo: estreia em bolsa posterior ao início da janela): `RDOR3`, `HAPV3`, `RAIL3`.
    
- Padrões Silver confirmados: **sem imputação, sem features**, unidades nativas, outer join ao calendário canônico B3.
    

---

## 3) Decisão

**Silver: CONCLUÍDA e ACEITA**. Manifesto verificado e persistido. Sem reexecução necessária.

---

## 4) Itens para decisão (próxima etapa)

### 4.1 Critérios mínimos para permanência de séries no **Silver pleno**

- **Cobertura mínima por coluna (Adj Close)** no calendário B3: sugerido **≥ 90%** (tolerância para IPOs recentes: **≥ 60%** com flag `recent_ipo`).
    
- **Integridade do índice temporal**: 100% normalizado (sem tz, sem duplicidades).
    
- **Aderência de esquema**: presença de `Close`, `Adj Close`, `Volume` em equities; macros podem carecer de `Adj Close` e ficam isentos.
    
- **Eventos corporativos**: divisões e proventos consistentes (NaN permitido quando inexistentes; não imputar em Silver).
    

> **Observação**: com esses thresholds, `RDOR3` (~34.8% cobertura) provavelmente **sai do Silver pleno** e permanece categorizado como **“Silver‑parcial”** para uso em análises específicas.

### 4.2 Encaminhamento para **Gold**

- Gold = derivativos/indicadores: retornos (log/aritm.), volatilidades (janelas), drawdown, beta/alpha, spreads (EWZ vs. IBOV, BRL proxy via DXY), normalizações, features de evento (ex‑div, splits) — **sempre** a partir do Silver.
    
- Disciplina: **DRY RUN → PERSIST** com manifesto próprio `gold_manifest_YYYYMMDD.csv`.
    

---

## 5) Próximos passos propostos

1. **Deliberar** e cravar os **critérios mínimos** (item 4.1). Emitir _DID‑SILVER‑CRIT_.
    
2. Executar **SILVER_FILTER_APPLY_V1** (dry run): gerar lista de colunas “pleno” vs. “parcial” + relatório de impacto.
    
3. Aprovar e persistir o filtro; atualizar **silver_manifest** com flags de elegibilidade.
    
4. Iniciar desenho de **GOLD_BASE_V1** (dry run): especificação de features e outputs padronizados.
    

---

**Fim do Checkpoint 0004 — Camada Silver encerrada.**