CREATE DATABASE international_debt_db;
USE international_debt_db;
/**create Countries table**/
CREATE TABLE Countries (
    Country_Code VARCHAR(10) PRIMARY KEY,
    Country_Full_Name VARCHAR(255),
    Income_Group VARCHAR(100),
    Region VARCHAR(100),
    Lending_Category VARCHAR(100),
    Currency_Unit VARCHAR(100),
    External_Debt_Reporting_Status VARCHAR(100));
DESCRIBE Countries;
/**create Indicators table**/
CREATE TABLE Indicators (
    Series_Code VARCHAR(50) PRIMARY KEY,
    Indicator_Name VARCHAR(500),
    Short_Definition TEXT,
    Long_Definition TEXT,
    Source VARCHAR(500),
    Topic VARCHAR(255),
    Dataset VARCHAR(255),
    Periodicity VARCHAR(100),
    Aggregation_Method VARCHAR(255));
DESCRIBE Indicators;
/**create Data_Debt table**/
CREATE TABLE Debt_Data (
    Debt_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Country_Code VARCHAR(10) NOT NULL,
    Series_Code VARCHAR(50) NOT NULL,
    Year INT NOT NULL,
    Debt_Value DOUBLE,

    FOREIGN KEY (Country_Code)
        REFERENCES Countries(Country_Code),

    FOREIGN KEY (Series_Code)
        REFERENCES Indicators(Series_Code));
DESCRIBE Debt_Data;