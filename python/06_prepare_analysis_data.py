import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

project_root = Path(__file__).resolve().parent.parent
output_folder = project_root / "output"

input_file = output_folder / "final_debt_data_wide.csv"

output_file = output_folder / "final_debt_data_long.csv"


# =========================================================
# LOAD FINAL WIDE DATASET
# =========================================================

print("=" * 70)
print("PREPARING MAIN DEBT DATA FOR ANALYSIS")
print("=" * 70)

df = pd.read_csv(
    input_file,
    encoding="latin1"
)

print("\nOriginal dataset shape:")
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
# IDENTIFY ID COLUMNS
# =========================================================

id_columns = [
    "Country Name",
    "Country Code",
    "Counterpart-Area Name",
    "Counterpart-Area Code",
    "Series Name",
    "Series Code"
]

print("\nIdentifier columns:")
print(id_columns)


# =========================================================
# CONVERT WIDE FORMAT TO LONG FORMAT
# =========================================================

print("\n" + "=" * 70)
print("CONVERTING WIDE FORMAT TO LONG FORMAT")
print("=" * 70)

long_df = pd.melt(
    df,
    id_vars=id_columns,
    value_vars=year_columns,
    var_name="Year",
    value_name="Value"
)


# =========================================================
# DATA TYPE CONVERSION
# =========================================================

long_df["Year"] = pd.to_numeric(
    long_df["Year"],
    errors="coerce"
)

long_df["Value"] = pd.to_numeric(
    long_df["Value"],
    errors="coerce"
)


# =========================================================
# SORT DATA
# =========================================================

long_df = long_df.sort_values(
    by=[
        "Country Code",
        "Counterpart-Area Code",
        "Series Code",
        "Year"
    ]
).reset_index(drop=True)


# =========================================================
# VERIFY LONG FORMAT DATA
# =========================================================

print("\nLong format shape:")
print(long_df.shape)

print("\nFirst 10 rows:")
print(long_df.head(10))

print("\nData types:")
print(long_df.dtypes)

print("\nYear range:")
print(
    "Minimum year:",
    long_df["Year"].min()
)
print(
    "Maximum year:",
    long_df["Year"].max()
)

print("\nMissing values:")
print(long_df.isnull().sum())

print("\nDuplicate rows:")
print(long_df.duplicated().sum())


# =========================================================
# SAVE LONG FORMAT DATASET
# =========================================================

long_df.to_csv(
    output_file,
    index=False
)


# =========================================================
# COMPLETION MESSAGE
# =========================================================

print("\n" + "=" * 70)
print("WIDE TO LONG TRANSFORMATION COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFinal dataset shape:")
print(long_df.shape)

print("\nSaved file:")
print(output_file)