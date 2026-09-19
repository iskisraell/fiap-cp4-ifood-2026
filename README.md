# FIAP CP4 - Case iFood

Entrega integrada de Cognitive Data Science e Machine Learning & Modelling.

## Notebook

- [Notebook atualizado no Colab](https://colab.research.google.com/github/iskisraell/fiap-cp4-ifood-2026/blob/main/CP4_Cognitive_Data_Science_COLAB.ipynb)
- [Notebook compartilhado anteriormente](https://colab.research.google.com/drive/1fSOEgGY4zv_y6LArEs0ijIyTCsYpsqU0?usp=sharing)
- Tabela Oracle usada: `IFOOD_CUSTOMERS`
- Dataset: 2.240 registros e 29 colunas

Antes da conexão, no Colab abra `Secrets`, crie `ORACLE_PASSWORD`, informe a senha e ative o acesso para o notebook. Se o segredo não existir, a célula pede a senha sem exibi-la. A credencial não está no código.

## Conteudo

- `CP4_Cognitive_Data_Science_COLAB.ipynb`: notebook para leitura Oracle, EDA, feature engineering, holdout estratificado e tuning.
- `01_estrutura_ifood.sql`: tabela e constraints Oracle.
- `02_validacao_e_dml.sql`: validacoes e demonstracao controlada de DDL/DML.
- `03_query_dataframe.sql`: query do DataFrame.
- `04_pipeline_ml.py`: pipeline reproduzivel.
- `06_load_ifood_oracle.py`: carga do CSV sem salvar senha.
- `08_execute_cp4_oracle.py`: execucao integrada e validacao local Oracle.
- `data.csv`: base usada no trabalho.

## Resultado Oracle

- 2.240 registros carregados.
- 2.240 IDs distintos.
- 24 valores nulos em `INCOME`.
- DataFrame Oracle: `(2240, 29)`.
- ROC AUC de referencia: `0,6970`.
- ROC AUC ajustado: `0,8340`.

Nenhuma senha ou configuracao privada do Oracle faz parte deste repositorio.
