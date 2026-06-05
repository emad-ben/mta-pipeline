import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw")

DATASETS = {
    "major_incidents": "major_incidents.csv",
    "delay_causing_incidents": "delay_causing_incidents.csv",
    "service_delivered": "service_delivered.csv",
    "daily_ridership": "daily_ridership.csv"
}

def print_header(title, width=60):
    print("=" * width)
    print(title.upper().center(width))
    print("=" * width)

def print_subheader(title, width=30):
    print("-" * width)
    print(title.upper().center(width))
    print("-" * width)

def explore_dataset(name, filename):
    """
    Add function signature here
    """
    path = os.path.join(DATA_DIR, filename)
    df = pd.read_csv(path)

    print_header(name)
    print(f"Row count:    {df.shape[0]}")
    print(f"Column count: {df.shape[1]}")

    # Column names & types
    print_subheader("columns")
    print(df.dtypes.to_string())

    # Missing value analysis per column
    print_subheader("missing values")
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        print(f"No missing values found")
    else:
        print(missing.to_string())
    
    # Peak at first 3 rows
    print_subheader("first 3 rows")
    sample = df.sample(3)
    print(sample.to_string())

    # Show date ranges for applicable columns (if found)
    print_subheader("date range(s)")
    for col in df.columns:
        if "date" in col.lower() or "year" in col.lower() or "month" in col.lower():
            try:
                parsed = pd.to_datetime(df[col])
                print(f"{col}: {parsed.min()} - {parsed.max()}")
            except:
                print(f"{col}: could not parse as date")

def main():
    for name, filename in DATASETS.items():
        explore_dataset(name, filename)


if __name__ == "__main__":
    main()
  