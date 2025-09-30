# BOLSA_2026_GEMINI

Projeto exclusivo em **Google Colab Pro + Drive Compartilhado + Gemini**, com governança disciplinada, SSOT explícito e trilha de checkpoints.

## Visão Geral

Este repositório acompanha o projeto `BOLSA_2026_GEMINI`, isolado do ciclo anterior (VS Code, containers, MinIO, PostgreSQL). Toda a execução ocorre no ecossistema Google: **Colab Pro** (execução), **Gemini** (agente de código) e **Drive Compartilhado** (armazenamento). O **Obsidian** é utilizado para memória e registro de decisões.

## Escopo e Ambiente

- Agente LLM: **Gemini** (gera apenas código em bloco único, conforme instruções).
    
- Estrategista: **GPT-5 Thinking** (define regras, valida, não entrega código para execução direta).
    
- Armazenamento raiz (Shared Drive):  
    `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/`
    
- Vault Obsidian:  
    `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/03_knowledge_base/`
    

## SSOT e Estrutura de Pastas

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

- **SSOT de endereçamento**: `03_knowledge_base/40_Logs_e_Decisoes/MEA_Matriz_Enderecamento.md`  
    Define, por tipo de artefato, o diretório correto, extensões aceitas e responsabilidades (quem cria/valida).
    

## Governança e Protocolos Ativos

1. **PROTOCOLO PERMANENTE DE RELACIONAMENTO — Owner ↔ Estrategista ↔ Agente**
    
2. **PROTOCOLO GPT-5 – MODO DUAL V1.2 (Instant + Thinking)**
    
3. **MANUAL DE APLICAÇÃO PRÁTICA — Protocolo Permanente**
    

Diretrizes operacionais relevantes:

- O Estrategista numera cada instrução: `ORIENTAÇÃO #00X`.
    
- O Agente replica o número no topo do código (comentário) e como primeira linha da saída (`print("ORIENTAÇÃO #00X")`).
    
- Execução em duas rodadas: **dry_run=True** (simulação) → **dry_run=False** (persistência), sem mudar a especificação entre as rodadas.
    
- Escopo exclusivo: apenas Drive Compartilhado `BOLSA_2026`.
    

## Regras de Versionamento (.gitignore)

Por padrão, **não são versionados**:

- Dados: `00_data/`
    
- Saídas: `04_outputs/`
    
- Configurações do Obsidian: `03_knowledge_base/.obsidian/`
    
- Caches e ambientes (`__pycache__`, `.ipynb_checkpoints/`, `.venv/`, etc.)
    

Observação: `05_checkpoints/` está ignorado por padrão. Remova essa entrada do `.gitignore` caso deseje versionar checkpoints.

## Utilitários

### Montagem do Google Drive

- Utilitário: `02_src/utils_drive.py`
    
    - `is_colab()` detecta se o código está rodando no Google Colab.
        
    - `mount_drive(mount_point='/content/drive')` monta o Google Drive no Colab ou configura ambiente local.
        
    - `get_project_root()` retorna o caminho raiz do projeto (Colab ou local).
        
    - `setup_environment()` configura o ambiente completo: monta drive, resolve caminhos e adiciona ao PYTHONPATH.
        

Este utilitário permite que os notebooks funcionem tanto no **Google Colab** quanto **localmente** sem modificações.

Exemplo de uso:

```python
from importlib.util import spec_from_file_location, module_from_spec
import os

# Localizar e importar o utilitário
utils_drive_path = os.path.join(os.getcwd(), '02_src', 'utils_drive.py')
spec = spec_from_file_location('utils_drive', utils_drive_path)
utils_drive = module_from_spec(spec)
spec.loader.exec_module(utils_drive)

# Configurar ambiente (funciona no Colab e localmente)
drive_path, project_root = utils_drive.setup_environment()
```

### Caminhos do Projeto

- Configuração canônica: `02_src/config_paths.yaml`
    
- Utilitário: `02_src/utils_paths.py`
    
    - `ROOT` aponta para a raiz do projeto.
        
    - `P(key, *extra, create_dirs=False)` resolve caminhos de forma segura:
        
        - Se `create_dirs=True` e **sem** `*extra`: cria o diretório da chave.
            
        - Se `create_dirs=True` e **com** `*extra`: cria o diretório pai do caminho final.
            
    - `ensure_dirs(*keys)` cria de forma idempotente os diretórios base desejados.
        

Exemplo de uso:

```python
from importlib.util import spec_from_file_location, module_from_spec

# Import dinâmico do utilitário (quando fora do PYTHONPATH)
spec = spec_from_file_location(
    "utils_paths",
    "/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/02_src/utils_paths.py"
)
utils = module_from_spec(spec)
spec.loader.exec_module(utils)

# Resolver caminhos
print(utils.P("data_processed"))
utils.ensure_dirs("models", "reports", "figures")
```

## Obsidian

Aponte o cofre para:

```
/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/03_knowledge_base
```

Notas principais:

- `10_Projeto/00_Visao_Geral.md` — briefing e objetivos.
    
- `40_Logs_e_Decisoes/LOG_Checkpoints_*.md` — histórico disciplinado de checkpoints.
    
- `40_Logs_e_Decisoes/MEA_Matriz_Enderecamento.md` — roteamento dos artefatos.
    

## Fluxo Operacional

1. Owner define objetivo.
    
2. Estrategista emite **ORIENTAÇÃO #00X**.
    
3. Owner cola a instrução no Agente (Gemini).
    
4. Agente entrega **apenas um bloco de código**.
    
5. Primeira rodada: `dry_run=True` (simulação e validações).
    
6. Segunda rodada: `dry_run=False` (persistência idempotente).
    
7. Resultados e decisões são registrados em checkpoint no Obsidian.
    

## Status Atual

- Estrutura criada no Shared Drive.
    
- `.gitignore`, **MEA**, `config_paths.yaml` e `utils_paths.py` persistidos.
    
- **Checkpoint 0001** registrado no Obsidian (abertura do projeto e validações iniciais).
    

## Próximos Passos

- Registrar o próximo checkpoint com o plano de trabalho imediato.
    
- Iniciar a série de notebooks em `01_notebooks/` conforme o roteiro analítico.
    
- Manter a disciplina de orientações numeradas e rodadas dry_run → persistência.
    

## Licença

A definir pelo Owner.