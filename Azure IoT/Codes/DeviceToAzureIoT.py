# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
from random import randint
import datetime
import time
import uuid
import json
import requests
from pytz import timezone 
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

# The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

# import dateutil.tz

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
    return json.dumps(details)

def callAPI(lat, lon):
    URL = "https://api.openweathermap.org/data/2.5/onecall"
    # location given here
    # UW2 location
    exclude = "minutely,hourly,current"
    appid = ""
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'lat': lat,
              'lon': lon,
              'exclude': exclude,
              'appid': appid}
    # sending get request and saving the detailsponse as detailsponse object
    r = requests.get(url = URL, params = PARAMS)
    return r.json()


# os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
# The client object is used to interact with your Azure IoT hub.
device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

# Connect the client.
device_client.connect()

# send 2 messages with 2 system properties & 1 custom property with a 1 second pause between each message

print("sending message")
data = lambda_handler(callAPI(30.613701, -200.190933))
msg = Message(data=data)
msg.message_id = uuid.uuid4()
msg.correlation_id = "correlation-1234"
msg.custom_properties["Power Outage"] = "yes"
msg.content_encoding = "utf-8"
msg.content_type = "application/json"
print(msg)
device_client.send_message(msg)
time.sleep(1)


# # finally, shut down the client
device_client.shutdown()
