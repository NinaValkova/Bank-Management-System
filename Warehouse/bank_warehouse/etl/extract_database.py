import pandas as pd
from sqlalchemy import create_engine

MYSQL_URI = "mysql+mysqldb://root:nina2000@host.docker.internal:3306/bankdb"


def extract_table_from_mysql(table_name: str) -> pd.DataFrame:
    engine = create_engine(MYSQL_URI)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, engine)
    return df
