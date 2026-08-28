import pandas as pd
import mysql.connector
from mysql.connector import Error

# ============================================================
# INTERNATIONAL DEBT ANALYSIS
# IMPORT CLEANED DATA INTO MYSQL
# ============================================================

print("=" * 80)
print("IMPORTING CLEANED DATA INTO MYSQL")
print("=" * 80)

# ============================================================
# 1. MYSQL CONNECTION
# ============================================================

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vetri@28",
        database="international_debt_db"
    )

    cursor = connection.cursor()

    print("\nMySQL connection successful!")

except Error as e:
    print("\nError connecting to MySQL:")
    print(e)
    exit()


# ============================================================
# 2. LOAD CSV FILES
# ============================================================

print("\n" + "=" * 80)
print("LOADING CSV FILES")
print("=" * 80)

countries_df = pd.read_csv(
    "output/countries_final.csv",
    encoding="latin1"
)

indicators_df = pd.read_csv(
    "output/indicators_final.csv",
    encoding="latin1"
)

debt_df = pd.read_csv(
    "output/final_debt_data_long.csv",
    encoding="latin1"
)

print("\nCountries dataset shape:")
print(countries_df.shape)

print("\nIndicators dataset shape:")
print(indicators_df.shape)

print("\nDebt dataset shape:")
print(debt_df.shape)

# ============================================================
# CHECK FOREIGN KEY MATCHES
# ============================================================

print("\n" + "=" * 80)
print("CHECKING FOREIGN KEY MATCHES")
print("=" * 80)

# ------------------------------------------------------------
# COUNTRY CODE CHECK
# ------------------------------------------------------------

debt_country_codes = set(debt_df["Country Code"].dropna().unique())

country_codes = set(
    countries_df["Country Code"].dropna().unique()
)

missing_country_codes = (
    debt_country_codes - country_codes
)

print("\nCountry Codes in Debt Data:")
print(len(debt_country_codes))

print("Country Codes in Countries Metadata:")
print(len(country_codes))

print("Missing Country Codes:")
print(len(missing_country_codes))

if missing_country_codes:
    print(sorted(missing_country_codes)[:20])


# ------------------------------------------------------------
# SERIES CODE CHECK
# ------------------------------------------------------------

debt_series_codes = set(
    debt_df["Series Code"].dropna().unique()
)

indicator_series_codes = set(
    indicators_df["Series Code"].dropna().unique()
)

missing_series_codes = (
    debt_series_codes - indicator_series_codes
)

print("\nSeries Codes in Debt Data:")
print(len(debt_series_codes))

print("Series Codes in Indicators Metadata:")
print(len(indicator_series_codes))

print("Missing Series Codes:")
print(len(missing_series_codes))

if missing_series_codes:
    print("\nMissing Series Code List:")
    print(sorted(missing_series_codes))


# ------------------------------------------------------------
# SAVE MISSING SERIES CODE RECORDS
# ------------------------------------------------------------

if missing_series_codes:

    missing_indicator_records = debt_df[
        debt_df["Series Code"].isin(
            missing_series_codes
        )
    ]

    missing_indicator_records.to_csv(
        "output/missing_indicator_records.csv",
        index=False
    )

    print("\nMissing indicator records saved to:")
    print(
        "output/missing_indicator_records.csv"
    )

# ============================================================
# ADD MISSING INDICATOR METADATA
# ============================================================

if missing_series_codes:

    print("\nMissing Series Codes found:")
    print(sorted(missing_series_codes))

    # Get the indicator names from the main debt dataset
    missing_indicators = (
        debt_df[
            debt_df["Series Code"].isin(missing_series_codes)
        ][
            ["Series Code", "Series Name"]
        ]
        .drop_duplicates()
        .copy()
    )

    print("\nMissing Indicator Details:")
    print(missing_indicators)

    # Create missing metadata records
    new_indicator_records = pd.DataFrame({
        "Series Code": missing_indicators["Series Code"],
        "Indicator Name": missing_indicators["Series Name"],
        "Short definition": "Not Available",
        "Long definition": "Not Available",
        "Source": "Not Available",
        "Topic": "Not Available",
        "Dataset": "Not Available",
        "Periodicity": "Not Available",
        "Aggregation method": "Not Available"
    })

    # Add the missing records to indicators dataset
    indicators_df = pd.concat(
        [indicators_df, new_indicator_records],
        ignore_index=True
    )

    # Remove any accidental duplicates
    indicators_df = indicators_df.drop_duplicates(
        subset="Series Code",
        keep="first"
    )

    print("\nUpdated Indicators Dataset Shape:")
    print(indicators_df.shape)

    print("\nMissing indicator metadata added successfully.")


