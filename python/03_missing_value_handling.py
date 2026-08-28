import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

project_root = Path(__file__).resolve().parent.parent

output_folder = project_root / "output"

input_file = output_folder / "cleaned_debt_data_wide.csv"

output_file = output_folder / "final_debt_data_wide.csv"


# =========================================================
# LOAD CLEANED DATASET
# =========================================================

print("=" * 70)
print("MISSING VALUE HANDLING")
print("=" * 70)

df = pd.read_csv(
    input_file,
    encoding="latin1"
)

print("\nDataset shape before missing value handling:")
print(df.shape)


# =========================================================
# IDENTIFY YEAR COLUMNS
# =========================================================

year_columns = [
    str(year)
    for year in range(2000, 2024)
    if str(year) in df.columns
]

print("\nYear columns:")
print(year_columns)


# =========================================================
# MISSING VALUES BEFORE FILLING
# =========================================================

print("\n" + "=" * 70)
print("MISSING VALUES BEFORE HANDLING")
print("=" * 70)

missing_before = df[year_columns].isnull().sum()

print(missing_before)

print("\nTotal missing values before:")
print(missing_before.sum())


# =========================================================
# FORWARD FILL AND BACKWARD FILL
# =========================================================

print("\n" + "=" * 70)
print("APPLYING FFILL AND BFILL")
print("=" * 70)

# Fill missing values from previous year
df[year_columns] = df[year_columns].ffill(axis=1)

# Fill remaining leading missing values from next available year
df[year_columns] = df[year_columns].bfill(axis=1)


# =========================================================
# MISSING VALUES AFTER FILLING
# =========================================================

print("\n" + "=" * 70)
print("MISSING VALUES AFTER FFILL + BFILL")
print("=" * 70)

missing_after = df[year_columns].isnull().sum()

print(missing_after)

print("\nTotal missing values after:")
print(missing_after.sum())


# =========================================================
# CALCULATE FILLED VALUES
# =========================================================

filled_values = (
    missing_before.sum()
    - missing_after.sum()
)

print("\nValues filled:")
print(filled_values)


# =========================================================
# SAVE FINAL DATASET
# =========================================================

df.to_csv(
    output_file,
    index=False
)

print("\n" + "=" * 70)
print("MISSING VALUE HANDLING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFinal dataset shape:")
print(df.shape)

print("\nSaved file:")
print(output_file)