import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from transform_major_incidents import transform_major_incidents
from transform_delay_causing_incidents import transform_delay_causing_incidents
from transform_service_delivered import transform_service_delivered
from transform_daily_ridership import transform_daily_ridership

def run_all():
    print("=" * 60)
    print("RUN ALL MTA DATASET TRANSFORMATIONS")
    print("=" * 60)
    print()

    steps = [
        ("1. MAJOR INCIDENTS", transform_major_incidents),
        ("2. DELAY CAUSING INCIDENTS", transform_delay_causing_incidents),
        ("3. SERVICE DELIVERED", transform_service_delivered),
        ("4. DAILY RIDERSHIP", transform_daily_ridership)
    ]

    completed = []
    failed = []

    for name, func in steps:
        print(f"{name}")
        try:
            func()
            completed.append(name)
        except Exception as e:
            print(f"ERROR: {e}")
            failed.append(name)

    print("=" * 60)
    print("TRANSFORMATION SUCCESS LOG")
    print("=" * 60)
    print(f"COMPLETE: {completed}")
    print(f"FAILED: {failed}")
    

if __name__ == "__main__":
    run_all()