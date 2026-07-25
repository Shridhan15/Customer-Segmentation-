import pandas as pd

def run_eda(df: pd.DataFrame) -> dict:
    return {
        "total_records": len(df),
        "columns": df.columns.tolist(),
        "missing_values": df.isnull().sum().to_dict(),
        "summary": df.describe().to_dict()
    }