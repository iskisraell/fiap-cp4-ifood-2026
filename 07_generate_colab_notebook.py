"""Gera um notebook Colab executavel apos a carga Oracle."""

import json
from pathlib import Path


ROOT = Path(__file__).parent
OUTPUT_DIR = ROOT / "deliverable_fiap"
if not OUTPUT_DIR.exists():
    OUTPUT_DIR = ROOT
OUT = OUTPUT_DIR / "CP4_Cognitive_Data_Science_COLAB.ipynb"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text, execution_count=None, output=None):
    outputs = []
    if output is not None:
        outputs = [{"name": "stdout", "output_type": "stream", "text": output.splitlines(True)}]
    return {
        "cell_type": "code",
        "execution_count": execution_count,
        "metadata": {},
        "outputs": outputs,
        "source": text.splitlines(True),
    }


def main():
    pipeline = (ROOT / "04_pipeline_ml.py").read_text(encoding="utf-8")
    pipeline = pipeline.split('if __name__ == "__main__":')[0]
    pipeline = pipeline.replace(
        'DATA_PATH = Path(__file__).with_name("data.csv")',
        'DATA_PATH = Path("data.csv")',
    )

    query = """SELECT
    ID, YEAR_BIRTH, EDUCATION, MARITAL_STATUS, INCOME, KIDHOME, TEENHOME,
    DT_CUSTOMER, RECENCY, MNTWINES, MNTFRUITS, MNTMEATPRODUCTS,
    MNTFISHPRODUCTS, MNTSWEETPRODUCTS, MNTGOLDPRODS, NUMDEALSPURCHASES,
    NUMWEBPURCHASES, NUMCATALOGPURCHASES, NUMSTOREPURCHASES,
    NUMWEBVISITSMONTH, ACCEPTEDCMP3, ACCEPTEDCMP4, ACCEPTEDCMP5,
    ACCEPTEDCMP1, ACCEPTEDCMP2, COMPLAIN, Z_COSTCONTACT, Z_REVENUE, RESPONSE
FROM IFOOD_CUSTOMERS
ORDER BY ID"""

    cells = [
        md(
            "# CP4 - Case iFood\n\n"
            "Cognitive Data Science + Machine Learning & Modelling\n\n"
            "Grupo Perceptron, sala 1TIAPZ-2026.\n\n"
            "Execute as células nesta ordem. A senha Oracle nunca deve ser escrita no notebook."
        ),
        code(
            "!pip -q install numpy==2.4.4 pandas==3.0.2 scikit-learn==1.9.1 oracledb==3.3.0\n"
            "import getpass\n"
            "import oracledb\n"
            "import pandas as pd",
        ),
        md(
            "## 1. Ler a tabela do Oracle\n\n"
            "Antes desta célula, crie e carregue `IFOOD_CUSTOMERS` no SQL Developer. "
            "No Colab, abra o painel de chave `Secrets`, crie `ORACLE_PASSWORD`, informe a senha e ative o acesso para este notebook. "
            "Se o segredo não estiver configurado, a célula solicitará a senha sem exibi-la."
        ),
        code(
            "ORACLE_USER = 'RM573854'\n"
            "try:\n"
            "    from google.colab import userdata\n"
            "    ORACLE_PASSWORD = userdata.get('ORACLE_PASSWORD')\n"
            "except Exception:\n"
            "    ORACLE_PASSWORD = None\n"
            "if not ORACLE_PASSWORD:\n"
            "    ORACLE_PASSWORD = getpass.getpass('Senha Oracle (não exibida): ')\n"
            "ORACLE_DSN = oracledb.makedsn('oracle.fiap.com.br', 1521, service_name='orcl')\n\n"
            f"SQL = '''{query}'''\n\n"
            "with oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN) as connection:\n"
            "    with connection.cursor() as cursor:\n"
            "        cursor.execute(SQL)\n"
            "        columns = [item[0] for item in cursor.description]\n"
            "        df = pd.DataFrame(cursor.fetchall(), columns=columns)\n\n"
            "print('shape:', df.shape)\n"
            "print('INCOME nulo:', int(df['INCOME'].isna().sum()))",
        ),
        code(pipeline),
        md(
            "## 2. EDA\n\n"
            "A análise verifica o desbalanceamento do alvo, valores ausentes, duplicidades e perfis de features repetidos. "
            "A taxa global de RESPONSE descreve o desbalanceamento; não comparamos o alvo por grupo antes do holdout."
        ),
        code(
            "eda = df.copy()\n"
            "eda.columns = [str(column).upper() for column in eda.columns]\n"
            "source_columns = len(eda.columns)\n"
            "X_eda, y_eda, groups_eda = build_features(eda)\n"
            "profile_sizes = pd.Series(groups_eda).value_counts()\n"
            "positive = int(y_eda.sum())\n"
            "summary = pd.DataFrame({\n"
            "    'Indicador': ['Linhas', 'Colunas da query', 'Resposta positiva', 'INCOME nulo', 'Linhas completas duplicadas', 'IDs duplicados', 'Perfis de features repetidos', 'Linhas excedentes nesses perfis'],\n"
            "    'Resultado': [\n"
            "        len(eda), source_columns, f'{positive} ({positive / len(eda):.2%})',\n"
            "        int(eda['INCOME'].isna().sum()), int(eda.duplicated().sum()), int(eda['ID'].duplicated().sum()),\n"
            "        int((profile_sizes > 1).sum()), int((profile_sizes - 1).clip(lower=0).sum())\n"
            "    ],\n"
            "})\n"
            "display(summary)\n"
            "campaign_distribution = (\n"
            "    X_eda['CAMPAIGNS_ACCEPTED'].value_counts().sort_index()\n"
            "    .rename_axis('CAMPAIGNS_ACCEPTED').reset_index(name='CLIENTES')\n"
            ")\n"
            "display(campaign_distribution)",
        ),
        md(
            "## 3. Feature Engineering\n\n"
            "AGE_AT_2014 aproxima a idade; TOTAL_CHILDREN resume a composição familiar; TOTAL_SPEND e TOTAL_PURCHASES medem valor e atividade de compra; "
            "CAMPAIGNS_ACCEPTED resume respostas a campanhas anteriores; WEB_PURCHASE_SHARE representa a preferência de canal; "
            "CUSTOMER_TENURE_DAYS mede o tempo de relacionamento. Nenhuma dessas variáveis usa RESPONSE. Perfis idênticos em X são agrupados para que nunca apareçam ao mesmo tempo no treino e no teste.\n\n"
            "## 4. Preparação e tuning\n\n"
            "O holdout usa o primeiro fold de StratifiedGroupKFold com cinco partes, preservando aproximadamente 80/20 e a proporção de RESPONSE sem dividir perfis repetidos. "
            "A validação cruzada também é por grupos e ocorre somente no treino. Imputação e one-hot encoding ficam dentro do Pipeline."
        ),
        code(
            "metrics = run(df)\n"
            "metrics"
        ),
        md(
            "## 5. Resultado\n\n"
            "Compare precision, recall, F1 e ROC AUC no holdout reservado. Discuta os quatro indicadores; ROC AUC maior não implica que precision, recall e F1 também aumentem. "
            "Execute todas as células no Colab e salve o notebook com as saídas antes de publicar a versão executada."
        ),
    ]
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
            "colab": {"name": "CP4_Cognitive_Data_Science_COLAB.ipynb"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    OUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
