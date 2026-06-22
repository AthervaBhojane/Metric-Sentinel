import pandas as pd

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    df = df.dropna()
    df.reset_index(drop=True, inplace=True)

    return df