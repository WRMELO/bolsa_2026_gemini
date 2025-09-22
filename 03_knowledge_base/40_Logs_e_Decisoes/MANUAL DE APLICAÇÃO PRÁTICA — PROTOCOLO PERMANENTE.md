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
