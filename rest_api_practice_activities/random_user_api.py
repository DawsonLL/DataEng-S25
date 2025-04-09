import requests

request = requests.get("https://randomuser.me/api/")
#print(request)

request = requests.get("https://randomuser.me/api/").json()
#print(request)

# Send an API request for a random female user
request = requests.get("https://randomuser.me/api/?gender=female").json()
#print(request)

# Send a request for a random female user from Germany
request = requests.get("https://randomuser.me/api/?gender=female&nat=de").json()
#print(request)

# To avoid having to rebuild the URL over and over again, we can use the params attribute instead
query_params = {"gender":"female", "nat":"de"}
request = requests.get("https://randomuser.me/api/", params=query_params).json()

