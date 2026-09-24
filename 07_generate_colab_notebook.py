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
    pipeline = pipeline.replace(
        'if not DATA_PATH.exists():\n'
        '    DATA_PATH = Path(__file__).parent / "deliverable_fiap" / "data.csv"\n',
        '',
    )
    pipeline = pipeline.replace(
        'DATA_PATH = Path("data.csv")\n',
        '',
    )
    pipeline = pipeline.replace('from pathlib import Path\n\n', '')
    pipeline = pipeline.replace(
        'Pode receber o DataFrame retornado pelo Oracle ou ler o CSV para teste local.',
        'Recebe o DataFrame retornado pela consulta Oracle.',
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
            "Pergunta que guiou nosso trabalho: como priorizar clientes com maior chance de responder a uma campanha?\n\n"
            "O modelo descreve respostas históricas. Ele não mede o efeito causal de uma campanha.\n\n"
            "Execute as células nesta ordem. A senha Oracle nunca deve ser escrita no notebook."
        ),
        code(
            "!pip -q install numpy==2.4.4 pandas==3.0.2 scikit-learn==1.9.1 oracledb==3.3.0\n"
            "import getpass\n"
            "import oracledb\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt",
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
            "df.attrs['data_source'] = 'Oracle'\n"
            "print('shape:', df.shape)\n"
            "print('INCOME nulo:', int(df['INCOME'].isna().sum()))",
        ),
        code(pipeline),
        md(
            "## 2. EDA\n\n"
            "Antes de modelar, medimos o que pode afetar a decisão: quantos clientes responderam, onde faltam dados e quantos têm o mesmo perfil de preditores. "
            "A resposta é pouco frequente, então uma acurácia simples poderia esconder um modelo que quase nunca encontra quem responde. "
            "Calculamos a taxa global de RESPONSE, mas não comparamos resultados por perfil repetido antes da separação."
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
            "display(campaign_distribution)\n"
            "\n"
            "unique_profiles = int(profile_sizes.size)\n"
            "extra_profile_rows = int((profile_sizes - 1).clip(lower=0).sum())\n"
            "response_counts = y_eda.value_counts().reindex([0, 1], fill_value=0)\n"
            "fig, axes = plt.subplots(1, 2, figsize=(11, 4))\n"
            "colors = ['#6B7280', '#ED1165']\n"
            "bars = axes[0].bar(['Não respondeu', 'Respondeu'], response_counts.values, color=colors)\n"
            "axes[0].set_title('Resposta à campanha')\n"
            "axes[0].set_ylabel('Clientes')\n"
            "axes[0].set_ylim(0, max(response_counts.values) * 1.18)\n"
            "for bar, value in zip(bars, response_counts.values):\n"
            "    axes[0].text(bar.get_x() + bar.get_width()/2, value, f'{value:,}\\n{value/len(y_eda):.1%}', ha='center', va='bottom')\n"
            "bars = axes[1].bar(['Perfis distintos', 'Linhas excedentes'], [unique_profiles, extra_profile_rows], color=['#2D2D2D', '#ED1165'])\n"
            "axes[1].set_title('Repetição dos preditores')\n"
            "axes[1].set_ylabel('Registros')\n"
            "axes[1].set_ylim(0, unique_profiles * 1.18)\n"
            "for bar, value in zip(bars, [unique_profiles, extra_profile_rows]):\n"
            "    axes[1].text(bar.get_x() + bar.get_width()/2, value, f'{value:,}', ha='center', va='bottom')\n"
            "axes[1].text(0.5, -0.22, f'{int((profile_sizes > 1).sum())} perfis aparecem mais de uma vez', transform=axes[1].transAxes, ha='center')\n"
            "fig.tight_layout()\n"
            "plt.show()",
        ),
        md(
            "## 3. Feature Engineering\n\n"
            "AGE_AT_2014 aproxima a idade; TOTAL_CHILDREN resume a composição familiar; TOTAL_SPEND e TOTAL_PURCHASES medem valor e atividade de compra; "
            "CAMPAIGNS_ACCEPTED resume respostas a campanhas anteriores; WEB_PURCHASE_SHARE representa a preferência de canal; "
            "CUSTOMER_TENURE_DAYS mede o tempo de relacionamento. Essas variáveis resumem comportamento, valor e contexto familiar em sinais que uma equipe de produto consegue discutir. "
            "Nenhuma usa RESPONSE. Como os perfis idênticos em X poderiam inflar a avaliação, mantemos cada perfil inteiro no treino ou no teste.\n\n"
            "Nosso alvo é prever uma resposta observada no histórico, não provar que a campanha causou a compra. Por isso, trataríamos o score como uma forma de priorizar um teste de campanha, não como uma regra automática de envio.\n\n"
            "## 4. Comparação justa\n\n"
            "O holdout usa o primeiro fold de StratifiedGroupKFold com cinco partes, preservando aproximadamente 80/20 e a proporção de RESPONSE sem dividir perfis repetidos. "
            "A validação cruzada também é por grupos e ocorre somente no treino. Imputação e one-hot encoding ficam dentro do Pipeline. "
            "A árvore de referência e a árvore ajustada usam o mesmo teste reservado, para que a comparação seja direta."
        ),
        code(
            "metrics = run(df)\n"
            "metrics"
        ),
        md(
            "## 5. O que os resultados dizem\n\n"
            "ROC AUC resume o quanto a árvore consegue ordenar clientes que responderam acima dos que não responderam. Precision e Recall ajudam a discutir a quantidade e a qualidade dos contatos selecionados; F1 resume o equilíbrio entre os dois. "
            "Não esperamos que todas as métricas melhorem ao mesmo tempo. O limiar de decisão deve considerar capacidade de contato e custo de uma resposta perdida.\n\n"
            "Antes de usar o score em uma campanha real, definiríamos esse limiar e compararíamos um grupo de teste com um grupo de controle. Assim, separaríamos a previsão de resposta do efeito que a campanha realmente causou."
        ),
        code(
            "metric_columns = ['precision', 'recall', 'f1', 'roc_auc']\n"
            "metric_labels = {'precision': 'Precisão', 'recall': 'Recall', 'f1': 'F1', 'roc_auc': 'ROC AUC'}\n"
            "metric_names = {'reference': 'Referência', 'tuned': 'Ajustada'}\n"
            "plot_metrics = metrics.set_index('model')[metric_columns].rename(index=metric_names, columns=metric_labels)\n"
            "ax = plot_metrics.plot(kind='bar', figsize=(10, 5), color=['#6B7280', '#ED1165', '#F59E0B', '#2D2D2D'])\n"
            "ax.set_title('Árvores no mesmo teste reservado')\n"
            "ax.set_ylabel('Pontuação')\n"
            "ax.set_xlabel('')\n"
            "ax.set_ylim(0, 1)\n"
            "ax.legend(title='Métrica', ncol=2, loc='upper left')\n"
            "ax.grid(axis='y', alpha=0.2)\n"
            "plt.xticks(rotation=0)\n"
            "plt.tight_layout()\n"
            "plt.show()\n"
            "\n"
            "reference_auc = float(metrics.loc[metrics['model'] == 'reference', 'roc_auc'].iloc[0])\n"
            "tuned_auc = float(metrics.loc[metrics['model'] == 'tuned', 'roc_auc'].iloc[0])\n"
            "reference_precision = float(metrics.loc[metrics['model'] == 'reference', 'precision'].iloc[0])\n"
            "tuned_precision = float(metrics.loc[metrics['model'] == 'tuned', 'precision'].iloc[0])\n"
            "reference_recall = float(metrics.loc[metrics['model'] == 'reference', 'recall'].iloc[0])\n"
            "tuned_recall = float(metrics.loc[metrics['model'] == 'tuned', 'recall'].iloc[0])\n"
            "print(f'ROC AUC: {reference_auc:.4f} → {tuned_auc:.4f} ({tuned_auc-reference_auc:+.4f})')\n"
            "print(f'Precisão: {reference_precision:.4f} → {tuned_precision:.4f}; Recall: {reference_recall:.4f} → {tuned_recall:.4f}')"
        ),
        md(
            "## 6. Leitura para o negócio\n\n"
            "Uma árvore com melhor ROC AUC pode ordenar melhor os clientes para uma lista de teste, mas não prova que uma campanha aumentará compras. "
            "A decisão seguinte é escolher quantos clientes contatar e validar o resultado com um grupo de controle.\n\n"
            "Os resultados salvos devem vir da execução Oracle deste notebook. Não substitua essa execução pelas métricas de uma validação local."
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
