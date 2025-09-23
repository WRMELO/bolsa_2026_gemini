
## 0) Objetivo do Checkpoint

Consolidar **conduta/governança** e o **estado técnico** ao fim do dia 2025-09-22, para retomada sem atritos. Este documento é a fonte de referência (SSOT) deste marco.

---

## 1) Governança & Conduta (vinculantes)

- **Papéis**
    
    - **Owner**: define objetivo/GO–STOP; não decide detalhes técnicos.
        
    - **Estrategista**: **emite instruções completas** (sem perguntas), valida dry run, aprova/nega persistência, registra checkpoints.
        
    - **Agente (Gemini 2.5 Pro)**: executa **1 bloco** autocontido por instrução; roda **dry_run→persist**.
        
- **Disciplina**
    
    - Sem perguntas de confirmação do Estrategista; linguagem técnica, normativa e direta.
        
    - **Dry run** sempre antes; **persistência** só com GO explícito (sem reescrever instrução).
        
    - **DÚVIDA_BLOQUEANTE** para qualquer ambiguidade/erro de qualidade que invalide persistência.
        
    - **Anti‑ambiguidade pandas**: proibido truth‑value de Series/DataFrame; sempre reduzir a escalar.
        
- **SSOT de caminhos**
    
    - ROOT: `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/`
        
    - RAW: `00_data/01_raw/` | SILVER: `00_data/02_silver/`
        
    - Proibido usar MyDrive e adivinhação de paths.
        

---

## 2) Estado técnico consolidado

### 2.1 Bronze (camada bruta) — **CONCLUÍDA**

- **24 tickers (.SA)**: ITUB4.SA, BBAS3.SA, B3SA3.SA, PSSA3.SA, VALE3.SA, GGBR4.SA, CSNA3.SA, SUZB3.SA, PETR4.SA, PRIO3.SA, UGPA3.SA, ELET3.SA, TAEE11.SA, CPLE6.SA, SBSP3.SA, VIVT3.SA, TIMS3.SA, RDOR3.SA, HAPV3.SA, ABEV3.SA, WEGE3.SA, TOTS3.SA, LREN3.SA, RAIL3.SA.
    
- **Índice/Indicadores (macros)**: ^BVSP, EWZ, ^GSPC, ^VIX, DX‑Y.NYB, ^TNX, **BZ=F** (fallback obrigatório: **CL=F**).
    
- **Janela**: 2012‑01‑01 → 2025‑09‑19; **yfinance**; `interval="1d"`; `actions=True`.
    
- **Persistência**: Parquet por ativo em `00_data/01_raw/…`; metadados (JSON) para macros disponível; equities sem metadados por limitação do `fast_info.to_dict` (não‑bloqueante).
    
- **Manifesto RAW**: `raw_manifest_20250922.csv` gerado (inventário de 31 arquivos Parquet).
    

### 2.2 Silver (tabelões reais) — **EM DRY RUN APROVADO**

- **Política Silver**: sem features, sem imputação; valores observados apenas.
    
- **Calendário canônico B3**: união das datas dos 24 .SA; 3409 pregões (2012‑01‑02 a 2025‑09‑19). Índices normalizados (tz‑free, `normalize()`).
    
- **Tabelões a persistir**: `silver_close_*`, `silver_adj_close_*`, `silver_volume_*`, `silver_dividends_*`, `silver_splits_*` (shape esperado **3409×31** cada).
    
- **Dimensões**: `dim_symbols_*` (31 linhas) e `map_symbol_alias.csv` (31 mapeamentos 1:1 com Bronze). Colunas dos tabelões = **alias do arquivo Bronze** (ex.: `itub4_sa`, `_bvsp`, `dx-y.nyb`, `bz=f`).
    
- **Cobertura macros** (dry run pós‑fix): `_bvsp 99.74%`, `_gspc 97.36%`, `_tnx 97.33%`, `_vix 97.36%`, `dx-y.nyb 97.39%`, `ewz 97.36%`, `bz=f 96.86%` — coerente com feriados internacionais.
    

---

## 3) Padrões técnicos (fixos)

- **Nomemclatura de arquivos**: snake_case + sufixo de data (`YYYYMMDD`); não sobrescrever — usar `_v2`, `_v3`…
    
- **Moedas/unidades**: manter nativas no Silver (BRL para .SA, USD/bbl para Brent, yield*10 para ^TNX, pontos para ^GSPC/^VIX/^BVSP). Conversões só no Gold.
    
- **Alinhamento temporal**: _outer join_ ao calendário B3; lacunas permanecem **NaN** (sem forward/back fill).
    
- **Relatórios mínimos**: shapes, `date_min/max` (quando aplicável), top‑5 colunas com mais NaN, cobertura macro (%), caminhos salvos, falhas com traceback completo.
    

---

## 4) Decisões registradas (DIDs)

1. **Estrategista não pergunta** se deve instruir: **instrui**. Owner só cola; Agente só executa.
    
2. **Dry run** obrigatório e suficiente para liberar persistência — sem reescrever instrução entre as rodadas.
    
3. **Silver ≠ Gold**: no Silver não existem D+N, retornos, médias, volatilidades ou normalizações.
    
4. **Alias de colunas** no Silver preserva o prefixo do arquivo Bronze (rastreabilidade 1:1), inclusive símbolos especiais.
    
5. **Fallback Brent**: se `BZ=F` indisponível, usar `CL=F` com nota de alias.
    

---

## 5) Riscos / Itens em aberto

- **Metadados equities**: falha benigna do `fast_info.to_dict`. Alternativas: `Ticker.info` (cautela) ou persistir subset mínimo (moeda, exchange) — tratar fora do caminho crítico.
    
- **Hashes**: revisar rotina de `sha256_tail20` (observação de repetição em amostra do raw_manifest).
    
- **Gold (futuro)**: especificar features e pipelines _on‑demand_ sobre o Silver; manter isolamento total de camadas.
    

---

## 6) Plano imediato de retomada (D+1)

1. Executar **SILVER_TABELAO_V1** com `dry_run=False` (persistência dos 5 tabelões + dimensões + manifesto Silver).
    
2. QC rápido pós‑persistência: shapes, cobertura macro, top‑5 NaN, caminhos salvos.
    
3. Registrar **Checkpoint 0004** com o fechamento da camada Silver.
    

---

## 7) Anexos úteis

**A) Tickers (24 .SA)**: ITUB4, BBAS3, B3SA3, PSSA3, VALE3, GGBR4, CSNA3, SUZB3, PETR4, PRIO3, UGPA3, ELET3, TAEE11, CPLE6, SBSP3, VIVT3, TIMS3, RDOR3, HAPV3, ABEV3, WEGE3, TOTS3, LREN3, RAIL3.  
**B) Macros**: ^BVSP, EWZ, ^GSPC, ^VIX, DX‑Y.NYB, ^TNX, BZ=F (fallback CL=F).  
**C) Convenções de nomes**: `<alias>_ohlcv_actions_20120101_<YYYYMMDD>.parquet` (RAW) | `silver_<metric>_<YYYYMMDD>.parquet` (SILVER).

---

**Fim do Checkpoint 0003** — pronto para retomada amanhã.