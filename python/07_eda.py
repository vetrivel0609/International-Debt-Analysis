import pandas as pd

# ============================================================
# INTERNATIONAL DEBT ANALYSIS - EXPLORATORY DATA ANALYSIS
# ============================================================

print("=" * 80)
print("EXPLORATORY DATA ANALYSIS (EDA)")
print("=" * 80)


# ============================================================
# 1. LOAD DATASETS
# ============================================================

print("\nLOADING DATASETS...\n")

debt_df = pd.read_csv(
    "output/final_debt_data_long.csv",
    encoding="latin1"
)
countries_df = pd.read_csv(
    "output/countries_final.csv",
    encoding="latin1"
)

indicators_df = pd.read_csv(
    "output/indicators_final.csv",
    encoding="latin1"
)


# ============================================================
# 2. BASIC DATASET OVERVIEW
# ============================================================

print("=" * 80)
print("1. DATASET OVERVIEW")
print("=" * 80)

print("\nMain Debt Dataset Shape:")
print(debt_df.shape)

print("\nCountry Metadata Shape:")
print(countries_df.shape)

print("\nIndicator Metadata Shape:")
print(indicators_df.shape)

print("\nMain Dataset Columns:")
print(debt_df.columns.tolist())

print("\nYear Range:")
print("Minimum Year:", debt_df["Year"].min())
print("Maximum Year:", debt_df["Year"].max())

print("\nNumber of Countries:")
print(debt_df["Country Name"].nunique())

print("\nNumber of Country Codes:")
print(debt_df["Country Code"].nunique())

print("\nNumber of Indicators:")
print(debt_df["Series Name"].nunique())

print("\nNumber of Series Codes:")
print(debt_df["Series Code"].nunique())


# ============================================================
# 3. STATISTICAL SUMMARY
# ============================================================

print("\n" + "=" * 80)
print("2. STATISTICAL SUMMARY OF VALUE")
print("=" * 80)

print("\nOverall Statistical Summary:")
print(debt_df["Value"].describe())


# ============================================================
# 4. COUNTRIES WITH MOST RECORDS
# ============================================================

print("\n" + "=" * 80)
print("3. COUNTRY-WISE RECORD DISTRIBUTION")
print("=" * 80)

country_records = (
    debt_df["Country Name"]
    .value_counts()
    .reset_index()
)

country_records.columns = [
    "Country Name",
    "Number of Records"
]

print("\nTop 20 Countries by Number of Records:")
print(country_records.head(20))


# ============================================================
# 5. INDICATOR DISTRIBUTION
# ============================================================

print("\n" + "=" * 80)
print("4. INDICATOR DISTRIBUTION")
print("=" * 80)

indicator_records = (
    debt_df["Series Name"]
    .value_counts()
    .reset_index()
)

indicator_records.columns = [
    "Series Name",
    "Number of Records"
]

print("\nTop 20 Most Frequent Indicators:")
print(indicator_records.head(20))


# ============================================================
# 6. YEAR-WISE DATA DISTRIBUTION
# ============================================================

print("\n" + "=" * 80)
print("5. YEAR-WISE DATA DISTRIBUTION")
print("=" * 80)

year_records = (
    debt_df.groupby("Year")
    .size()
    .reset_index(name="Number of Records")
)

print(year_records)


# ============================================================
# 7. SELECT IMPORTANT DEBT INDICATORS
# ============================================================

print("\n" + "=" * 80)
print("6. AVAILABLE DEBT-RELATED INDICATORS")
print("=" * 80)

debt_indicators = indicators_df[
    indicators_df["Indicator Name"]
    .str.contains(
        "debt",
        case=False,
        na=False
    )
]

print("\nNumber of Debt-Related Indicators:")
print(len(debt_indicators))

print("\nFirst 30 Debt-Related Indicators:")
print(
    debt_indicators[
        ["Series Code", "Indicator Name"]
    ].head(30)
)


# ============================================================
# 8. COUNTERPART AREA DISTRIBUTION
# ============================================================

