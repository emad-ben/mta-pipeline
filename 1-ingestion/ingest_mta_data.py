import requests
import pandas as pd
import os

BASE_URL = "https://data.ny.gov/resource/{}.json"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "0-data", "raw")

DATASETS = {
    "major_incidents": "ereg-mcvp",
    "delay_causing_incidents": "g937-7k7c",
    "service_delivered": "32ch-sei3",
    "daily_ridership": "vxuj-8kew"
}

LIMIT = 50_000

def download_dataset(name, dataset_id):
    """
    Downloads a full dataset from the NY Open Data (Socrata) API using
    paginated requests and saves it as a CSV.

    The function fetches data in batches using Socrata’s `$limit` and `$offset`
    parameters until no more records are returned. Each response is a list of
    JSON objects (rows), which are accumulated and converted into a DataFrame.

    Parameters
    ----------
    name : str
        Output filename (without extension). Example: "major_incidents"

    dataset_id : str
        Socrata dataset identifier used in the API URL.

    Data Flow
    ---------
    API - paginated JSON batches - list of dicts - pandas DataFrame - CSV

    Example API Record
    ------------------
    {
        "incident_id": "12345",
        "date": "2024-01-01T08:30:00",
        "line": "A",
        "description": "Signal failure"
    }

    Output
    ------
    Saves CSV to:
        data/raw/{name}.csv

    Notes
    -----
    Uses `$limit=50000` and `$offset` for pagination until an empty batch is returned by API.
    """
    print(f"Downloading {name}...")
    all_rows = []
    offset = 0

    while True:
        url = BASE_URL.format(dataset_id)
        params = {"$limit": LIMIT, "$offset": offset}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"ERROR: fetching for {name}")
            break
        
        batch = response.json()
        if not batch:
            break
        
        all_rows.extend(batch)
        offset += LIMIT
        print(f"Retrieved {len(all_rows)} rows so far...")
    
    if all_rows:
        df = pd.DataFrame(all_rows)
        output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Save {len(df)} rows to {output_path}")
    else:
        print(f"Failed to get data for {name}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name, dataset_id in DATASETS.items():
        download_dataset(name, dataset_id)
    print(f"All datasets downloaded successfully")

if __name__ == "__main__":
    main()
