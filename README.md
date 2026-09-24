# FIAP CP4 | Case iFood

Entrega integrada de Cognitive Data Science e Machine Learning & Modelling.

## Grupo Perceptron

- Giovanni Henrique Pereira Hessel (RM 570574)
- Suellen Pereira da Silva (RM 573862)
- Arthur Zeferino (RM 570858)
- Israel Carneiro de Toledo (RM 573854)

## Pergunta que guiou o trabalho

Nosso objetivo é priorizar clientes com maior chance de responder a uma campanha. A árvore resume padrões históricos de resposta; ela não mede o efeito causal da campanha nem promete aumento de vendas. Usaríamos o score para montar um público de teste, definir um limite de contato e validar a campanha com um grupo de controle.

## Notebook

- Repositório GitHub: https://github.com/iskisraell/fiap-cp4-ifood-2026
- Abrir no Colab: https://colab.research.google.com/github/iskisraell/fiap-cp4-ifood-2026/blob/main/cp4.ipynb
- Notebook-fonte: cp4.ipynb
- Execução Oracle anterior, de 18/09: https://colab.research.google.com/drive/1fSOEgGY4zv_y6LArEs0ijIyTCsYpsqU0?usp=sharing
- Tabela: IFOOD_CUSTOMERS, com 2.240 registros e 29 colunas.

O notebook conduz da pergunta de negócio à consulta Oracle, mostra a EDA e as novas variáveis, explica a comparação justa das árvores e interpreta as métricas com gráficos. Os outputs Oracle da versão atual ainda precisam ser executados e salvos no Colab.

## EDA e separação

A EDA local encontrou 334 respostas positivas (14,91%), 24 valores ausentes em INCOME, nenhuma linha ou ID duplicado e 193 perfis de features repetidos. Os 201 registros excedentes desses perfis são mantidos juntos no holdout e nas dobras de validação.

O holdout por StratifiedGroupKFold tem 1.792 linhas de treino e 448 de teste, sem interseção de perfis. O teste fica fora do tuning. Imputação e one-hot encoding são ajustados dentro do Pipeline.

## Decision Tree e validação local

A referência usa DecisionTreeClassifier sem tuning, com os parâmetros padrão do scikit-learn e random_state=42. A busca ajusta criterion, max_depth, min_samples_leaf e class_weight usando validação cruzada por grupos somente no treino.

Resultados locais no CSV, com o holdout agrupado:

| Modelo | Precision | Recall | F1 | ROC AUC |
|---|---:|---:|---:|---:|
| Referência | 0,3651 | 0,3433 | 0,3538 | 0,6357 |
| Ajustado | 0,5000 | 0,3134 | 0,3853 | 0,7973 |

O ROC AUC aumentou 0,1616. Precision e F1 também subiram; o Recall caiu. Esses valores são da validação local por grupos. A execução Oracle de 18/09 usou split aleatório e não é comparável diretamente.

Essa troca importa para produto: a árvore ajustada ordenou melhor os clientes e trouxe maior precisão, mas deixou escapar mais respostas positivas. O ponto de corte depende da capacidade de contato e do custo de perder respostas. Como o alvo é histórico, qualquer uso em campanha precisa de um teste com controle para medir o efeito real.

## Arquivos

- 01_estrutura_ifood.sql: tabela, tipos, chave primária e constraints.
- 02_validacao_e_dml.sql: validações e demonstração de CREATE, ALTER, INSERT, UPDATE e DELETE.
- 03_query_dataframe.sql: consulta dos 29 campos de IFOOD_CUSTOMERS.
- 04_pipeline_ml.py: feature engineering, holdout agrupado, referência e tuning.
- 06_load_ifood_oracle.py e 08_execute_cp4_oracle.py: carga e validação Oracle.
- data.csv: base usada na validação local.
- presentation/CP4_iFood_Apresentacao.pptx: pitch de seis slides, com a pergunta de negócio, método e resultados.
- presentation/Roteiro_Apresentacao_CP4.md: fala sugerida para os quatro integrantes, com até dois tópicos por pessoa.
- presentation/output/ROTEIRO_APRESENTACAO_CP4_FIAP.pdf: roteiro formatado para apresentar.
- presentation/output/ROTEIRO_APRESENTACAO_CP4_FIAP.docx: versão editável do roteiro.

O segredo ORACLE_PASSWORD não está no notebook nem no repositório. Para a entrega final, execute a versão atual no Colab com Oracle e salve o notebook com as saídas. Um integrante envia um único PDF ou TXT na aba Trabalho do Teams até 25/09/2026 às 23:59.
