import pandas as pd
from pathlib import Path


# Project root folder
project_root = Path(__file__).resolve().parent.parent

# Data folder
data_folder = project_root / "data"


# Find all CSV files
csv_files = list(data_folder.glob("*.csv"))

print("=" * 80)
print("INTERNATIONAL DEBT ANALYSIS - DATASET INSPECTION")
print("=" * 80)

print(f"\nNumber of CSV files found: {len(csv_files)}\n")


for file in csv_files:

    print("\n" + "=" * 80)
    print(f"FILE: {file.name}")
    print("=" * 80)

    try:
        # Load CSV
        df = pd.read_csv(
            file,
            encoding="latin1"
        )

        # Basic information
        print("\n--- DATASET SHAPE ---")
        print(df.shape)

        print("\n--- COLUMN NAMES ---")
        print(df.columns.tolist())

        print("\n--- DATA TYPES ---")
        print(df.dtypes)

        print("\n--- FIRST 5 ROWS ---")
        print(df.head())

        print("\n--- LAST 5 ROWS ---")
        print(df.tail())

        print("\n--- MISSING VALUES ---")
        print(df.isnull().sum())

        print("\n--- DUPLICATE ROWS ---")
        print(df.duplicated().sum())

        print("\n--- COMPLETELY EMPTY ROWS ---")
        print(df.isna().all(axis=1).sum())

        print("\n--- COMPLETELY EMPTY COLUMNS ---")
        print(df.columns[df.isna().all()].tolist())

    except Exception as e:
        print(f"\nERROR while reading {file.name}")
        print(e)


print("\n" + "=" * 80)
print("INSPECTION COMPLETED")
print("=" * 80)