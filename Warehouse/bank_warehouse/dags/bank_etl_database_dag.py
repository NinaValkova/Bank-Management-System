from typing import Any
from airflow.decorators import dag, task
from pendulum import datetime
import pandas as pd

from etl.extract_database import extract_table_from_mysql
from etl.load_data import load_data_to_snowflake
from etl.transform_database import (
    transform_database_accounts,
    transform_database_guests,
    transform_database_users,
    transform_database_dispositions,
    transform_database_transactions,
)


@dag(
    dag_id="bank_etl_database_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bank", "database"],
)
def bank_etl_database_dag():

    @task()
    def extract(table_name: str) -> Any:
        df = extract_table_from_mysql(table_name)
        return df.to_json(orient="split", date_format="iso")

    @task()
    def transform_accounts(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_database_accounts(df).to_json(
            orient="split", date_format="iso"
        )

    @task()
    def transform_guests(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_database_guests(df).to_json(orient="split", date_format="iso")

    @task()
    def transform_users(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_database_users(df).to_json(orient="split", date_format="iso")

    @task()
    def transform_dispositions(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_database_dispositions(df).to_json(
            orient="split", date_format="iso"
        )

    @task()
    def transform_transactions(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_database_transactions(df).to_json(
            orient="split", date_format="iso"
        )

    @task()
    def load(json_str: Any, table: str) -> None:
        df = pd.read_json(json_str, orient="split")
        load_data_to_snowflake(
            df,
            database="BANK_DB",
            schema="BRONZE_LAYER",
            table=table,
        )

    accounts_raw = extract("accounts")
    guests_raw = extract("guests") 
    users_raw = extract("users")  
    dispositions_raw = extract("dispositions")
    transactions_raw = extract("transactions")

    load(transform_accounts(accounts_raw), "DATABASE_ACCOUNTS")
    load(transform_guests(guests_raw), "DATABASE_GUESTS")
    load(transform_users(users_raw), "DATABASE_USERS")
    load(transform_dispositions(dispositions_raw), "DATABASE_DISPOSITIONS")
    load(transform_transactions(transactions_raw), "DATABASE_TRANSACTIONS")


bank_etl_database_dag()
