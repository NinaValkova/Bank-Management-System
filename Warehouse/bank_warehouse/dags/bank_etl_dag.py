from typing import Any
import os
import pandas as pd
import yaml
from pendulum import datetime

from airflow.decorators import dag, task
from airflow.sdk.bases.operator import AirflowException

from etl.extract_data import extract_data_from_s3
from etl.load_data import load_data_to_snowflake
from etl.transform import (
    transform_account_data,
    transform_district_data,
    transform_card_data,
    transform_client_data,
    transform_disp_data,
    transform_order_data,
    transform_loan_data,
    transform_trans_data,
)

with open("include/config.yaml") as file:
    config = yaml.safe_load(file)


@dag(
    dag_id="bank_etl_dag",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["bank"],
)
def bank_etl_dag():

    @task
    def extract_all_asc(bucket: str, folder: str, aws_conn_id: str) -> Any:
        files = extract_data_from_s3(
            bucket=bucket,
            folder=folder,
            aws_conn_id=aws_conn_id,
            file_type="asc",
        )

        return {k: v.to_json(orient="split") for k, v in files.items()}

    @task
    def pick_file(files: Any, keyword: str) -> Any:
        keyword = keyword.lower()
        available_keys = list(files.keys())

        for key, json_str in files.items():
            filename = os.path.basename(key).lower()
            if keyword in filename:
                return json_str

        raise AirflowException(
            f"{keyword} file not found in S3 listing. "
            f"Available files: {[os.path.basename(k) for k in available_keys]}"
        )

    @task
    def transform_district(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_district_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_account(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_account_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_client(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_client_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_disp(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_disp_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_card(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_card_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_order(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_order_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_loan(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_loan_data(df).to_json(orient="split", date_format="iso")

    @task
    def transform_trans(json_str: Any) -> Any:
        df = pd.read_json(json_str, orient="split")
        return transform_trans_data(df).to_json(orient="split", date_format="iso")

    @task
    def load(json_str: Any, target_key: str) -> None:
        df = pd.read_json(json_str, orient="split")
        db = config["snowflake"]["database"]
        target = config["snowflake"]["targets"][target_key]
        load_data_to_snowflake(
            df,
            database=db,
            schema=target["schema"],
            table=target["table"],
        )

    all_files = extract_all_asc(
        bucket=config["s3"]["bucket"],
        folder=config["s3"]["folder"],
        aws_conn_id=config["aws_conn_id"],
    )

    district_raw = pick_file(all_files, "district")
    account_raw = pick_file(all_files, "account")
    client_raw = pick_file(all_files, "client")
    disp_raw = pick_file(all_files, "disp")
    card_raw = pick_file(all_files, "card")
    order_raw = pick_file(all_files, "order")
    loan_raw = pick_file(all_files, "loan")
    trans_raw = pick_file(all_files, "trans")

    load(transform_district(district_raw), "district")
    load(transform_account(account_raw), "account")
    load(transform_client(client_raw), "client")
    load(transform_disp(disp_raw), "disp")
    load(transform_card(card_raw), "card")
    load(transform_order(order_raw), "order")
    load(transform_loan(loan_raw), "loan")
    load(transform_trans(trans_raw), "transaction")


bank_etl_dag()
