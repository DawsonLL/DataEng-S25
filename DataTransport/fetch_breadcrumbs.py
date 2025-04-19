import requests
import json

vehicle_ids = ["2902", "2904"]  # replace with your assigned IDs
all_data = []

for vid in vehicle_ids:              
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    response = requests.get(url)
    if response.ok:
        all_data.extend(response.json())

with open("bcsample.json", "w") as f:
    json.dump(all_data, f, indent=2)