

## 1. Identificação e Escopo

- **Projeto:** `BOLSA_2026_GEMINI`
    
- **Ambiente exclusivo:** Google (Colab Pro + Drive Compartilhado + Gemini)
    
- **Agente LLM:** Gemini (executa apenas código, sob instruções do Estrategista)
    
- **Estrategista:** GPT-5 (este documento)
    
- **Isolamento:** não herda nada do projeto anterior (VS Code, containers, MinIO, PostgreSQL)
    

## 2. Localização física (SSOT de caminhos)

- **Shared Drive:** `BOLSA_2026`
    
- **Raiz do projeto (Drive):**  
    `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/`
    
- **Vault Obsidian:**  
    `/content/drive/Shareddrives/BOLSA_2026/a_bolsa2026_gemini/03_knowledge_base`
    

## 3. Estrutura criada e validada

Criada a árvore de diretórios padrão do projeto:

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

Status: estrutura confirmada no Drive Compartilhado com caminhos absolutos resolvidos.

## 4. Artefatos de governança e disciplina

- **`.gitignore`** criado na raiz do projeto com as regras:
    
    - Ignorar dados (`00_data/`) e saídas (`04_outputs/`).
        
    - Ignorar configs do Obsidian (`03_knowledge_base/.obsidian/`).
        
    - Ignorar caches/notebooks temporários, ambientes virtuais e arquivos de sistema.
        
    - Observação: `05_checkpoints/` está ignorado por padrão. Se desejar versionar checkpoints, remover essa linha do `.gitignore`.
        
- **MEA — Matriz de Endereçamento de Artefatos** criada em:  
    `03_knowledge_base/40_Logs_e_Decisoes/MEA_Matriz_Enderecamento.md`  
    Função: SSOT que define, por tipo de artefato, o diretório correto, extensões aceitas, quem cria e quem valida.
    
- **Configuração de caminhos (YAML)**
    
    - Arquivo: `02_src/config_paths.yaml`
        
    - Define `paths:` para todos os alvos (dados, notebooks, src, kb, models, reports, figures, checkpoints).
        
    - Política: não sobrescrever sem ordem explícita (SSOT).
        

## 5. Utilitário de caminhos — `utils_paths.py`

- **ORIENTAÇÃO #001** executada em duas rodadas:
    
    - Rodada A: `dry_run=True` (simulação) — prévia do arquivo, resolução de caminhos em memória, sem escrita.
        
    - Rodada B: `dry_run=False` (persistência) — escrita efetiva, import e testes.
        
- **Local do arquivo:** `02_src/utils_paths.py`
    
- **Comportamento implementado:**
    
    - Carrega `02_src/config_paths.yaml` (com `yaml.safe_load`).
        
    - `ROOT` definido como o diretório pai de `02_src`.
        
    - Função `P(key, *extra, create_dirs=False)`:
        
        - Se `create_dirs=True` e **sem** `*extra`: cria o **próprio diretório alvo** da chave.
            
        - Se `create_dirs=True` e **com** `*extra`: cria o **diretório pai** do caminho final (caso de arquivo destino).
            
        - Erro normativo: `PathKeyNotFoundError("PATH_KEY_NOT_FOUND: <key> …")` para chave ausente.
            
        - Erro normativo: `FileNotFoundError("VALIDATION_ERROR: CONFIG_NOT_FOUND: <path>")` se o YAML não existir.
            
    - Função `ensure_dirs(*keys)` idempotente, usando `P(..., create_dirs=True)`.
        
    - Sem logs automáticos na importação; logs apenas quando chamado.
        
- **Testes aplicados com sucesso:**
    
    - `ensure_dirs("data_processed","data_final","models","reports","figures","checkpoints","kb","nb_analysis")`.
        
    - Resolução e existência confirmadas para `P("kb")` e `P("nb_analysis")`.
        
- **Disciplina de não hard-code:** nenhum caminho absoluto fora de `ROOT_PATH`.
    

## 6. Regras operacionais consolidadas (este projeto)

- **Sequenciamento de instruções**
    
    - Cada instrução do Estrategista recebe um identificador: `ORIENTAÇÃO #00X`.
        
    - O Agente deve:
        
        - Repetir o identificador na **primeira linha do código** (comentário).
            
        - Imprimir o identificador como **primeira linha da saída** (`print("ORIENTAÇÃO #00X")`).
            
- **Dry-run → Persistência**
    
    - Mesma orientação é executada em duas rodadas:
        
        - Rodada A: `dry_run=True` (simulação).
            
        - Rodada B: `dry_run=False` (persistência).
            
    - Não emitir nova orientação entre A e B; apenas alternar o flag.
        
- **Escopo exclusivo**
    
    - Operar somente em Drive Compartilhado `BOLSA_2026`, sem `MyDrive` e sem integrações herdadas (containers, MinIO, PostgreSQL).
        
- **SSOT**
    
    - MEA e `config_paths.yaml` são as fontes canônicas para roteamento de artefatos e caminhos.
        
    - Proibido sobrescrever artefatos SSOT sem ordem explícita.
        

## 7. Decisões fechadas

- Nome do projeto: `BOLSA_2026_GEMINI`.
    
- Raiz do projeto no Drive: `a_bolsa2026_gemini/` (dentro do Shared Drive `BOLSA_2026`).
    
- Estrutura de diretórios formalizada e criada.
    
- `.gitignore`, MEA e `config_paths.yaml` criados e validados.
    
- `utils_paths.py` persistido conforme ORIENTAÇÃO #001, com correções de criação de diretório e testes de sanidade.
    

## 8. Validações registradas

- Drive montado (Shared Drives) e caminho raiz resolvido.
    
- Prévia do `utils_paths.py` exibida no dry-run.
    
- 5 chaves de caminho resolvidas em memória (`data_raw`, `data_processed`, `data_final`, `models`, `checkpoints`).
    
- Persistência idempotente realizada e import do módulo bem-sucedida.
    
- `ensure_dirs` executado e verificado sem falso negativo.
    

## 9. Pendências

- Nenhuma pendência técnica desta fase.
    
- Próximos registros devem seguir este formato de checkpoint nesta mesma pasta.
    

---

**Fim do Checkpoint 0001.**