# ============================================================
# 3. CLEAN MYSQL TABLES BEFORE IMPORT
# ============================================================

print("\n" + "=" * 80)
print("CLEARING EXISTING TABLE DATA")
print("=" * 80)

# Delete child table data first because of foreign keys
cursor.execute("DELETE FROM Debt_Data")
cursor.execute("DELETE FROM Indicators")
cursor.execute("DELETE FROM Countries")

connection.commit()

print("\nExisting table data cleared successfully.")


# ============================================================
# 4. IMPORT COUNTRIES TABLE
# ============================================================

print("\n" + "=" * 80)
print("IMPORTING COUNTRIES")
print("=" * 80)

country_query = """
INSERT INTO Countries (
    Country_Code,
    Country_Full_Name,
    Income_Group,
    Region,
    Lending_Category,
    Currency_Unit,
    External_Debt_Reporting_Status
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

country_data = list(
    countries_df[
        [
            "Country Code",
            "Country Full Name",
            "Income Group",
            "Region",
            "Lending Category",
            "Currency Unit",
            "External Debt Reporting Status"
        ]
    ].itertuples(index=False, name=None)
)

cursor.executemany(
    country_query,
    country_data
)

connection.commit()

print("Countries imported:", len(country_data))


# ============================================================
# 5. IMPORT INDICATORS TABLE
# ============================================================

print("\n" + "=" * 80)
print("IMPORTING INDICATORS")
print("=" * 80)

indicator_query = """
INSERT INTO Indicators (
    Series_Code,
    Indicator_Name,
    Short_Definition,
    Long_Definition,
    Source,
    Topic,
    Dataset,
    Periodicity,
    Aggregation_Method
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

indicator_data = list(
    indicators_df[
        [
            "Series Code",
            "Indicator Name",
            "Short definition",
            "Long definition",
            "Source",
            "Topic",
            "Dataset",
            "Periodicity",
            "Aggregation method"
        ]
    ].itertuples(index=False, name=None)
)

cursor.executemany(
    indicator_query,
    indicator_data
)

connection.commit()

print("Indicators imported:", len(indicator_data))


# ============================================================
# 6. PREPARE DEBT DATA
# ============================================================

print("\n" + "=" * 80)
print("PREPARING DEBT DATA")
print("=" * 80)

# Select only columns required for Debt_Data table
debt_import_df = debt_df[
    [
        "Country Code",
        "Series Code",
        "Year",
        "Value"
    ]
].copy()

# Rename columns for clarity
debt_import_df.columns = [
    "Country_Code",
    "Series_Code",
    "Year",
    "Debt_Value"
]

# Convert NaN values to None for MySQL
debt_import_df = debt_import_df.where(
    pd.notnull(debt_import_df),
    None
)

print("\nDebt records ready for import:")
print(len(debt_import_df))


# ============================================================
# 7. IMPORT DEBT DATA IN BATCHES
# ============================================================

print("\n" + "=" * 80)
print("IMPORTING DEBT DATA")
print("=" * 80)

debt_query = """
INSERT INTO Debt_Data (
    Country_Code,
    Series_Code,
    Year,
    Debt_Value
)
VALUES (%s, %s, %s, %s)
"""

batch_size = 10000
total_rows = len(debt_import_df)

for start in range(0, total_rows, batch_size):

    end = min(start + batch_size, total_rows)

    batch = list(
        debt_import_df.iloc[start:end]
        .itertuples(index=False, name=None)
    )

    cursor.executemany(
        debt_query,
        batch
    )

    connection.commit()

    print(
        f"Imported {end:,} of {total_rows:,} debt records"
    )


# ============================================================
# 8. VERIFY MYSQL DATA
# ============================================================

print("\n" + "=" * 80)
print("VERIFYING MYSQL TABLES")
print("=" * 80)

cursor.execute("SELECT COUNT(*) FROM Countries")
countries_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Indicators")
indicators_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Debt_Data")
debt_count = cursor.fetchone()[0]

print("\nCountries table records:")
print(countries_count)

print("\nIndicators table records:")
print(indicators_count)

print("\nDebt_Data table records:")
print(debt_count)


# ============================================================
# 9. CLOSE CONNECTION
# ============================================================

cursor.close()
connection.close()

print("\n" + "=" * 80)
print("MYSQL DATA IMPORT COMPLETED SUCCESSFULLY")
print("=" * 80)