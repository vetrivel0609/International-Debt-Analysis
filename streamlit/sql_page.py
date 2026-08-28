import streamlit as st
import pandas as pd
from db import get_connection


# ============================================================
# INTERNATIONAL DEBT ANALYSIS
# SQL ANALYTICAL QUESTIONS
# ============================================================

def sql_page():

    st.title("🌍 International Debt Analysis")

    st.write(
        "Explore the international debt dataset using 30 SQL analytical questions."
    )

    conn = get_connection()


    # ========================================================
    # 30 SQL ANALYTICAL QUESTIONS
    # ========================================================

    queries = {

        # ====================================================
        # BASIC QUERIES
        # ====================================================

        "1. Retrieve all distinct country names from the dataset":
        """
        SELECT DISTINCT Country_Full_Name AS Country
        FROM Countries
        ORDER BY Country_Full_Name;
        """,

        "2. Count the total number of countries available":
        """
        SELECT COUNT(*) AS Total_Countries
        FROM Countries;
        """,

        "3. Find the total number of indicators present":
        """
        SELECT COUNT(*) AS Total_Indicators
        FROM Indicators;
        """,

        "4. Display the first 10 records of the dataset":
        """
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
        """,

        "5. Calculate the total global debt":
        """
        SELECT
            SUM(Debt_Value) AS Total_Global_Debt
        FROM Debt_Data;
        """,

        "6. List all unique indicator names":
        """
        SELECT DISTINCT Indicator_Name AS Indicator
        FROM Indicators
        ORDER BY Indicator_Name;
        """,

        "7. Find the number of records for each country":
        """
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
        """,

        "8. Display all records where debt is greater than 1 billion USD":
        """
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
        """,

        "9. Find the minimum, maximum, and average debt values":
        """
        SELECT
            MIN(Debt_Value) AS Minimum_Debt,
            MAX(Debt_Value) AS Maximum_Debt,
            AVG(Debt_Value) AS Average_Debt
        FROM Debt_Data;
        """,

        "10. Count total number of records in the dataset":
        """
        SELECT COUNT(*) AS Total_Records
        FROM Debt_Data;
        """,


        # ====================================================
        # INTERMEDIATE QUERIES
        # ====================================================

        "11. Find the total debt for each country":
        """
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
        """,

        "12. Display the top 10 countries with the highest total debt":
        """
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
        """,

        "13. Find the average debt per country":
        """
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
        """,

        "14. Calculate total debt for each indicator":
        """
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
        """,

        "15. Identify the indicator contributing the highest total debt":
        """
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
        """,

        "16. Find the country with the lowest total debt":
        """
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
        """,

        "17. Calculate total debt for each country and indicator combination":
        """
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
        """,

        "18. Count how many indicators each country has":
        """
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
        """,

        "19. Display countries whose total debt is above the global average":
        """
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
                SELECT
                    SUM(Debt_Value) AS country_total
                FROM Debt_Data
                GROUP BY Country_Code
            ) AS country_totals
        )
        ORDER BY Total_Debt DESC;
        """,

        "20. Rank countries based on total debt":
        """
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
        """,


        # ====================================================
        # ADVANCED QUERIES
        # ====================================================

        "21. Find the top 5 indicators contributing most to global debt":
        """
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
        """,

        "22. Calculate percentage contribution of each country to total global debt":
        """
        SELECT
            c.Country_Full_Name AS Country,
            SUM(d.Debt_Value) AS Total_Debt,
            ROUND(
                SUM(d.Debt_Value) /
                (SELECT SUM(Debt_Value)
                 FROM Debt_Data) * 100,
                2
            ) AS Percentage_of_Global_Debt
        FROM Debt_Data d
        JOIN Countries c
            ON d.Country_Code = c.Country_Code
        GROUP BY
            c.Country_Code,
            c.Country_Full_Name
        ORDER BY Percentage_of_Global_Debt DESC;
        """,

        "23. Identify the top 3 countries for each indicator based on debt":
        """
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
            Indicator_Name AS Indicator,
            Country,
            Total_Debt,
            Country_Rank
        FROM ranked
        WHERE Country_Rank <= 3
        ORDER BY
            Indicator,
            Country_Rank;
        """,

        "24. Find the difference between maximum and minimum debt for each country":
        """
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
        """,

        "25. Create a view for the top 10 countries with highest debt":
        """
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
        """,

        "26. Categorize countries into High Debt, Medium Debt and Low Debt":
        """
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
        """,

        "27. Calculate cumulative debt per country using window functions":
        """
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
        """,

        "28. Find indicators where average debt is higher than overall average debt":
        """
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
        """,

        "29. Identify countries contributing more than 5% of global debt":
        """
        SELECT
            c.Country_Full_Name AS Country,
            SUM(d.Debt_Value) AS Total_Debt,

            ROUND(
                SUM(d.Debt_Value) /
                (SELECT SUM(Debt_Value)
                 FROM Debt_Data) * 100,
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
            (SELECT SUM(Debt_Value)
             FROM Debt_Data) * 100 > 5

        ORDER BY Percentage_of_Global_Debt DESC;
        """,

        "30. Find the most dominant indicator for each country":
        """
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
        """
    }


    # ========================================================
    # QUERY SELECTION
    # ========================================================

    selected = st.selectbox(
        "Choose Query",
        list(queries.keys())
    )


    # ========================================================
    # EXECUTE QUERY
    # ========================================================

    if st.button(
        "Execute Query",
        use_container_width=True,
        type="primary"
    ):

        try:

            # ------------------------------------------------
            # QUERY 25 - CREATE VIEW
            # ------------------------------------------------

            if selected.startswith(
                "25. Create a view"
            ):

                cursor = conn.cursor()

                cursor.execute(
                    queries[selected]
                )

                conn.commit()

                cursor.close()

                # Read the newly created view
                df = pd.read_sql(
                    """
                    SELECT *
                    FROM top_10_countries_debt;
                    """,
                    conn
                )

            else:

                df = pd.read_sql(
                    queries[selected],
                    conn
                )


            # ------------------------------------------------
            # SUCCESS MESSAGE
            # ------------------------------------------------

            st.success(
                "✅ Query executed successfully."
            )


            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            st.subheader("Answer")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


            st.caption(
                f"Rows returned: {len(df):,}"
            )


        except Exception as e:

            st.error(
                "Unable to execute the selected query."
            )

            st.error(str(e))


        finally:

            conn.close()