"""Solution — Exercise 2: Cleaning a messy income statement"""

import pandas as pd

# Task 1
df = pd.read_csv("data/income_statement.csv")
print("Raw columns:", df.columns.tolist())
print(df.head())

# Task 2
df.columns = (df.columns
              .str.strip()
              .str.lower()
              .str.replace(r"[\s\(\)$&/]+", "_", regex=True)
              .str.replace(r"_+", "_", regex=True)
              .str.strip("_"))
print("\nCleaned columns:", df.columns.tolist())

# Task 3
numeric_cols = [c for c in df.columns if c != "fiscal_year"]
for col in numeric_cols:
    df[col] = (df[col]
               .astype(str)
               .str.replace(r"[$,M\s]", "", regex=True)
               .replace("None", pd.NA)
               .astype(float))

# Task 4
# Fill with median — dropping the row loses a full year of data; imputing is
# reasonable for a single interior missing value in a small time series.
median_interest = df["interest_expense"].median()
df["interest_expense"] = df["interest_expense"].fillna(median_interest)
print("\nAfter fill:\n", df)

# Task 5
df["gross_margin_pct"] = ((df["revenue_m"] - df["cost_of_goods_sold"]) / df["revenue_m"] * 100).round(2)
df["ebit"]             = df["revenue_m"] - df["cost_of_goods_sold"] - df["sg_a_expenses"]
df["interest_coverage"] = (df["ebit"] / df["interest_expense"]).round(2)
print("\nFinal table:\n", df[["fiscal_year","gross_margin_pct","ebit","interest_coverage"]])

# Bonus
print("\nHighest gross margin year:", df.loc[df["gross_margin_pct"].idxmax(), "fiscal_year"])
print("Lowest  gross margin year:", df.loc[df["gross_margin_pct"].idxmin(), "fiscal_year"])
