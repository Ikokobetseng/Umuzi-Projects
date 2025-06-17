
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\IkayR\Downloads\Northwind.sqlite"

def run_query(query, db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query(query, conn)
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return pd.DataFrame()

# Part 1: Customer Orders

query = """
WITH RankedOrders AS (
  SELECT 
    c.CustomerID,
    c.CompanyName,
    o.OrderDate,
    ROW_NUMBER() OVER (PARTITION BY c.CustomerID ORDER BY o.OrderDate DESC) AS LatestOrderRank,
    MIN(o.OrderDate) OVER (PARTITION BY c.CustomerID) AS FirstOrderDate
  FROM 
    Customers c
  JOIN 
    Orders o ON c.CustomerID = o.CustomerID
)
SELECT 
  CustomerID,
  CompanyName,
  DATE(OrderDate) AS LatestOrderDate,
  ROUND(JULIANDAY(OrderDate) - JULIANDAY(FirstOrderDate)) AS DaysSinceFirstOrder
FROM 
  RankedOrders
WHERE 
  LatestOrderRank = 1;
"""

result = run_query(query)
print(result)


#Part 2: Customer Segmentation with Data Transformation


query = """
WITH CustomerTotalRevenue AS (
  SELECT 
    c.CustomerID,
    c.CompanyName,
    SUM(od.UnitPrice * od.Quantity) AS TotalRevenue
  FROM 
    Customers c
  JOIN 
    Orders o ON c.CustomerID = o.CustomerID
  JOIN 
    `Order Details` od ON o.OrderID = od.OrderID
  GROUP BY 
    c.CustomerID, c.CompanyName
)
SELECT 
  CustomerID,
  CompanyName,
  ROUND(TotalRevenue, 2) AS TotalRevenue,
  CASE 
    WHEN TotalRevenue > 10000 THEN 'High Value'
    WHEN TotalRevenue BETWEEN 5000 AND 10000 THEN 'Mid Value'
    ELSE 'Low Value'
  END AS CustomerSegment
FROM 
  CustomerTotalRevenue
ORDER BY 
  TotalRevenue DESC
LIMIT 15;
"""

result = run_query(query)
print(result)
