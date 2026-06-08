import pandas as pd
import os

INPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw", "service_delivered.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "0-data", "processed", "service_delivered_clean.csv")

DAY_TYPE_MAP = {
    1: "Weekday",
    2: "Weekend"
}

def transform_service_delivered():
    df = pd.read_csv(INPUT_PATH)
    print(f"Rows loaded: {len(df)}")

    # Add year and month_number columns for easier analysis later
    df["month"] = pd.to_datetime(df["month"], errors="coerce")
    df["year"] = df["month"].dt.year
    df["month_number"] = df["month"].dt.month

    # Decode day type
    df["day_type"] = df["day_type"].map(DAY_TYPE_MAP)

    # Recalculate service_delivered column as a percentage
    df["service_delivered_pct"] = (df["num_actual_trains"] / df["num_sched_trains"]).round(4)
    df.drop(columns=["service_delivered"], inplace=True)

    # Standardize division and label columns
    df["division"] = df["division"].str.strip().str.upper()
    df["line"] = df["line"].str.strip().str.upper()

    # Sort by month and line
    df.sort_values(["month", "line"]).reset_index(drop=True)

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Rows saved to {os.path.basename(OUTPUT_PATH)}: {len(df)}")

    # Some trial analysis on what trains had the best and worst service and when
    min_mask = df["service_delivered_pct"] == df["service_delivered_pct"].min()
    max_mask = df["service_delivered_pct"] == df["service_delivered_pct"].max()
    print(df[min_mask][["year", "month_number", "line", "service_delivered_pct"]].iloc[0].to_dict())
    print(df[max_mask][["year", "month_number", "line", "service_delivered_pct"]].iloc[0].to_dict())

if __name__ == "__main__":
    transform_service_delivered()
