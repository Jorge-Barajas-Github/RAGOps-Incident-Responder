import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/incident_reports.csv")

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Could not find dataset at: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    print("\nDataset shape:")
    print(df.shape)

    print("\nColumns:")
    for col in df.columns:
        print(f"- {col}")

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isna().sum())

if __name__ == "__main__":
    main()