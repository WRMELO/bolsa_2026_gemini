
# MEA — Matriz de Endereçamento de Artefatos (BOLSA_2026_GEMINI)

## Regras Globais
- Não versionar dados (00_data/) nem saídas (04_outputs/) no Git.
- Nomes: snake_case + sufixo de data/hora quando aplicável: nome_recurso_YYYYMMDD_HHMM.ext
- Caminhos SEMPRE resolvidos a partir de ROOT_PROJECT.

## Tabela de Roteamento
| Tipo de artefato       | Caminho padrão                                     | Extensões aceitas              | Quem cria | Quem valida |
|------------------------|-----------------------------------------------------|--------------------------------|-----------|-------------|
| Dados brutos           | 00_data/01_raw/                                     | .csv .parquet .json .zip       | Owner     | Estrategista|
| Dados processados      | 00_data/02_processed/                               | .parquet .csv                  | Agente    | Estrategista|
| Dados finais           | 00_data/03_final/                                   | .parquet .csv                  | Agente    | Estrategista|
| Notebooks prototyping  | 01_notebooks/prototyping/                           | .ipynb                         | Owner     | Estrategista|
| Notebooks EDA          | 01_notebooks/analysis/                              | .ipynb                         | Owner     | Estrategista|
| Notebooks modeling     | 01_notebooks/modeling/                              | .ipynb                         | Owner     | Estrategista|
| Código fonte           | 02_src/                                             | .py                            | Agente    | Estrategista|
| Conhecimento (vault)   | 03_knowledge_base/                                  | .md                            | Owner     | Estrategista|
| Modelos treinados      | 04_outputs/models/                                  | .pkl .pt .onnx .h5             | Agente    | Estrategista|
| Relatórios             | 04_outputs/reports/                                 | .md .html .pdf                 | Agente    | Estrategista|
| Figuras                | 04_outputs/figures/                                 | .png .jpg .svg                 | Agente    | Estrategista|
| Checkpoints            | 05_checkpoints/                                     | .md                            | Estrategista| Owner     |

## Convenções de nomes (exemplos)
- Dataset final: ibov_silver_YYYYMMDD.parquet
- Modelo: xgb_caivscai_v1_YYYYMMDD.pkl
- Relatório: eda_ibov_YYYYMMDD.html
- Checkpoint: checkpoint_YYYYMMDD_HHMM.md
