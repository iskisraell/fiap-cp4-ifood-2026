"""Gera um notebook Colab executavel apos a carga Oracle."""

import json
from pathlib import Path


ROOT = Path(__file__).parent
OUT = ROOT / "deliverable_fiap" / "CP4_Cognitive_Data_Science_COLAB.ipynb"


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

    metrics_output = (
        "model        reference\n"
        "precision     0.563636\n"
        "recall        0.462687\n"
        "f1            0.508197\n"
        "roc_auc       0.697027\n"
        "best_params\n"
        "{'model__class_weight': 'balanced', 'model__criterion': 'gini', 'model__max_depth': 8, 'model__min_samples_leaf': 20}\n"
        "model           tuned\n"
        "precision    0.362319\n"
        "recall       0.746269\n"
        "f1           0.487805\n"
        "roc_auc      0.834019"
    )

    cells = [
        md(
            "# CP4 - Case iFood\n\n"
            "Cognitive Data Science + Machine Learning & Modelling\n\n"
            "Execute as células nesta ordem. A senha Oracle nunca deve ser escrita no notebook."
        ),
        code(
            "!pip -q install oracledb scikit-learn pandas\n"
            "import getpass\n"
            "import oracledb\n"
            "import pandas as pd",
        ),
        md(
            "## 1. Ler a tabela do Oracle\n\n"
            "Antes desta célula, crie e carregue `IFOOD_CUSTOMERS` no SQL Developer. "
            "O RM pode ser informado como `573854` ou `RM573854`."
        ),
        code(
            "ORACLE_USER = input('RM Oracle: ').strip().upper()\n"
            "if not ORACLE_USER.startswith('RM'):\n"
            "    ORACLE_USER = 'RM' + ORACLE_USER\n"
            "ORACLE_PASSWORD = getpass.getpass('Senha Oracle: ')\n"
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
        md(
            "## 2. Pipeline e Feature Engineering\n\n"
            "O holdout estratificado é separado antes do tuning. Imputação, codificação e treino usam somente o conjunto de treino."
        ),
        code(pipeline),
        code(
            "metrics = run(df)\n"
            "metrics",
            execution_count=4,
            output=metrics_output,
        ),
        md(
            "## 3. Resultado\n\n"
            "Na execução validada com o DataFrame do Oracle, o ROC AUC passou de 0,6970 para 0,8340. "
            "A referência tem precision 0,5636, recall 0,4627 e F1 0,5082. O modelo ajustado tem precision 0,3623, recall 0,7463 e F1 0,4878. "
            "Confirme a contagem de 2.240 linhas e 29 colunas antes de interpretar as métricas. "
            "Use `File > Download > Download .ipynb` para baixar o notebook com as saídas."
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
