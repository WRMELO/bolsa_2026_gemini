# Manual de Aplicação Prática

## Owner ↔ Estrategista ↔ Agente

Este manual mostra como aplicar o protocolo no dia a dia, em forma de checklist operacional.  
Deve ser usado como guia rápido em todos os projetos.

---

## 1. Fluxo de Interação

1. **Owner** define o objetivo ou problema.  
2. **Estrategista** (ChatGPT) transforma em instrução clara e padronizada.  
3. **Owner** copia/cola a instrução no **Agente** (Copilot).  
4. **Agente** devolve **um único bloco de código auto-contido**.  
5. **Owner** executa o código em seu ambiente (ex.: Jupyter/VS Code).  
6. **Owner** traz o resultado de volta ao Estrategista.  
7. **Estrategista** valida → se correto, avança; se errado, reorienta.  

---

## 2. Regras Fixas

- Owner nunca pede código direto ao Agente.  
- Estrategista nunca gera código executável.  
- Agente nunca muda requisitos nem improvisa.  
- Primeira execução sempre em **dry_run=True**.  
- Persistência só ocorre com autorização explícita.  

---

## 3. O que cada papel faz

- **Owner**: define objetivos, cola instruções no Agente, executa código, retorna resultados.  
- **Estrategista**: planeja, define regras, valida outputs, gera instruções padronizadas.  
- **Agente**: escreve apenas código auto-contido, devolve logs/resultados conforme checklist.  

---

## 4. Critérios de Escalonamento

- Se erro se repetir **duas vezes seguidas** → Agente deve parar e formular dúvidas ao Estrategista.  
- Se Owner for exposto a tentativa/erro técnico → registrar como falha grave de protocolo.  
- Se Estrategista emitir instrução ambígua → corrigir imediatamente e registrar.  

---

## 5. Checkpoint Obrigatório

Ao final de cada etapa, registrar:  

- Objetivo da etapa  
- Resultado obtido  
- Falhas encontradas  
- Decisão tomada (Go/NoGo)  
- Próxima ação  

---

## 6. Onde guardar

- Este manual deve acompanhar o **PROTOCOLO PERMANENTE**.  
- Recomendado:  
  - Arquivo `MANUAL_APLICACAO_PRATICA.md` em `/docs/` ou na raiz do projeto.  
  - Também colado no Obsidian, junto ao protocolo principal.  

---

## 7. Resumo em 3 linhas (lembrança rápida)

- **Owner → Estrategista → Agente → Owner** (ciclo fechado).  
- **dry_run primeiro, persistência só autorizada.**  
- **Erro repetido duas vezes → escalonamento obrigatório.**  


# 8.Emenda ao protocolo (imediata)

1. **Full traceback sempre**: quando der exceção, o Agente **deve imprimir o traceback completo** (arquivo, linha, código) antes de qualquer mensagem normativa.
    
2. **DÚVIDA_BLOQUEANTE automática**: se a exceção for “truth value of a Series is ambiguous”, o Agente **deve parar** e emitir um bloco de texto estruturado com:
    
    - `linha_exata:` (código fonte daquela linha)
        
    - `contexto:` (3 linhas antes/depois)
        
    - `intenção:` _(algum verdadeiro / todos verdadeiros / checagem de vazio)_
        
    - `proposta:` _(usar .any() / .all() / .empty / 'col' in df.columns etc.)_
        
3. **Ambiguity kill pre-flight**: antes de rodar o pipeline, o Agente **deve fazer uma varredura no próprio notebook** pelos padrões de risco (`if df:`, `if df['...']`, `if (df['...'] == ...)`, `if series:`) e **trocar por versões escalares**.
    
4. **Porta de saída**: se após a varredura o erro persistir, **não prossegue**: abre DÚVIDA_BLOQUEANTE e aguarda decisão. (Conforme escalonamento: erro repetido → parar e perguntar.)
   
   ### A. Regra Zero (obrigatória em toda resposta/célula)

- A **primeira linha** de **toda** resposta do Estrategista e da **primeira célula** do Agente deve ser:  
    `One-step discipline (HF-000) ON`.
    
- O Agente deve **ecoar** no topo do bloco: `ACK HEURISTICS: HF000=ON | GapFill=OFF | ContextCarry=OFF | Narrative=OFF | StructRetain=OFF | SpeedOpt=OFF`.
    

### B. SSOT e caminhos

- O Estrategista **nunca** supõe arquivo/caminho. Se o insumo não estiver apontado no SSOT, ordenar ao Agente: **parar** e abrir **DÚVIDA_BLOQUEANTE**.
    
- Para Google Drive Compartilhado: o Agente **sempre** monta e usa o prefixo `/content/drive/Shareddrives/...`; é **proibido** “adivinhar” caminhos alternativos.
    

### C. Verbosidade e modo de execução

- **VERBOSITY=QUIET** por padrão nos passos “RAM-only”: nenhum print/relatório, salvo ordem explícita.
    
- **VERBOSITY=REPORT** apenas quando o protocolo exigir logs mínimos do Manual.
    

### D. Anti-ambiguidade pandas (pre-flight mandatório)

- Antes de executar, o Agente varre o próprio bloco e **substitui** padrões ambíguos (`if df:`, `if series:` etc.) por checagens escalares (`.empty`, `.any()`, `.all()`, `pd.notna()`).
    
- Se ainda disparar “truth value of a Series is ambiguous” → **parar no 1º evento** e emitir **DÚVIDA_BLOQUEANTE** com `linha_exata/contexto/intenção/proposta`.
    

### E. Bootstrap, fallback e robustez de rede

- `pip install yfinance` no topo; 3 tentativas com backoff simples para downloads.
    
- Macros: **fallback obrigatório** `BZ=F → CL=F`; o Agente retorna a lista `macros_utilizadas`.
    

### F. Fronteiras de papel e forma de entrega

- Estrategista **nunca** entrega código; apenas instruções claras, checklist e critérios de bloqueio.
    
- Agente **sempre** entrega **um bloco único** de código, sem narrativa fora do bloco, confirmando heurísticas no topo.
    

### G. Escalonamento e porta de saída

- **Erro idêntico repetido 2x** → Agente **para** e abre **DÚVIDA_BLOQUEANTE**.
    
- **Ambiguidade de requisito** → Estrategista corrige a instrução e registra ajuste.