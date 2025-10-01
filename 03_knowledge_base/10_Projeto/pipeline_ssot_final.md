# Pipeline diário – SSOT de Close e Volume

Resumo do fluxo final implementado para coleta, padronização e materialização dos painéis SSOT (Single Source of Truth) em Parquet.

## Objetivo

- Manter diariamente uma base consolidada para 31 séries (24 ações B3 .SA + 7 indicadores), de 2012-01-01 até a data mais recente disponível.
- Padronizar schema e timezone (America/Sao_Paulo) em uma camada “adequado”.
- Gerar painéis wide (date + colunas=tickers) para close e volume em `00_data/02_curado` como SSOT.

## Camadas e artefatos

- 00_data/01_bruto
  - Parquets individuais por série com OHLCV (coletados de investpy e yfinance).
- 00_data/02_adequado
  - Mesmos dados normalizados: colunas [ticker, date, open, high, low, close, volume, datetime_sp].
  - date é string YYYY-MM-DD; datetime_sp em TZ America/Sao_Paulo.
- 00_data/02_curado
  - `panel_close.parquet` e `panel_volume.parquet`: matrizes diárias (linhas = datas; colunas = tickers)
  - `panel_close_manifest.json` e `panel_volume_manifest.json`: metadados (linhas, colunas, datas mín/máx, tickers, source).

## Fontes de dados

- Ações B3 (.SA): investpy (primeira opção) com fallback para yfinance.
- Indicadores/ETF/commodities: yfinance.

## Janela de datas

- 2012-01-01 até a data de corte mais recente definida no ambiente/execução.

## Regras de padronização (02_adequado)

- Renomeação de colunas para o schema: [ticker, date, open, high, low, close, volume, datetime_sp].
- datetime_sp sempre em America/Sao_Paulo; date normalizado (YYYY-MM-DD).
- Remoção de duplicados por (ticker, date).
- Recorte para a janela alvo.

## SSOT (02_curado)

- Construído diretamente a partir de `00_data/02_adequado` via pivot, sem depender de CSVs de estágio.
- Resultados:
  - `panel_close.parquet`
  - `panel_volume.parquet`
  - Manifestos JSON respectivos com metadados e a tag `source: "from_02_adequado"`.

## Orquestração

- Script: `02_src/update_to_ssot.py`
  - Passos:
    1) Ingestão para `00_data/01_bruto` (investpy/yfinance)
    2) Padronização em `00_data/02_adequado`
    3) Materialização SSOT (close/volume) em `00_data/02_curado`
  - Flags CLI: `--start`, `--end`, `--skip-ingest`, `--skip-adequado`, `--skip-ssot`, `--floor`.
  - Implementado para gerar sempre o SSOT diretamente de 02_adequado.

## Verificação de qualidade

- Notebook `01_notebooks/estruturacao_e_ingesta.ipynb` possui célula de verificação que:
  - Lê os Parquets SSOT
  - Reporta datas globais (mín/máx), número de linhas e, por ticker, a primeira/última data com valor e % de cobertura.

## Operação diária (resumo)

1) Executar o orquestrador para atualizar dados e SSOT.
2) Abrir o notebook e rodar a célula de verificação para conferir datas e cobertura.

## Decisões importantes

- Simplicidade sobre camadas intermediárias: SSOT é gerado diretamente de 02_adequado para evitar drift.
- MinIO e estágios CSV foram deixados como opcionais/futuros; não afetam a geração do SSOT.

## Próximos passos sugeridos (opcionais)

- Exportar CSVs de qualidade (cobertura por ticker) para `00_data/02_curado`.
- Checagem automática de consistência entre painéis de close e volume (mesmos índices/colunas).
