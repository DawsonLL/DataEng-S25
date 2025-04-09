import requests

response = requests.get("https://api.thecatapi.com/")
#print(response.text)

response = requests.get("https://api.thecatapi.com/v1/breeds")
#print(response.text)
#print(response)
#print(response.status_code)
#print(response.headers)
#print(response.request)

endpoint = "https://api.thecatapi.com/v1/breeds/search"
query_params = {"q":"ragamuffin"}
request = requests.get(endpoint, params=query_params).json()
print(request)