print("\n" + "=" * 80)
print("7. COUNTERPART AREA DISTRIBUTION")
print("=" * 80)

counterpart_distribution = (
    debt_df["Counterpart-Area Name"]
    .value_counts()
    .reset_index()
)

counterpart_distribution.columns = [
    "Counterpart-Area Name",
    "Number of Records"
]

print(counterpart_distribution.head(20))


# ============================================================
# 9. COUNTRY + INDICATOR RECORD ANALYSIS
# ============================================================

print("\n" + "=" * 80)
print("8. COUNTRY-INDICATOR ANALYSIS")
print("=" * 80)

country_indicator_counts = (
    debt_df.groupby(
        ["Country Name", "Series Name"]
    )
    .size()
    .reset_index(name="Number of Yearly Records")
)

print("\nSample Country-Indicator Records:")
print(country_indicator_counts.head(20))


# ============================================================
# 10. MERGE COUNTRY METADATA
# ============================================================

print("\n" + "=" * 80)
print("9. MERGING COUNTRY METADATA")
print("=" * 80)

eda_df = debt_df.merge(
    countries_df,
    on="Country Code",
    how="left"
)

print("\nMerged Dataset Shape:")
print(eda_df.shape)

print("\nRegion Distribution:")
print(
    eda_df["Region"]
    .value_counts()
)

print("\nIncome Group Distribution:")
print(
    eda_df["Income Group"]
    .value_counts()
)


# ============================================================
# 11. DATA QUALITY CHECK
# ============================================================

print("\n" + "=" * 80)
print("10. FINAL EDA DATA QUALITY CHECK")
print("=" * 80)

print("\nMissing Values:")
print(eda_df.isnull().sum())

print("\nDuplicate Rows:")
print(eda_df.duplicated().sum())

# ============================================================
# 12. SELECT MAIN DEBT INDICATOR
# ============================================================

print("\n" + "=" * 80)
print("11. SELECTING MAIN DEBT INDICATOR")
print("=" * 80)

main_indicator_keywords = [
    "External debt stocks, total"
]

main_indicators = indicators_df[
    indicators_df["Indicator Name"]
    .str.contains(
        "External debt stocks, total",
        case=False,
        na=False
    )
]

print("\nMatching Main Debt Indicators:")
print(
    main_indicators[
        ["Series Code", "Indicator Name"]
    ].head(20)
)

if main_indicators.empty:
    print("\nERROR: Main debt indicator not found.")
    print("Please check the available indicators manually.")
