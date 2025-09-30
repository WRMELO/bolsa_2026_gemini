
# Tomada de Decisão sobre Cálculo das Proporções de Neutro

A lógica de tomada de decisão deste projeto combina duas camadas complementares: uma camada estatística, que observa todo o universo de ativos de forma conjunta, e uma camada operacional, que aplica regras de compra e venda em cada ativo de forma individual.

O universo considerado é composto por 24 ativos. Dentro desse conjunto, entre 10 e 12 ativos são efetivamente mantidos na carteira, enquanto outros 12 a 14 permanecem em reserva, monitorados para uma possível entrada. Além disso, alguns ativos podem ser temporariamente colocados em quarentena, caso apresentem riscos específicos ou eventos excepcionais.

Na camada estatística, todos os 24 ativos são tratados em conjunto. Essa abordagem não significa que as decisões sejam tomadas como se houvesse um único ativo coletivo, mas sim que as probabilidades de alta, queda ou neutro são calculadas com a mesma régua. Essa padronização garante comparabilidade: a chance de queda de PETR4 pode ser interpretada de forma equivalente à chance de queda de VALE3, o que permite ranquear os ativos do mais ao menos promissor. Essa consistência facilita tanto o treinamento dos modelos quanto o processo de alocação de capital.

Na camada operacional, as decisões são sempre individuais, aplicadas a cada ativo. A regra central é clara: se um ativo que já está na carteira sinaliza queda, ele deve ser vendido compulsoriamente, independentemente do comportamento dos outros 23. A venda gera liquidez imediata e obrigatória. O dinheiro liberado não precisa ser reinvestido de forma imediata nem em um único ativo. Ele fica disponível para ser distribuído em qualquer proporção entre os ativos restantes que não estejam em quarentena, de acordo com o ranking global e os sinais positivos observados. Assim, a compra é opcional: só ocorre quando houver justificativa clara para alocação.

Esse arranjo permite lidar com eventos estruturais assimétricos. Se uma notícia negativa derruba um ativo específico enquanto outra positiva fortalece outro, o agregado dos 24 pode até sugerir tendência de alta, mas isso não impede que o ativo com sinal negativo seja vendido compulsoriamente. Ao mesmo tempo, o ativo fortalecido pode receber capital, desde que seu sinal seja consistente e a política de risco permita.

O papel da classe “neutro” nesse processo é o de representar a zona de indecisão. Ela é definida com base em cortes globais para assegurar comparabilidade entre ativos, mas não implica que todos passem o mesmo tempo em neutro. Ativos mais voláteis tendem a escapar dessa faixa com frequência maior, enquanto ativos mais estáveis permanecem mais tempo neutros. A uniformização é apenas uma convenção estatística; a decisão real continua sendo individual e adaptada ao comportamento de cada ativo.

Em síntese, o projeto opera com um motor duplo: o global, que fornece consistência estatística e régua comum para todos os ativos, e o individual, que aplica as regras de carteira. Vender compulsoriamente quando um ativo sinaliza mal e comprar opcionalmente apenas quando houver justificativa sólida assegura disciplina. Esse mecanismo organiza a circulação de capital entre ativos, sempre subordinado à premissa maior do projeto: a preservação vitalícia do capital.

---

Quer que eu já formate esse `.md` no estilo dos outros checkpoints (com cabeçalho, data e numeração), ou prefere manter como texto autônomo de tomada de decisão?
