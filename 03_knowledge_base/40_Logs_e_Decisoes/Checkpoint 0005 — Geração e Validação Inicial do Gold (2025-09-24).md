:

---



## Situação atual

- **Camada Bronze**: concluída e persistida com partições e manifesto.
    
- **Camada Silver**: concluída, com manifestos (`silver_manifest_20250923.csv` e `silver_manifest_20250923_v2.csv`) e artefatos `silver_close`, `silver_adj_close`, `silver_volume`, `silver_dividends`, `silver_splits`, `dim_symbols`, `map_symbol_alias`.
    
- **Camada Gold**: em fase inicial (GERAÇÃO em DRY RUN).
    

---

## Artefato usado

- **Fonte**: `silver_manifest_20250923_v2.csv`
    
- **Close escolhido**: `silver_close_20250923_v2.parquet`
    
- **Integridade**:
    
    - `rows_total`: 3409
        
    - `cols_total`: 31
        
    - `file_size_bytes`: 561709
        
    - Bateu manifesto × arquivo físico.
        
- **Data**:
    
    - `date_min`: 2012-01-02
        
    - `date_max`: 2025-09-19
        
    - `n_linhas`: 3409
        
    - Fonte: índice do DataFrame (DatetimeIndex).
        
- **Universo de tickers**: 24 (excluídos macros whitelist).
    
    - 10 primeiros: `abev3_sa, b3sa3_sa, bbas3_sa, cple6_sa, csna3_sa, elet3_sa, ggbr4_sa, hapv3_sa, itub4_sa, lren3_sa`.
        

---

## Geração de rótulos (GOLD_GEN_V1, DRY RUN)

- **Horizontes**: D+1, D+3, D+5.
    
- **Distribuição obtida** (↓,0,↑):
    
    - D+1: 24.61% / 50.02% / 25.38% → ✅ dentro da banda [45%–55% neutro].
        
    - D+3: 19.84% / 58.54% / 21.62% → ⚠️ fora da banda [38%–45%].
        
    - D+5: 15.78% / 66.05% / 18.17% → ⚠️ fora da banda [30%–38%].
        
- **Critério aplicado**:
    
    - **D+1**: banda **crítica** → bloqueante se fora.
        
    - **D+3 e D+5**: banda apenas **informativa** (não bloqueante).
        
- **Status final do GEN**: DRY RUN concluído com sucesso.
    

---

## Próximo passo

Rodar **GOLD_VALIDATE_V1 (DRY RUN)**, que deve:

1. Confirmar integridade (manifesto × arquivo).
    
2. Confirmar datas canônicas (`date_min`, `date_max`).
    
3. Confirmar universo de tickers.
    
4. Reportar novamente distribuições de classes com hurdles.
    
5. Aplicar bloqueio **apenas se D+1 estiver fora da banda**.
    
6. Produzir resumo Gold em memória (shape + colunas de rótulos).
    

Somente após validação positiva será liberado o **GOLD_PERSIST_V1 (ExecProfile=WRITE)** para gravar em `00_data/03_gold/` e registrar o manifesto correspondente.

---

## Decisão conceitual consolidada

- **Venda compulsória**: sempre por ativo individual, sinal negativo → venda imediata.
    
- **Compra opcional**: recursos liberados podem ser alocados em qualquer subset dos demais ativos (exceto em quarentena), proporcional ao ranking global.
    
- **Rótulos**:
    
    - Critério **global** (mesma régua de neutro para todos os tickers) → garante comparabilidade.
        
    - **Bandas de neutro**:
        
        - D+1 → rígida, bloqueante.
            
        - D+3/D+5 → informativas, não bloqueantes.
            
- **Justificativa**: preserva a consistência estatística para treino e ranking, mas mantém a decisão individual por ativo.
    

---

## Estado de execução

- **Google Drive montado** e acessível.
    
- **SSOT** respeitado: arquivos lidos somente via manifesto.
    
- **Anti-simulação ativo**: todos os números vieram do Parquet físico.
    
- **Execução em DRY RUN**: nada persistido até aqui.
    

---

👉 Este checkpoint marca a **conclusão do GOLD_GEN_V1 em DRY RUN** e a definição clara do critério de validação: **D+1 bloqueante; D+3/D+5 informativos**.  
O próximo passo obrigatório é rodar o **GOLD_VALIDATE_V1 (DRY RUN)** antes de qualquer persistência.

---

