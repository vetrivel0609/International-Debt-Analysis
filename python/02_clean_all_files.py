import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

project_root = Path(__file__).resolve().parent.parent

data_folder = project_root / "data"
output_folder = project_root / "output"

output_folder.mkdir(exist_ok=True)


# =========================================================
# FUNCTION: STANDARDIZE TEXT COLUMNS
# =========================================================

def clean_text_columns(df):

    for column in df.columns:

        if df[column].dtype == "object" or str(df[column].dtype) == "str":

            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    return df


# =========================================================
# FUNCTION: REMOVE EMPTY ROWS AND DUPLICATES
# =========================================================

def basic_cleaning(df):

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove completely empty columns
    df = df.dropna(axis=1, how="all")

    # Clean text columns
    df = clean_text_columns(df)

    return df


# =========================================================
# CLEAN FILE 1:
# IDS_ALLCountries_Data.csv
# =========================================================

print("\n" + "=" * 70)
print("CLEANING: IDS_ALLCountries_Data.csv")
print("=" * 70)

main_file = data_folder / "IDS_ALLCountries_Data.csv"

debt_df = pd.read_csv(
    main_file,
    encoding="latin1"
)

print("Original shape:", debt_df.shape)

# Basic cleaning
debt_df = basic_cleaning(debt_df)

print("Shape after basic cleaning:", debt_df.shape)


# ---------------------------------------------------------
# Remove footer / non-data rows
# ---------------------------------------------------------

debt_df = debt_df.dropna(
    subset=["Country Code"]
)

print("Shape after removing non-data rows:", debt_df.shape)


# ---------------------------------------------------------
# Remove years 2024 to 2032
# ---------------------------------------------------------

years_to_remove = [
    "2024",
    "2025",
    "2026",
    "2027",
    "2028",
    "2029",
    "2030",
    "2031",
    "2032"
]

debt_df = debt_df.drop(
    columns=years_to_remove,
    errors="ignore"
)

print("Shape after removing years 2024-2032:", debt_df.shape)


# ---------------------------------------------------------
# Identify remaining year columns: 2000 to 2023
# ---------------------------------------------------------

year_columns = [
    str(year)
    for year in range(2000, 2024)
    if str(year) in debt_df.columns
]


# ---------------------------------------------------------
# Remove rows where ALL remaining years are missing
# ---------------------------------------------------------

rows_before = len(debt_df)

debt_df = debt_df.dropna(
    subset=year_columns,
    how="all"
)

rows_removed = rows_before - len(debt_df)

print("Rows removed with no data in any year:", rows_removed)
print("Final shape:", debt_df.shape)


# ---------------------------------------------------------
# Save cleaned main dataset
# ---------------------------------------------------------

main_output = output_folder / "cleaned_debt_data_wide.csv"

debt_df.to_csv(
    main_output,
    index=False
)

print("Saved:", main_output)


# =========================================================
# CLEAN FILE 2:
# IDS_CountryMetaData.csv
# =========================================================

print("\n" + "=" * 70)
print("CLEANING: IDS_CountryMetaData.csv")
print("=" * 70)

country_file = data_folder / "IDS_CountryMetaData.csv"

country_df = pd.read_csv(
    country_file,
    encoding="latin1"
)

print("Original shape:", country_df.shape)

country_df = basic_cleaning(country_df)


# ---------------------------------------------------------
# Keep only useful columns for this project
# ---------------------------------------------------------

country_columns_to_keep = [
    "Code",
    "Long Name",
    "Income Group",
    "Region",
    "Lending category",
    "Currency Unit",
    "External debt Reporting status"
]

country_columns_to_keep = [
    column
    for column in country_columns_to_keep
    if column in country_df.columns
]

country_df = country_df[country_columns_to_keep]


# Rename columns for easier use
country_df = country_df.rename(
    columns={
        "Code": "Country Code",
        "Long Name": "Country Full Name",
        "Lending category": "Lending Category",
        "External debt Reporting status": "External Debt Reporting Status"
    }
)

print("Final shape:", country_df.shape)

country_output = output_folder / "countries_cleaned.csv"

country_df.to_csv(
    country_output,
    index=False
)

print("Saved:", country_output)


# =========================================================
# CLEAN FILE 3:
# IDS_SeriesMetaData.csv
# =========================================================

print("\n" + "=" * 70)
print("CLEANING: IDS_SeriesMetaData.csv")
print("=" * 70)

series_file = data_folder / "IDS_SeriesMetaData.csv"

series_df = pd.read_csv(
    series_file,
    encoding="latin1"
)

print("Original shape:", series_df.shape)

series_df = basic_cleaning(series_df)


# ---------------------------------------------------------
# Keep useful indicator metadata
# ---------------------------------------------------------

series_columns_to_keep = [
    "Code",
    "Indicator Name",
    "Short definition",
    "Long definition",
    "Source",
    "Topic",
    "Dataset",
    "Periodicity",
    "Aggregation method"
]

series_columns_to_keep = [
    column
    for column in series_columns_to_keep
    if column in series_df.columns
]

series_df = series_df[series_columns_to_keep]


# Rename Code
series_df = series_df.rename(
    columns={
        "Code": "Series Code"
    }
)

print("Final shape:", series_df.shape)

series_output = output_folder / "indicators_cleaned.csv"

series_df.to_csv(
    series_output,
    index=False
)

print("Saved:", series_output)


# =========================================================
# CLEAN FILE 4:
# IDS_FootNoteMetaData.csv
# =========================================================

print("\n" + "=" * 70)
print("CLEANING: IDS_FootNoteMetaData.csv")
print("=" * 70)

footnote_file = data_folder / "IDS_FootNoteMetaData.csv"

footnote_df = pd.read_csv(
    footnote_file,
    encoding="latin1"
)

print("Original shape:", footnote_df.shape)

footnote_df = basic_cleaning(footnote_df)


# ---------------------------------------------------------
# Remove redundant Type column
# ---------------------------------------------------------

footnote_df = footnote_df.drop(
    columns=["Type"],
    errors="ignore"
)

print("Final shape:", footnote_df.shape)

footnote_output = output_folder / "footnotes_cleaned.csv"

footnote_df.to_csv(
    footnote_output,
    index=False
)

print("Saved:", footnote_output)


# =========================================================
# CLEAN FILE 5:
# Country-Series - Metadata.csv
# =========================================================

print("\n" + "=" * 70)
print("CLEANING: Country-Series - Metadata.csv")
print("=" * 70)

country_series_file = (
    data_folder / "Country-Series - Metadata.csv"
)

country_series_df = pd.read_csv(
    country_series_file,
    encoding="latin1"
)

print("Original shape:", country_series_df.shape)

country_series_df = basic_cleaning(country_series_df)


# ---------------------------------------------------------
# Remove redundant Type column
# ---------------------------------------------------------

country_series_df = country_series_df.drop(
    columns=["Type"],
    errors="ignore"
)

print("Final shape:", country_series_df.shape)

country_series_output = (
    output_folder / "country_series_cleaned.csv"
)

country_series_df.to_csv(
    country_series_output,
    index=False
)

print("Saved:", country_series_output)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 70)
print("ALL 5 FILES CLEANED SUCCESSFULLY")
print("=" * 70)

print("\nCleaned files created:")

for file in output_folder.glob("*.csv"):
    print("-", file.name)

print("\nNext step:")
print("Prepare the main debt dataset for analysis.")
print("Convert Wide Format -> Long Format.")