else:

    main_series_code = main_indicators.iloc[0]["Series Code"]
    main_indicator_name = main_indicators.iloc[0]["Indicator Name"]

    print("\nSelected Series Code:")
    print(main_series_code)

    print("\nSelected Indicator:")
    print(main_indicator_name)


    # ========================================================
    # 13. CREATE MAIN DEBT ANALYSIS DATASET
    # ========================================================

    print("\n" + "=" * 80)
    print("12. CREATING MAIN DEBT ANALYSIS DATASET")
    print("=" * 80)

    main_debt_df = eda_df[
        eda_df["Series Code"] == main_series_code
    ].copy()

    print("\nMain Debt Dataset Shape:")
    print(main_debt_df.shape)

    print("\nYear Range:")
    print(
        main_debt_df["Year"].min(),
        "to",
        main_debt_df["Year"].max()
    )

    print("\nNumber of Countries/Groups:")
    print(main_debt_df["Country Name"].nunique())


    # ========================================================
    # 14. COUNTRY-WISE DEBT ANALYSIS
    # ========================================================

    print("\n" + "=" * 80)
    print("13. COUNTRY-WISE DEBT ANALYSIS")
    print("=" * 80)

    country_debt = (
        main_debt_df
        .groupby(["Country Name", "Country Code"])["Value"]
        .agg(
            Average_Debt="mean",
            Maximum_Debt="max",
            Minimum_Debt="min",
            Latest_Debt="last"
        )
        .reset_index()
    )

    print("\nCountry-wise Debt Analysis:")
    print(country_debt.head(20))


    # ========================================================
    # 15. TOP 10 COUNTRIES BY LATEST DEBT
    # ========================================================

    print("\n" + "=" * 80)
    print("14. TOP 10 COUNTRIES BY LATEST DEBT")
    print("=" * 80)

    latest_year = main_debt_df["Year"].max()

    latest_debt = (
        main_debt_df[
            main_debt_df["Year"] == latest_year
        ]
        .sort_values("Value", ascending=False)
    )

    top_10_countries = latest_debt[
        ["Country Name", "Country Code", "Value"]
    ].head(10)

    print(f"\nTop 10 Countries/Groups by Debt in {latest_year}:")
    print(top_10_countries)


    # ========================================================
    # 16. BOTTOM 10 COUNTRIES BY LATEST DEBT
    # ========================================================

    print("\n" + "=" * 80)
    print("15. BOTTOM 10 COUNTRIES BY LATEST DEBT")
    print("=" * 80)

    bottom_10_countries = (
        latest_debt[
            latest_debt["Value"] > 0
        ]
        .sort_values("Value")
        [
            ["Country Name", "Country Code", "Value"]
        ]
        .head(10)
    )

    print(f"\nBottom 10 Countries/Groups by Debt in {latest_year}:")
    print(bottom_10_countries)


    # ========================================================
    # 17. YEAR-WISE DEBT TREND
    # ========================================================

    print("\n" + "=" * 80)
    print("16. YEAR-WISE DEBT TREND")
    print("=" * 80)

    yearly_debt_trend = (
        main_debt_df
        .groupby("Year")["Value"]
        .agg(
            Average_Debt="mean",
            Maximum_Debt="max",
            Minimum_Debt="min"
        )
        .reset_index()
    )

    print("\nYear-wise Debt Trend:")
    print(yearly_debt_trend)


    # ========================================================
    # 18. GROWTH AND DECLINE ANALYSIS
    # ========================================================

    print("\n" + "=" * 80)
    print("17. YEAR-OVER-YEAR GROWTH ANALYSIS")
    print("=" * 80)

    yearly_growth = (
        yearly_debt_trend[
            ["Year", "Average_Debt"]
        ]
        .copy()
    )

    yearly_growth["Percentage_Change"] = (
        yearly_growth["Average_Debt"]
        .pct_change()
        * 100
    )

    print("\nYear-over-Year Percentage Change:")
    print(yearly_growth)


    # ========================================================
    # 19. HIGHEST AND LOWEST YEARLY CHANGE
    # ========================================================

    print("\n" + "=" * 80)
    print("18. HIGHEST AND LOWEST YEARLY CHANGE")
    print("=" * 80)

    highest_growth = (
        yearly_growth
        .dropna()
        .nlargest(5, "Percentage_Change")
    )

    lowest_growth = (
        yearly_growth
        .dropna()
        .nsmallest(5, "Percentage_Change")
    )

    print("\nTop 5 Highest Growth Years:")
    print(highest_growth)

    print("\nTop 5 Highest Decline Years:")
    print(lowest_growth)


    # ========================================================
    # 20. REGIONAL DEBT ANALYSIS
    # ========================================================

    print("\n" + "=" * 80)
    print("19. REGIONAL DEBT ANALYSIS")
    print("=" * 80)

    regional_debt = (
        main_debt_df[
            main_debt_df["Year"] == latest_year
        ]
        .groupby("Region")["Value"]
        .agg(
            Average_Debt="mean",
            Maximum_Debt="max",
            Number_of_Records="count"
        )
        .reset_index()
        .sort_values(
            "Average_Debt",
            ascending=False
        )
    )

    print(f"\nRegional Debt Analysis - {latest_year}:")
    print(regional_debt)


    # ========================================================
    # 21. INCOME GROUP DEBT ANALYSIS
    # ========================================================

    print("\n" + "=" * 80)
    print("20. INCOME GROUP DEBT ANALYSIS")
    print("=" * 80)

    income_group_debt = (
        main_debt_df[
            main_debt_df["Year"] == latest_year
        ]
        .groupby("Income Group")["Value"]
        .agg(
            Average_Debt="mean",
            Maximum_Debt="max",
            Number_of_Records="count"
        )
        .reset_index()
        .sort_values(
            "Average_Debt",
            ascending=False
        )
    )

    print(f"\nIncome Group Debt Analysis - {latest_year}:")
    print(income_group_debt)


    # ========================================================
    # 22. DEBT VOLATILITY ANALYSIS
    # ========================================================

    print("\n" + "=" * 80)
    print("21. DEBT VOLATILITY ANALYSIS")
    print("=" * 80)

    country_volatility = (
        main_debt_df
        .groupby(["Country Name", "Country Code"])["Value"]
        .agg(
            Average_Debt="mean",
            Standard_Deviation="std",
            Maximum_Debt="max",
            Minimum_Debt="min"
        )
        .reset_index()
    )

    country_volatility = (
        country_volatility
        .sort_values(
            "Standard_Deviation",
            ascending=False
        )
    )

    print("\nTop 10 Most Volatile Countries/Groups:")
    print(country_volatility.head(10))


    # ========================================================
    # 23. COUNTRY COMPARISON
    # ========================================================

    print("\n" + "=" * 80)
    print("22. COUNTRY COMPARISON")
    print("=" * 80)

    top_country_names = (
        top_10_countries["Country Name"]
        .head(5)
        .tolist()
    )

    country_comparison = (
        main_debt_df[
            main_debt_df["Country Name"]
            .isin(top_country_names)
        ]
        [
            ["Country Name", "Year", "Value"]
        ]
        .sort_values(
            ["Country Name", "Year"]
        )
    )

    print("\nTop 5 Country Debt Comparison:")
    print(country_comparison.head(50))


    # ========================================================
    # 24. CREATE INSIGHT SUMMARY
    # ========================================================

    print("\n" + "=" * 80)
    print("23. EDA INSIGHT SUMMARY")
    print("=" * 80)

    print(
        f"\nMain Indicator Used: {main_indicator_name}"
    )

    print(
        f"Latest Year Available: {latest_year}"
    )

    print(
        f"Highest Debt Record: "
        f"{top_10_countries.iloc[0]['Country Name']}"
    )

    print(
        f"Highest Debt Value: "
        f"{top_10_countries.iloc[0]['Value']:,.2f}"
    )

    print(
        f"Lowest Positive Debt Record: "
        f"{bottom_10_countries.iloc[0]['Country Name']}"
    )

    print(
        f"Lowest Positive Debt Value: "
        f"{bottom_10_countries.iloc[0]['Value']:,.2f}"
    )


    # ========================================================
    # 25. SAVE ALL EDA ANALYSIS OUTPUTS
    # ========================================================

    print("\n" + "=" * 80)
    print("24. SAVING EDA ANALYSIS RESULTS")
    print("=" * 80)

    main_debt_df.to_csv(
        "output/eda_main_debt_indicator.csv",
        index=False
    )

    country_debt.to_csv(
        "output/eda_country_debt_analysis.csv",
        index=False
    )

    top_10_countries.to_csv(
        "output/eda_top_10_countries.csv",
        index=False
    )

    bottom_10_countries.to_csv(
        "output/eda_bottom_10_countries.csv",
        index=False
    )

    yearly_debt_trend.to_csv(
        "output/eda_yearly_debt_trend.csv",
        index=False
    )

    yearly_growth.to_csv(
        "output/eda_yearly_growth.csv",
        index=False
    )

    regional_debt.to_csv(
        "output/eda_regional_debt_analysis.csv",
        index=False
    )

    income_group_debt.to_csv(
        "output/eda_income_group_analysis.csv",
        index=False
    )

    country_volatility.to_csv(
        "output/eda_country_volatility.csv",
        index=False
    )

    country_comparison.to_csv(
        "output/eda_country_comparison.csv",
        index=False
    )

    print("\nEDA Analysis Files Saved Successfully!")

# ============================================================
# EDA COMPLETED
# ============================================================

print("\n" + "=" * 80)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 80)