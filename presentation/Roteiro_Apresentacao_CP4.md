# Roteiro da apresentação | CP4 Case iFood

**Grupo Perceptron · 1TIAPZ-2026 · aproximadamente 4 minutos**

Esta é uma divisão sugerida para cada integrante apresentar de um a dois tópicos. O texto está escrito para ser dito em voz alta; usem as ideias, sem decorar cada frase.

## Slide 1 — Israel: pergunta e objetivo

“Nós começamos com uma pergunta de negócio: entre tantos clientes, quem tem maior chance de responder a uma campanha? A ideia é organizar melhor um teste de público. O modelo prevê respostas parecidas com as que vimos no histórico; ele não prova que a campanha causou a compra.”

## Slide 2 — Giovanni: o que os dados mostram

“Na base, 334 de 2.240 clientes aceitaram a campanha observada, cerca de 15%. Essa resposta é registrada na coluna RESPONSE. Também encontramos 193 perfis de preditores que se repetem, somando 201 registros além da primeira ocorrência. Como a resposta positiva é bem menos comum, olhar só a taxa geral de acerto poderia esconder um modelo que não encontra quase ninguém que responde.”

## Slide 3 — Suellen: do Oracle à análise

“Na parte de dados, criamos a tabela IFOOD_CUSTOMERS, definimos tipos e restrições e carregamos os registros do CSV. Em 18 de setembro, conferimos 2.240 linhas, 2.240 IDs distintos e a consulta Oracle com 29 campos. Demonstramos CREATE, ALTER, INSERT, UPDATE e DELETE em uma tabela separada, para não alterar a base principal. A modelagem agrupada atual ainda precisa ser executada com esse DataFrame Oracle.”

## Slide 4 — Suellen: variáveis que ajudam a contar a história

“Também criamos variáveis mais fáceis de interpretar. Juntamos gastos e compras, resumimos o número de campanhas aceitas e calculamos idade aproximada, composição familiar, participação de compras pela web e tempo de relacionamento. Essas variáveis ajudam a descrever o cliente sem usar a resposta que queremos prever.”

## Slide 5 — Arthur: comparação sem vazamento

“Para comparar as árvores com justiça, reservamos um teste estratificado de 20% antes de ajustar os parâmetros. Mantivemos a proporção de respostas e os perfis iguais do mesmo lado. No treino, fizemos cinco dobras mantendo a proporção de respostas, escolhemos a configuração pela ROC AUC e ajustamos critério, profundidade, mínimo de clientes por folha e peso de classe. A imputação e as categorias também são ajustadas só dentro do treino.”

## Slide 6 — Israel: resultado e próximo passo

“Na validação local agrupada, a ROC AUC, que indica se quem respondeu fica acima de quem não respondeu no ranking, foi de 0,6357 na referência e 0,7973 na árvore ajustada. A precisão passou de 0,3651 para 0,5000, enquanto o recall caiu de 0,3433 para 0,3134. Isso mostra uma troca: a árvore ajustada ordenou melhor e aumentou a precisão, mas encontrou menos dos clientes que responderam. Como próximo passo de produto, escolheríamos o limite de contato e testaríamos a campanha contra um grupo de controle. Esses números ainda são da validação local com o CSV; precisamos salvar a execução agrupada usando o DataFrame Oracle.”

## Passagem para o notebook

“Agora vamos abrir o notebook e mostrar a consulta, a separação do teste e a comparação das métricas.”
