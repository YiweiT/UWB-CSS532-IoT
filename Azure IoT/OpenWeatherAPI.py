import json
import requests

URL = "https://api.openweathermap.org/data/2.5/onecall"
# location given here
# UW2 location
exclude = "minutely,hourly,current"
appid = "0fcba73b989318f34faf502dabd76a2f"
# defining a params dict for the parameters to be sent to the API
PARAMS = {'lat': 47.613701,
            'lon': -122.190933,
            'exclude': exclude,
            'appid': appid}
# sending get request and saving the detailsponse as detailsponse object
r = requests.get(url = URL, params = PARAMS)
print(r.json())