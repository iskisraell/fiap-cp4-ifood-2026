"""Carga segura do CSV na tabela IFOOD_CUSTOMERS.

Uso:
    python 06_load_ifood_oracle.py

O script nao salva a senha e nao apaga a tabela. Para uma recarga limpa,
execute TRUNCATE TABLE manualmente no SQL Developer somente depois de
confirmar que a tabela pertence ao seu usuario.
"""

from getpass import getpass
from pathlib import Path

import oracledb
import pandas as pd


SOURCE = Path(__file__).with_name("data.csv")
if not SOURCE.exists():
    SOURCE = Path(r"C:\Users\israel.toledo\Downloads\data.csv")
COLUMNS = [
    "ID", "YEAR_BIRTH", "EDUCATION", "MARITAL_STATUS", "INCOME", "KIDHOME",
    "TEENHOME", "DT_CUSTOMER", "RECENCY", "MNTWINES", "MNTFRUITS",
    "MNTMEATPRODUCTS", "MNTFISHPRODUCTS", "MNTSWEETPRODUCTS", "MNTGOLDPRODS",
    "NUMDEALSPURCHASES", "NUMWEBPURCHASES", "NUMCATALOGPURCHASES",
    "NUMSTOREPURCHASES", "NUMWEBVISITSMONTH", "ACCEPTEDCMP3", "ACCEPTEDCMP4",
    "ACCEPTEDCMP5", "ACCEPTEDCMP1", "ACCEPTEDCMP2", "COMPLAIN",
    "Z_COSTCONTACT", "Z_REVENUE", "RESPONSE",
]
PLACEHOLDERS = ", ".join(f":{index + 1}" for index in range(len(COLUMNS)))
INSERT_SQL = f"INSERT INTO IFOOD_CUSTOMERS ({', '.join(COLUMNS)}) VALUES ({PLACEHOLDERS})"


def value_or_none(value):
    return None if pd.isna(value) else value


def main():
    username = input("RM Oracle: ").strip()
    password = getpass("Senha Oracle: ")
    dsn = oracledb.makedsn("oracle.fiap.com.br", 1521, service_name="orcl")
    data = pd.read_csv(SOURCE)
    data.columns = [str(column).upper() for column in data.columns]
    data["DT_CUSTOMER"] = pd.to_datetime(data["DT_CUSTOMER"], errors="raise")

    rows = []
    for record in data[COLUMNS].itertuples(index=False, name=None):
        row = [value_or_none(value) for value in record]
        date_index = COLUMNS.index("DT_CUSTOMER")
        row[date_index] = row[date_index].to_pydatetime()
        rows.append(tuple(row))

    with oracledb.connect(user=username, password=password, dsn=dsn) as connection:
        with connection.cursor() as cursor:
            cursor.executemany(INSERT_SQL, rows)
            connection.commit()
            cursor.execute("SELECT COUNT(*) FROM IFOOD_CUSTOMERS")
            count = cursor.fetchone()[0]
    print(f"Registros inseridos nesta execucao: {len(rows)}")
    print(f"Total atual em IFOOD_CUSTOMERS: {count}")


if __name__ == "__main__":
    main()
