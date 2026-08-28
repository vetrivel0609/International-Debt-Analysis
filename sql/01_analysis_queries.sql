USE international_debt_db;

-- ============================================================
-- BASIC QUERIES
-- ============================================================
-- QUERY 01
-- Retrieve all distinct country names
-- ============================================================
SELECT DISTINCT Country_Full_Name
FROM Countries
ORDER BY Country_Full_Name;
-- ============================================================
-- QUERY 02
-- Count total number of countries
-- ============================================================
SELECT COUNT(*) AS Total_Countries
FROM Countries;
-- ============================================================
-- QUERY 03
-- Find total number of indicators
-- ============================================================
SELECT COUNT(*) AS Total_Indicators
FROM Indicators;
-- ============================================================
-- QUERY 04
-- Display first 10 records of the dataset
-- ============================================================
SELECT
    d.Debt_ID,
    c.Country_Full_Name AS Country,
    i.Indicator_Name AS Indicator,
    d.Year,
    d.Debt_Value
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
ORDER BY d.Debt_ID
LIMIT 10;
-- ============================================================
-- QUERY 05
-- Calculate total global debt
-- ============================================================
SELECT
    SUM(Debt_Value) AS Total_Global_Debt
FROM Debt_Data;
-- ============================================================
-- QUERY 06
-- List all unique indicator names
-- ============================================================
SELECT DISTINCT Indicator_Name
FROM Indicators
ORDER BY Indicator_Name;
-- ============================================================
-- QUERY 07
-- Find number of records for each country
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    COUNT(d.Debt_ID) AS Number_of_Records
FROM Countries c
LEFT JOIN Debt_Data d
    ON c.Country_Code = d.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Number_of_Records DESC;
-- ============================================================
-- QUERY 08
-- Display records where debt is greater than 1 billion USD
-- ============================================================
SELECT
    d.Debt_ID,
    c.Country_Full_Name AS Country,
    i.Indicator_Name AS Indicator,
    d.Year,
    d.Debt_Value
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
WHERE d.Debt_Value > 1000000000
ORDER BY d.Debt_Value DESC;
-- ============================================================
-- QUERY 09
-- Find minimum, maximum and average debt values
-- ============================================================
SELECT
    MIN(Debt_Value) AS Minimum_Debt,
    MAX(Debt_Value) AS Maximum_Debt,
    AVG(Debt_Value) AS Average_Debt
FROM Debt_Data;
-- ============================================================
-- QUERY 10
-- Count total number of records
-- ============================================================
SELECT
    COUNT(*) AS Total_Records
FROM Debt_Data;
-- ============================================================
-- INTERMEDIATE QUERIES
-- ============================================================
-- QUERY 11
-- Find total debt for each country
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Total_Debt DESC;
-- ============================================================
-- QUERY 12
-- Top 10 countries with highest total debt
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Total_Debt DESC
LIMIT 10;
-- ============================================================
-- QUERY 13
-- Average debt per country
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    AVG(d.Debt_Value) AS Average_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Average_Debt DESC;
-- ============================================================
-- QUERY 14
-- Calculate total debt for each indicator
-- ============================================================
SELECT
    i.Indicator_Name AS Indicator,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
GROUP BY
    i.Series_Code,
    i.Indicator_Name
ORDER BY Total_Debt DESC;
-- ============================================================
-- QUERY 15
-- Identify indicator contributing highest total debt
-- ============================================================
SELECT
    i.Indicator_Name AS Indicator,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
GROUP BY
    i.Series_Code,
    i.Indicator_Name
ORDER BY Total_Debt DESC
LIMIT 1;
-- ============================================================
-- QUERY 16
-- Find country with lowest total debt
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Total_Debt ASC
LIMIT 1;
-- ============================================================
-- QUERY 17
-- Total debt for each country and indicator combination
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    i.Indicator_Name AS Indicator,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name,
    i.Series_Code,
    i.Indicator_Name
ORDER BY Total_Debt DESC;
-- ============================================================
-- QUERY 18
-- Count how many indicators each country has
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    COUNT(DISTINCT d.Series_Code) AS Number_of_Indicators
FROM Countries c
LEFT JOIN Debt_Data d
    ON c.Country_Code = d.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Number_of_Indicators DESC;
-- ============================================================
-- QUERY 19
-- Countries whose total debt is above global average
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
HAVING SUM(d.Debt_Value) >
(
    SELECT AVG(country_total)
    FROM
    (
        SELECT SUM(Debt_Value) AS country_total
        FROM Debt_Data
        GROUP BY Country_Code
    ) AS country_totals
)
ORDER BY Total_Debt DESC;
-- ============================================================
-- QUERY 20
-- Rank countries based on total debt
-- ============================================================
SELECT
    Country,
    Total_Debt,
    RANK() OVER (
        ORDER BY Total_Debt DESC
    ) AS Debt_Rank
FROM
(
    SELECT
        c.Country_Full_Name AS Country,
        SUM(d.Debt_Value) AS Total_Debt
    FROM Debt_Data d
    JOIN Countries c
        ON d.Country_Code = c.Country_Code
    GROUP BY
        c.Country_Code,
        c.Country_Full_Name
) AS country_debt
ORDER BY Debt_Rank;
-- ============================================================
-- ADVANCED QUERIES
-- ============================================================
-- QUERY 21
-- Top 5 indicators contributing most to global debt
-- ============================================================
SELECT
    i.Indicator_Name AS Indicator,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
GROUP BY
    i.Series_Code,
    i.Indicator_Name
