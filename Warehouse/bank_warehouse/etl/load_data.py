import pandas as pd
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook


def load_data_to_snowflake(
    df: pd.DataFrame,
    database: str,
    schema: str,
    table: str,
):
    if df.empty:
        raise ValueError("Empty DataFrame")

    hook = SnowflakeHook(snowflake_conn_id="my_snowflake_conn")
    engine = hook.get_sqlalchemy_engine()

    df.to_sql(
        name=table,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        method="multi",
    )
