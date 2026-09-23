# FIAP CP4 | Case iFood

Entrega integrada de Cognitive Data Science e Machine Learning & Modelling.

## Grupo Perceptron

- Giovanni Henrique Pereira Hessel (RM 570574)
- Suellen Pereira da Silva (RM 573862)
- Arthur Zeferino (RM 570858)
- Israel Carneiro de Toledo (RM 573854)

## Notebook

- Abrir no Colab: https://colab.research.google.com/github/iskisraell/fiap-cp4-ifood-2026/blob/main/cp4.ipynb
- Notebook-fonte: cp4.ipynb
- Execução Oracle anterior, de 18/09: https://colab.research.google.com/drive/1fSOEgGY4zv_y6LArEs0ijIyTCsYpsqU0?usp=sharing
- Tabela: IFOOD_CUSTOMERS, com 2.240 registros e 29 colunas.

O notebook contém a query Oracle, a EDA, as justificativas das features e o pipeline de modelagem. Os outputs da versão atual ainda precisam ser executados e salvos no Colab.

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

## Arquivos

- 01_estrutura_ifood.sql: tabela, tipos, chave primária e constraints.
- 02_validacao_e_dml.sql: validações e demonstração de CREATE, ALTER, INSERT, UPDATE e DELETE.
- 03_query_dataframe.sql: consulta dos 29 campos de IFOOD_CUSTOMERS.
- 04_pipeline_ml.py: feature engineering, holdout agrupado, referência e tuning.
- 06_load_ifood_oracle.py e 08_execute_cp4_oracle.py: carga e validação Oracle.
- data.csv: base usada na validação local.

O segredo ORACLE_PASSWORD não está no notebook nem no repositório. Para a entrega final, execute a versão atual no Colab com Oracle e salve o notebook com as saídas. Um integrante envia um único PDF ou TXT na aba Trabalho do Teams até 25/09/2026 às 23:59.