ORDER BY Total_Debt DESC
LIMIT 5;
-- ============================================================
-- QUERY 22
-- Percentage contribution of each country
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt,
    ROUND(
        SUM(d.Debt_Value) /
        (
            SELECT SUM(Debt_Value)
            FROM Debt_Data
        ) * 100,
        2
    ) AS Percentage_of_Global_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Percentage_of_Global_Debt DESC;
-- ============================================================
-- QUERY 23
-- Top 3 countries for each indicator
-- ============================================================
WITH country_indicator AS
(
    SELECT
        d.Series_Code,
        i.Indicator_Name,
        d.Country_Code,
        c.Country_Full_Name AS Country,
        SUM(d.Debt_Value) AS Total_Debt
    FROM Debt_Data d
    JOIN Countries c
        ON d.Country_Code = c.Country_Code
    JOIN Indicators i
        ON d.Series_Code = i.Series_Code
    GROUP BY
        d.Series_Code,
        i.Indicator_Name,
        d.Country_Code,
        c.Country_Full_Name
),
ranked AS
(
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Series_Code
            ORDER BY Total_Debt DESC
        ) AS Country_Rank
    FROM country_indicator
)
SELECT
    Indicator_Name,
    Country,
    Total_Debt,
    Country_Rank
FROM ranked
WHERE Country_Rank <= 3
ORDER BY
    Indicator_Name,
    Country_Rank;
-- ============================================================
-- QUERY 24
-- Difference between maximum and minimum debt for each country
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    MAX(d.Debt_Value) AS Maximum_Debt,
    MIN(d.Debt_Value) AS Minimum_Debt,
    MAX(d.Debt_Value) - MIN(d.Debt_Value) AS Debt_Difference
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Debt_Difference DESC;
-- ============================================================
-- QUERY 25
-- Create a view for top 10 countries with highest debt
-- ============================================================
CREATE OR REPLACE VIEW top_10_countries_debt AS
SELECT
    c.Country_Code,
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
ORDER BY Total_Debt DESC
LIMIT 10;

SELECT *
FROM top_10_countries_debt;
-- ============================================================
-- QUERY 26
-- Categorize countries into High, Medium and Low Debt
--
-- Thresholds:
-- High   >= 100 billion
-- Medium >= 10 billion
-- Low    < 10 billion
-- ============================================================
SELECT
    Country,
    Total_Debt,
    CASE
        WHEN Total_Debt >= 100000000000
            THEN 'High Debt'
        WHEN Total_Debt >= 10000000000
            THEN 'Medium Debt'
        ELSE 'Low Debt'
    END AS Debt_Category
FROM
(
    SELECT
        c.Country_Full_Name AS Country,
        SUM(d.Debt_Value) AS Total_Debt
    FROM Debt_Data d
    JOIN Countries c
        ON d.Country_Code = c.Country_Code
    GROUP BY
        c.Country_Code,
        c.Country_Full_Name
) AS country_debt
ORDER BY Total_Debt DESC;
-- ============================================================
-- QUERY 27
-- Cumulative debt per country using window function
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    d.Year,
    SUM(d.Debt_Value) AS Yearly_Debt,
    SUM(SUM(d.Debt_Value)) OVER (
        PARTITION BY d.Country_Code
        ORDER BY d.Year
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS Cumulative_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    d.Country_Code,
    c.Country_Full_Name,
    d.Year
ORDER BY
    Country,
    d.Year;
-- ============================================================
-- QUERY 28
-- Indicators whose average debt is higher than overall average
-- ============================================================
SELECT
    i.Indicator_Name AS Indicator,
    AVG(d.Debt_Value) AS Average_Debt
FROM Debt_Data d
JOIN Indicators i
    ON d.Series_Code = i.Series_Code
GROUP BY
    i.Series_Code,
    i.Indicator_Name
HAVING AVG(d.Debt_Value) >
(
    SELECT AVG(Debt_Value)
    FROM Debt_Data
)
ORDER BY Average_Debt DESC;
-- ============================================================
-- QUERY 29
-- Countries contributing more than 5% of global debt
-- ============================================================
SELECT
    c.Country_Full_Name AS Country,
    SUM(d.Debt_Value) AS Total_Debt,
    ROUND(
        SUM(d.Debt_Value) /
        (
            SELECT SUM(Debt_Value)
            FROM Debt_Data
        ) * 100,
        2
    ) AS Percentage_of_Global_Debt
FROM Debt_Data d
JOIN Countries c
    ON d.Country_Code = c.Country_Code
GROUP BY
    c.Country_Code,
    c.Country_Full_Name
HAVING
    SUM(d.Debt_Value) /
    (
        SELECT SUM(Debt_Value)
        FROM Debt_Data
    ) * 100 > 5
ORDER BY Percentage_of_Global_Debt DESC;
-- ============================================================
-- QUERY 30
-- Most dominant indicator for each country
-- ============================================================
WITH country_indicator AS
(
    SELECT
        d.Country_Code,
        c.Country_Full_Name AS Country,
        d.Series_Code,
        i.Indicator_Name AS Indicator,
        SUM(d.Debt_Value) AS Total_Debt
    FROM Debt_Data d
    JOIN Countries c
        ON d.Country_Code = c.Country_Code
    JOIN Indicators i
        ON d.Series_Code = i.Series_Code
    GROUP BY
        d.Country_Code,
        c.Country_Full_Name,
        d.Series_Code,
        i.Indicator_Name
),
ranked AS
(
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY Country_Code
            ORDER BY Total_Debt DESC
        ) AS Indicator_Rank
    FROM country_indicator
)
SELECT
    Country,
    Indicator,
    Total_Debt
FROM ranked
WHERE Indicator_Rank = 1
ORDER BY Total_Debt DESC;