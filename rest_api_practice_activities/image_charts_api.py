import requests

url =  "https://image-charts.com/chart?chs=700x125&cht=ls&chd=t:23,15,28"
response = requests.get(url)

# Stores the fetched image as a png file
with open("chart.png", mode="wb") as file:
    file.write(response.content)