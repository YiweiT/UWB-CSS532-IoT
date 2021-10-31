from paho.mqtt import client as mqtt
import time
import ssl
import calendar
import datetime
import json
import random

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed for m" + str(mid))

def on_connection(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_log(client, userdata, level, buf):
    print("log: " + buf)

device_id = ""
iot_hub_name = ""
sas_token = ""
client = mqtt.Client(client_id=device_id, protocol=mqtt.MQTTv311, clean_session=False)
client.on_log = on_log
client.tls_set_context(context=None)

# set up client credential
username = "{}.azure-devices.net/{}/api-version=2018-06-30".format(iot_hub_name, device_id)
client.username_pw_set(username=username, password=sas_token)

# connect to the Azure IoT Hub
client.on_connect = on_connection
client.connect(iot_hub_name + ".azure-devices.net", port=8883)

# publish
time.sleep(1)

msg = {
        "temperature": 28,
        "humidity": 80,
        "barometer": 1013,
        "wind": {
            "velocity": 22,
            "bearing": 255
            }
        }

data_out = json.dumps(msg)
client.publish("devices/{device_id}/messages/events/".format(device_id = device_id), payload=data_out, qos=1, retain=False)
print("Publishing on devices/" + device_id + "/messages/events/" + data_out)
time.sleep(1)
