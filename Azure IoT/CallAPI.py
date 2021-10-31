import json
# import dateutil.tz
from pytz import timezone 
# print('Loading function')
import requests
import json
from datetime import datetime
# import boto3

# s3 = boto3.client('s3')

ZERO_K = float(273.15)

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def getMean(arr):
    return round(sum(arr) / len(arr))

def getMedian(arr):
    arr.sort()
    mid = len(arr) // 2
    if len(arr) % 2 == 1:
        return arr[mid]
    else:
        return getMean(arr[mid:mid + 2])

def timestamp2date(rt: int, _timezone):
    tz = timezone(_timezone)
    time = datetime.fromtimestamp(rt, tz)
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    return date

def kelvin2celsius(temp):
    # print(type(temp))
    return round(temp - ZERO_K, 2)

def lambda_handler(event):
    bucket = 'aws-iot-historical-weather'
    daily_data = event["daily"]

    details = dict()
    location_info = {"timezone": event["timezone"],
                     "latitude": event["lat"],
                     "longitude": event["lon"],
                     "temperature_unit": "Celsius"
                    }
    details["location_information"] = location_info
    temp = []
    details["daily"] = {}
    timezone = event["timezone"]
    for day_data in daily_data:

        dt = timestamp2date(day_data["dt"], timezone)
        sunrise_t = timestamp2date(day_data["sunrise"], timezone)
        sunset_t = timestamp2date(day_data["sunset"], timezone)
        day_temp = kelvin2celsius(day_data["temp"]["day"])
        temp.append(day_temp)
        details["daily"][dt] = {"sunrise": sunrise_t,
                   "sunset": sunset_t,
                   "day_temperature": day_temp}


    # temp_max = max(temp)
    # temp_min = min(temp)
    # temp_avg = getMean(temp)
    # temp_median = getMedian(temp)
    # temp_agg = {"temp_max": temp_max,
    #             "temp_min": temp_min,
    #             "temp_avg": temp_avg,
    #             "temp_median": temp_median
    #             }

    # details["temperature_stat"] = temp_agg
    # # format to json file
    # # create a file name and convert dict -> json -> bytes
    # filename = event['lat'] + ", " + event["lon"] + "_historical_weather.json"
    # uploadByteStream = bytes(json.dumps(details).encode('UTF-8'))

    # s3.put_object(Bucket=bucket, key=filename, body=uploadByteStream)
    print(details)
    print("Put Completed!")

def callAPI(lat, lon):
    URL = "https://api.openweathermap.org/data/2.5/onecall"
    # location given here
    # UW2 location
    exclude = "minutely,hourly,current"
    appid = "0fcba73b989318f34faf502dabd76a2f"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'lat': lat,
              'lon': lon,
              'exclude': exclude,
              'appid': appid}
    # sending get request and saving the detailsponse as detailsponse object
    r = requests.get(url = URL, params = PARAMS)
    return r.json()

if __name__ == "__main__":
    
    lambda_handler(callAPI(47.613701, -122.190933))