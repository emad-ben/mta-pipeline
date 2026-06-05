import pandas as pd
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw", "delay_causing_incidents.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "processed", "delay_causing_incidents_clean.csv")

DAY_TYPE_MAP = {
    1: "Weekday",
    2: "Weekend"
}

def transform_delay_causing_incidents():
    df = pd.read_csv(INPUT_PATH)
    print(f"Rows loaded to DF from raw CSV: {len(df)}")

    # Decode day_type (represents weekday as 1 and weekend as 2)
    df["day_type"] = df["day_type"].map(DAY_TYPE_MAP)

    # Convert month column to datetime dtype
    df["month"] = pd.to_datetime(df["month"], errors="coerce")

    # Fill missing reporting_category values with "Unknown"
    before = df["reporting_category"].isna().sum()
    df.fillna({"reporting_category": "Unknown"}, inplace=True)
    print(f"Filled {before} missing reporting_category values with 'Unknown'")

    # Renaming columns with ambiguous names
    df = df.rename(columns={
        "incidents": "incident_count",
        "reporting_category": "delay_category"
    })

    # Adding year and month columns
    df["year"] = df["month"].dt.year
    df["month_number"] = df["month"].dt.month

    # Standardize division and line labels
    df["division"] = df["division"].str.strip().str.upper()
    df["line"] = df["line"].str.strip().str.upper()

    # Sort by month and line
    df = df.sort_values(["month", "line"]).reset_index(drop=True)

    # Save as CSV file
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Rows saved to cleaned CSV: {len(df)}")

    # Quick peak at transformed dataset
    pass

if __name__ == "__main__":
    transform_delay_causing_incidents()