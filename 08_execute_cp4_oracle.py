"""Executa a Parte 1 do CP4 no schema Oracle do usuario.

Uso seguro:
    python 08_execute_cp4_oracle.py --reset-target

O reset remove somente IFOOD_CUSTOMERS e suas constraints. A senha e lida
com getpass e nunca e salva em arquivo.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
from datetime import datetime
from getpass import getpass
from pathlib import Path

import oracledb
import pandas as pd


BASE = Path(__file__).resolve().parent
SOURCE = Path(__file__).with_name("data.csv")
if not SOURCE.exists():
    SOURCE = Path(r"C:\Users\israel.toledo\Downloads\data.csv")
TARGET = "IFOOD_CUSTOMERS"
COLUMNS = [
    "ID", "YEAR_BIRTH", "EDUCATION", "MARITAL_STATUS", "INCOME", "KIDHOME",
    "TEENHOME", "DT_CUSTOMER", "RECENCY", "MNTWINES", "MNTFRUITS",
    "MNTMEATPRODUCTS", "MNTFISHPRODUCTS", "MNTSWEETPRODUCTS", "MNTGOLDPRODS",
    "NUMDEALSPURCHASES", "NUMWEBPURCHASES", "NUMCATALOGPURCHASES",
    "NUMSTOREPURCHASES", "NUMWEBVISITSMONTH", "ACCEPTEDCMP3", "ACCEPTEDCMP4",
    "ACCEPTEDCMP5", "ACCEPTEDCMP1", "ACCEPTEDCMP2", "COMPLAIN",
    "Z_COSTCONTACT", "Z_REVENUE", "RESPONSE",
]
SELECT_SQL = f"SELECT {', '.join(COLUMNS)} FROM {TARGET} ORDER BY ID"
INSERT_SQL = (
    f"INSERT INTO {TARGET} ({', '.join(COLUMNS)}) "
    f"VALUES ({', '.join(f':{i + 1}' for i in range(len(COLUMNS)))})"
)


def split_sql_script(text: str) -> list[str]:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"--[^\r\n]*", "", text)
    return [part.strip() for part in text.split(";") if part.strip()]


def connect(username: str, password: str):
    dsns = [
        ("SID=ORCL", oracledb.makedsn("oracle.fiap.com.br", 1521, sid="ORCL")),
        ("SERVICE_NAME=orcl", oracledb.makedsn("oracle.fiap.com.br", 1521, service_name="orcl")),
    ]
    errors = []
    for label, dsn in dsns:
        try:
            return oracledb.connect(user=username, password=password, dsn=dsn), label
        except oracledb.Error as exc:
            errors.append(f"{label}: {exc}")
    raise RuntimeError("Nao foi possivel conectar ao Oracle: " + " | ".join(errors))


def scalar(cursor, sql: str):
    cursor.execute(sql)
    return cursor.fetchone()[0]


def value_or_none(value):
    return None if pd.isna(value) else value


def load_csv(cursor, connection) -> int:
    data = pd.read_csv(SOURCE)
    data.columns = [str(column).upper() for column in data.columns]
    data["DT_CUSTOMER"] = pd.to_datetime(data["DT_CUSTOMER"], errors="raise")
    rows = []
    date_index = COLUMNS.index("DT_CUSTOMER")
    for record in data[COLUMNS].itertuples(index=False, name=None):
        row = [value_or_none(value) for value in record]
        row[date_index] = row[date_index].to_pydatetime()
        rows.append(tuple(row))
    cursor.executemany(INSERT_SQL, rows)
    connection.commit()
    return len(rows)


def run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    path = BASE / "04_pipeline_ml.py"
    spec = importlib.util.spec_from_file_location("cp4_pipeline", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Nao foi possivel carregar {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run(df)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reset-target",
        action="store_true",
        help="Remove e recria somente IFOOD_CUSTOMERS antes da carga",
    )
    args = parser.parse_args()

    username = input("RM Oracle: ").strip().upper()
    if not username.startswith("RM"):
        username = "RM" + username
    password = getpass("Senha Oracle: ")
    connection, dsn_label = connect(username, password)
    evidence = [f"executado_em={datetime.now().isoformat(timespec='seconds')}", f"dsn={dsn_label}"]

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT USER, SYS_CONTEXT('USERENV','SERVICE_NAME'), "
                "SYS_CONTEXT('USERENV','DB_NAME') FROM DUAL"
            )
            current_user, service_name, db_name = cursor.fetchone()
            print(f"Usuario conectado: {current_user}")
            print(f"Servico: {service_name} | Banco: {db_name}")
            evidence.extend([
                f"usuario={current_user}",
                f"servico={service_name}",
                f"banco={db_name}",
            ])

            cursor.execute(
                "SELECT COUNT(*) FROM ALL_OBJECTS "
                "WHERE OWNER = USER AND OBJECT_NAME = 'IFOOD_CUSTOMERS' "
                "AND OBJECT_TYPE = 'TABLE'"
            )
            exists = cursor.fetchone()[0] == 1
            if exists and args.reset_target:
                print("Removendo somente IFOOD_CUSTOMERS...")
                cursor.execute("DROP TABLE IFOOD_CUSTOMERS CASCADE CONSTRAINTS PURGE")
                exists = False
            if exists:
                count = scalar(cursor, "SELECT COUNT(*) FROM IFOOD_CUSTOMERS")
                if count:
                    raise RuntimeError(
                        f"IFOOD_CUSTOMERS ja possui {count} registros. "
                        "Use --reset-target somente se quiser recriar a tabela."
                    )

            if not exists:
                ddl = (BASE / "01_estrutura_ifood.sql").read_text(encoding="utf-8")
                for statement in split_sql_script(ddl):
                    cursor.execute(statement)
                print("Tabela e constraints criadas.")

            inserted = load_csv(cursor, connection)
            total = scalar(cursor, "SELECT COUNT(*) FROM IFOOD_CUSTOMERS")
            distinct_ids = scalar(cursor, "SELECT COUNT(DISTINCT ID) FROM IFOOD_CUSTOMERS")
            income_null = scalar(cursor, "SELECT COUNT(*) FROM IFOOD_CUSTOMERS WHERE INCOME IS NULL")
            response = dict(cursor.execute(
                "SELECT RESPONSE, COUNT(*) FROM IFOOD_CUSTOMERS GROUP BY RESPONSE"
            ).fetchall())
            print(f"Registros inseridos: {inserted}")
            print(f"Total: {total} | IDs distintos: {distinct_ids} | Income nulo: {income_null}")
            print(f"Response: {response}")
            evidence.extend([
                f"inseridos={inserted}",
                f"total={total}",
                f"ids_distintos={distinct_ids}",
                f"income_nulo={income_null}",
                f"response={response}",
            ])

            demo = "IFOOD_CP4_DML_DEMO"
            cursor.execute(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {demo} PURGE'; EXCEPTION WHEN OTHERS THEN NULL; END;")
            cursor.execute(f"CREATE TABLE {demo} (DEMO_ID NUMBER(6) NOT NULL, LABEL VARCHAR2(40) NOT NULL, AMOUNT NUMBER(10,2))")
            cursor.execute(f"ALTER TABLE {demo} ADD CONSTRAINT {demo}_PK PRIMARY KEY (DEMO_ID)")
            cursor.execute(f"INSERT INTO {demo} (DEMO_ID, LABEL, AMOUNT) VALUES (1, 'registro de teste', 100)")
            cursor.execute(f"UPDATE {demo} SET AMOUNT = AMOUNT + 25 WHERE DEMO_ID = 1")
            cursor.execute(f"DELETE FROM {demo} WHERE DEMO_ID = 1")
            connection.commit()
            cursor.execute(f"DROP TABLE {demo} PURGE")
            connection.commit()
            print("CREATE/ALTER/INSERT/UPDATE/DELETE demonstrados em tabela isolada.")

            cursor.execute(SELECT_SQL)
            df = pd.DataFrame(cursor.fetchall(), columns=[item[0] for item in cursor.description])
            print(f"DataFrame Oracle: {df.shape}")
            metrics = run_pipeline(df)
            metrics_path = BASE / "deliverable_fiap" / "metrics_oracle.csv"
            metrics.to_csv(metrics_path, index=False)
            evidence.append(f"dataframe_shape={df.shape}")
            evidence.append(f"metrics_oracle={metrics.to_dict(orient='records')}")
            evidence_path = BASE / "deliverable_fiap" / "oracle_validation.txt"
            evidence_path.write_text("\n".join(evidence) + "\n", encoding="utf-8")
            print(f"Metricas Oracle: {metrics_path}")
            print(f"Evidencia Oracle: {evidence_path}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
