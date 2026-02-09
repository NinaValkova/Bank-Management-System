import io
import os
import logging
import pandas as pd

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk.bases.operator import AirflowException

logger = logging.getLogger(__name__)


def extract_data_from_s3(bucket, folder, aws_conn_id, file_type="asc") -> dict:
    s3 = S3Hook(aws_conn_id=aws_conn_id)
    keys = s3.list_keys(bucket_name=bucket, prefix=folder)

    if not keys:
        raise AirflowException("No files found in S3")

    dfs = {}

    for key in keys:
        if not key.lower().endswith(f".{file_type}"):
            continue

        obj = s3.get_key(key, bucket)
        raw = obj.get()["Body"].read().decode("utf-8")

        if "trans" in key.lower():
            chunks = []
            for chunk in pd.read_csv(io.StringIO(raw), sep=";", chunksize=50_000):
                chunks.append(chunk)

            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(io.StringIO(raw), sep=";")

        dfs[key] = df

    if not dfs:
        raise AirflowException("No ASC files processed")

    return dfs
