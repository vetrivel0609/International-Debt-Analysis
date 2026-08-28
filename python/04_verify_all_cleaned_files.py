import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

project_root = Path(__file__).resolve().parent.parent
output_folder = project_root / "output"


# =========================================================
# FILES TO VERIFY
# =========================================================

files = {
    "Main Debt Dataset": "final_debt_data_wide.csv",
    "Country Metadata": "countries_cleaned.csv",
    "Indicator Metadata": "indicators_cleaned.csv",
    "Footnotes Metadata": "footnotes_cleaned.csv",
    "Country-Series Metadata": "country_series_cleaned.csv"
}


# =========================================================
# VERIFY ALL FILES
# =========================================================

print("=" * 80)
print("FINAL VERIFICATION OF ALL 5 CLEANED DATASETS")
print("=" * 80)


summary = []

for dataset_name, file_name in files.items():

    file_path = output_folder / file_name

    print("\n" + "=" * 80)
    print(dataset_name.upper())
    print("=" * 80)

    if not file_path.exists():
        print(f"FILE NOT FOUND: {file_name}")
        continue

    # Load file
    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    # Basic information
    print("\nFile Name:")
    print(file_name)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing Values:")
    print(df.isnull().sum())

    total_missing = df.isnull().sum().sum()

    print("\nTotal Missing Values:")
    print(total_missing)

    duplicate_rows = df.duplicated().sum()

    print("\nDuplicate Rows:")
    print(duplicate_rows)

    empty_rows = df.isna().all(axis=1).sum()

    print("\nCompletely Empty Rows:")
    print(empty_rows)

    empty_columns = df.columns[
        df.isna().all()
    ].tolist()

    print("\nCompletely Empty Columns:")
    print(empty_columns)

    # Add to summary
    summary.append({
        "Dataset": dataset_name,
        "File": file_name,
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": total_missing,
        "Duplicate Rows": duplicate_rows,
        "Empty Rows": empty_rows,
        "Empty Columns": len(empty_columns)
    })


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 80)
print("FINAL CLEANING SUMMARY")
print("=" * 80)

summary_df = pd.DataFrame(summary)

print("\n")
print(summary_df.to_string(index=False))


# =========================================================
# SAVE VERIFICATION REPORT
# =========================================================

report_file = output_folder / "final_data_verification_report.csv"

summary_df.to_csv(
    report_file,
    index=False
)

print("\nVerification report saved to:")
print(report_file)

print("\n" + "=" * 80)
print("VERIFICATION COMPLETED")
print("=" * 80)