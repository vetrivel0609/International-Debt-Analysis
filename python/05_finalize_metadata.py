import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

project_root = Path(__file__).resolve().parent.parent
output_folder = project_root / "output"


# =========================================================
# FILE PATHS
# =========================================================

countries_file = output_folder / "countries_cleaned.csv"
indicators_file = output_folder / "indicators_cleaned.csv"


# =========================================================
# LOAD DATASETS
# =========================================================

print("=" * 70)
print("FINALIZING METADATA FILES")
print("=" * 70)

countries_df = pd.read_csv(
    countries_file,
    encoding="latin1"
)

indicators_df = pd.read_csv(
    indicators_file,
    encoding="latin1"
)


# =========================================================
# COUNTRY METADATA
# =========================================================

print("\n" + "=" * 70)
print("COUNTRY METADATA")
print("=" * 70)

print("\nMissing values BEFORE:")
print(countries_df.isnull().sum())

# Fill missing metadata values
countries_df = countries_df.fillna("Not Available")

print("\nMissing values AFTER:")
print(countries_df.isnull().sum())

print("\nFinal shape:")
print(countries_df.shape)


# =========================================================
# INDICATOR METADATA
# =========================================================

print("\n" + "=" * 70)
print("INDICATOR METADATA")
print("=" * 70)

print("\nMissing values BEFORE:")
print(indicators_df.isnull().sum())

# Fill missing metadata values
indicators_df = indicators_df.fillna("Not Available")

print("\nMissing values AFTER:")
print(indicators_df.isnull().sum())

print("\nFinal shape:")
print(indicators_df.shape)


# =========================================================
# SAVE FINALIZED FILES
# =========================================================

countries_output = output_folder / "countries_final.csv"
indicators_output = output_folder / "indicators_final.csv"

countries_df.to_csv(
    countries_output,
    index=False
)

indicators_df.to_csv(
    indicators_output,
    index=False
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("METADATA FINALIZATION COMPLETED")
print("=" * 70)

print("\nSaved:")
print(countries_output)
print(indicators_output)

print("\nCountry Metadata Missing Values:")
print(countries_df.isnull().sum().sum())

print("\nIndicator Metadata Missing Values:")
print(indicators_df.isnull().sum().sum())