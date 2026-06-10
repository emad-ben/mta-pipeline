import pandas as pd
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw", "daily_ridership.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "processed", "daily_ridership_clean.csv")

def transform_daily_ridership():
    # Load
    df = pd.read_csv(INPUT_PATH)
    print(f"ROWS LOADED: {len(df)}")

    # Convert date column from type object to type datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # only want subway columns
    df = df[[
        "date",
        "subways_total_estimated_ridership",
        "subways_of_comparable_pre_pandemic_day"
    ]]

    # Make column names more intuitive
    df = df.rename(columns={
        "subways_total_estimated_ridership": "daily_ridership",
        "subways_of_comparable_pre_pandemic_day": "pct_of_prepandemic"
    })

    df["year"] = df["date"].dt.year
    df["month_number"] = df["date"].dt.month

    # Aggregate data to be at the granularity of months
    monthly = df.groupby(["year", "month_number"]).agg(
        total_monthly_ridership = ("daily_ridership", "sum"),
        avg_daily_ridership = ("daily_ridership", "mean"),
        avg_pct_of_prepandemic = ("pct_of_prepandemic", "mean"),
        days_recorded = ("daily_ridership", "count")
    ).reset_index()

    # Construct month column to align with other 3 databases
    monthly["month"] = pd.to_datetime(
        monthly[["year", "month_number"]].rename(columns={"month_number": "month"}).assign(day=1)
    )

    # Round float columns
    monthly["avg_daily_ridership"] = monthly["avg_daily_ridership"].round(0)
    monthly["avg_pct_of_prepandemic"] = monthly["avg_pct_of_prepandemic"].round(4)

    # Reorder columns
    monthly = monthly[[
        "month", "year", "month_number",
        "total_monthly_ridership",
        "avg_daily_ridership",
        "avg_pct_of_prepandemic",
        "days_recorded"
    ]]

    # Order rows by month (date column)
    monthly = monthly.sort_values("month").reset_index(drop=True)

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    monthly.to_csv(OUTPUT_PATH, index=False)

    print(f"ROWS SAVED: {len(monthly)}")
    print(f"MIN MONTHLY RIDERSHIP: {(monthly['total_monthly_ridership'].min()):,} (PCT_PP {monthly.loc[monthly['total_monthly_ridership'] == monthly['total_monthly_ridership'].min(), 'avg_pct_of_prepandemic'].iloc[0]})")
    print(f"MAX MONTHLY RIDERSHIP: {(monthly['total_monthly_ridership'].max()):,} (PCT_PP {monthly.loc[monthly['total_monthly_ridership'] == monthly['total_monthly_ridership'].max(), 'avg_pct_of_prepandemic'].iloc[0]})")

    print(monthly.sample(3))

if __name__ == "__main__":
    transform_daily_ridership()
