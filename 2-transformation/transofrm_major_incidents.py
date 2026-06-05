import pandas as pd
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw", "major_incidents.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "processed", "major_incidents_clean.csv")

DAY_TYPE_MAP = {
    1: "Weekday",
    2: "Weekend"
}

def transform_major_incidents():
    print(f"Transforming major_incidents dataset...")

    df = pd.read_csv(INPUT_PATH)
    print(f"Rows loaded: {len(df)}")

    # Drop rows with missing division or line value
    df = df.dropna(subset=["division", "line"])
    print(f"Rows loaded after dropping rows with missing division and/or line: {len(df)}")

    # Convert month column to datetime type
    df["month"] = pd.to_datetime(df["month"], errors="coerce")

    # Update day type to "Weekday"/"Weekend" instead of "1" and "2"
    df["day_type"] = df["day_type"].map(DAY_TYPE_MAP)

    # Rename columns for clarity
    df = df.rename(columns={
        "count": "incident_count",
        "category": "incident_category"
    })

    # Add year and month columns for easier analysis
    df["year"] = df["month"].dt.year
    df["month_number"] = df["month"].dt.month

    # Standardize division and line labels
    df["division"] = df["division"].str.strip().str.upper()
    df["line"] = df["line"].str.strip().str.upper()

    # Sort by month and line
    df = df.sort_values(["month", "line"]).reset_index(drop=True)
    print(df.head(10))

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Rows saved {len(df)} to {OUTPUT_PATH}")



if __name__ == "__main__":
    transform_major_incidents()
    
