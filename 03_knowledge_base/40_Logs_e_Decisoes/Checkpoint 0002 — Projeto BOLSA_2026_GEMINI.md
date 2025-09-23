Perfeito. Aqui está o **Checkpoint 0002**, em formato Markdown, consolidando tudo que discutimos até agora sobre os **planos, protocolos e ajustes**.

---

# 📌 Checkpoint 0002 — Projeto BOLSA_2026_GEMINI

**Data:** 2025-09-22

## 1. Situação Atual

- O projeto migrou de execução local (VSCode/Jupyter) para o **ambiente Google (Colab + Gemini + Drive)**.
    
- O **Agente** foi atualizado para **Gemini 2.5 Flash**.
    
- O fluxo **Owner ↔ Estrategista ↔ Agente** segue o **PROTOCOLO PERMANENTE** e o **MANUAL DE APLICAÇÃO PRÁTICA**.
    

## 2. Papéis Reforçados

- **Owner:** define objetivos, cola instruções, executa, traz resultados.
    
- **Estrategista (GPT-5):** formula **instruções claras e completas**, nunca gera código.
    
- **Agente (Gemini):** devolve apenas **um bloco de código auto-contido**, executa regras frias, sem improvisos.
    

## 3. Avanços e Decisões

1. **Universo inicial de ativos (24 tickers)** foi consolidado, balanceado por setor.
    
    - Inclui financeiro, materiais, energia, utilities, saúde, consumo, indústria, tecnologia e transporte.
        
    - Regra fixa: `RDOR3.SA` sempre `DROP` (<5 anos de histórico).
        
2. **Índice âncora:** `^BVSP` (Ibovespa).
    
3. **Macros candidatas:** `EWZ, ^GSPC, ^VIX, DX-Y.NYB, ^TNX, BZ=F`.
    
    - Fallback automático: `BZ=F → CL=F`, registrar `alias="WTI_fallback_for_Brent"`.
        
4. **Regras de elegibilidade:**
    
    - Histórico ≥ 5 anos.
        
    - ADTV monetário (252 pregões) ≥ percentil 70 do universo.
        
    - “Um por emissor”: manter o de maior liquidez.
        
    - Manutenção: marcar substituição se **2 trimestres consecutivos** abaixo do corte.
        
5. **Anti-ambiguidade (Series pandas):**
    
    - **Nunca** usar `if <Series/DataFrame>`.
        
    - **Sempre** reduzir a escalar (`.any()`, `.all()`, `.empty`, `float()`).
        
    - Casting obrigatório para `float` antes de usar `np.isfinite`.
        
6. **Execução separada:**
    
    - **Ingesta:** download e métricas (sem decisões).
        
    - **Seleção:** aplicar critérios fora da ingesta.
        
7. **dry_run:**
    
    - Primeira execução sempre com `dry_run=True`.
        
    - Persistência só após GO explícito.
        

## 4. Problemas Identificados

- **Erro recorrente:** “truth value of a Series is ambiguous” → causado por falta de casting escalar.
    
- **Solução definida:** sempre extrair último valor (`iloc[-1]`, `ravel()[-1]`), converter em `float`, só então aplicar regras.
    
- **Outro problema:** Agente narrando em vez de só devolver código.
    
    - Ordem reforçada: **único bloco de código Python**, sem narrativa.
        
- **Pacote ausente (`yfinance`)** → resolvido via **bootstrap automático** (`pip install` no próprio código).
    

## 5. Ajustes no Protocolo

- Inclusão da cláusula **“Ambiguity kill + DÚVIDA_BLOQUEANTE automática”**:
    
    - Varredura preventiva no notebook para eliminar `if Series`.
        
    - Se erro persistir → Agente deve parar e emitir `DÚVIDA_BLOQUEANTE` com linha, contexto, intenção e proposta.
        

## 6. Próximos Passos

1. Executar ORIENTAÇÃO #U0R no Gemini 2.5 Flash para validar `dry_run=True`.
    
2. Receber relatórios (`df_status_symbols`, `df_eligibility`, `df_maintenance`, `df_sector_summary`, `df_macros`, `manifesto_universe_v1`).
    
3. Se tudo correto → checkpoint com GO e emissão da instrução para `dry_run=False` (persistência em arquivos padronizados).
    

---

✅ **Decisão deste checkpoint:** manter a disciplina rígida do protocolo, reforçar casting escalar e bootstrap de pacotes. Avançaremos em novo chat com a instrução limpa para o Agente 2.5 Flash.

---

