import pandas as pd


def transform_database_accounts(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[["id", "account_number", "balance", "created_at"]]


def transform_database_guests(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()

    cols = [
        "id",
        "first_name",
        "second_name",
        "username",
        "email",
        "password",
        "created_at",
    ]

    return df.loc[df["id"].ne(1), cols]


def transform_database_users(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[["id", "birth_number"]]


def transform_database_dispositions(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[["id", "user_id", "account_id", "type"]]


def transform_database_transactions(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower()
    return df[
        [
            "id",
            "account_id",
            "from_account",
            "to_account",
            "amount",
            "balance",
            "currency",
            "date",
            "type",
            "operation",
        ]
    ]
