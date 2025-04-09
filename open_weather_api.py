import requests, json

api_key = "API_KEY_HERE"

# url for current weather
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# url for forecast information
forecast_url = "http://api.openweathermap.org/data/2.5/forecast?"

# grab city name from user
city_name = "Portland"

complete_url = base_url + "appid=" + api_key + "&q=" + city_name
forecast_complete_url = forecast_url + "appid=" + api_key + "&q=" + city_name + ",OR,US"

# get method of requests module
# return response object
response = requests.get(complete_url)
forecast_response = requests.get(forecast_complete_url)

# json method of response object 
# convert json format data into
# python format data
weather_json = response.json()
forecast_json = forecast_response.json()

# Now x contains list of nested dictionaries
# Check the value of "cod" key is equal to
# "404", means city is found otherwise,
# city is not found
if weather_json["cod"] != "404":

    # store the value of "main"
    # key in variable y
    y = weather_json["main"]

    # store the value of "weather"
    # key in variable z
    z = weather_json["weather"]

    # store the value corresponding 
    # to the "main" key at 
    # the 0th index of z 
    weather = z[0]["main"]

    # Determine if it is currently raining in Portland, OR
    print("A. Is it raining in Portland, OR right now?")
    if(weather == "Rain"):
        print("Yes.")
    else:
        print("No.")
    print("Here is the current weather: ", weather)

    willRain = False
    print("Is it forecasted to be raining in Portland within the next three days?")
    for date in forecast_json["list"]:
        if date["weather"][0]["main"] == "Rain":
            willRain = True
            print("It will rain on this day: ", date["dt_txt"])

    if willRain == False:
        print("It will not rain in Portland, OR within the next three days.")
        