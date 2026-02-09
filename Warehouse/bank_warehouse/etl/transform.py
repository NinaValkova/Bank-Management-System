import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_account_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "account_id",
            "district_id",
            "frequency",
            "date",
        ]
    ]


def transform_district_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower()
    return df[
        [
            "a1",
            "a2",
            "a3",
            "a4",
            "a5",
            "a6",
            "a7",
            "a8",
            "a9",
            "a10",
            "a11",
            "a12",
            "a13",
            "a14",
            "a15",
            "a16",
        ]
    ]

def transform_client_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()

    return df[
        [
            "client_id",
            "birth_number",
            "district_id",
        ]
    ]


def transform_disp_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "disp_id",
            "client_id",
            "account_id",
            "type",
        ]
    ]



def transform_card_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "card_id",
            "disp_id",
            "type",
            "issued",
        ]
    ]


def transform_order_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "order_id",
            "account_id",
            "bank_to",
            "account_to",
            "amount",
            "k_symbol",
        ]
    ]


def transform_loan_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "loan_id",
            "account_id",
            "date",
            "amount",
            "duration",
            "payments",
            "status",
        ]
    ]



def transform_trans_data(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "trans_id",
            "account_id",
            "date",
            "type",
            "operation",
            "amount",
            "balance",
            "k_symbol",
            "bank",
            "account",
        ]
    ]
