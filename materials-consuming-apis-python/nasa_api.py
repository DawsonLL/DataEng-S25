import requests

endpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"

# replace DEMO_KEY if generated own key
api_key = "DEMO_KEY"
query_params = {"api_key": api_key, "earth_date": "2020-07-01", "camera":"fhaz"}
response = requests.get(endpoint, params=query_params)
#print(response.json())

photos = response.json()["photos"]
print(f"Found {len(photos)} photos")
print(photos[2]["img_src"])