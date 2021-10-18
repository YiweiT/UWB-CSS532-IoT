# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.

import argparse
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import sys
import threading
import time
from uuid import uuid4
import json
import requests

ENDPOINT = "a3j171i1vxnhop-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERT = "certs_1/0c733e32fb4112d2300fdb56eec5559b21990d1f328afd296b1ed193373f4aae-certificate.pem.crt"
PATH_TO_KEY = "certs_1/0c733e32fb4112d2300fdb56eec5559b21990d1f328afd296b1ed193373f4aae-private.pem.key"
PATH_TO_ROOT = "certs_1/RootCA1.pem"
MESSAGE = {
  "temperature": 28,
  "humidity": 80,
  "barometer": 1013,
  "wind": {
    "velocity": 22,
    "bearing": 255
  }
}
TOPIC_PUBLISH = "topic/test/toiot/weather"
TOPIC_SUBSCRIBE = "test/republish/todevice/temp_humidity"



received_all_event = threading.Event()

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

# Callback when connection is accidentally lost.
def on_connection_interrupted(connection, error, **kwargs):
    print("Connection interrupted. error: {}".format(error))


# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    print("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

    if return_code == mqtt.ConnectReturnCode.ACCEPTED and not session_present:
        print("Session did not persist. Resubscribing to existing topics...")
        resubscribe_future, _ = connection.resubscribe_existing_topics()

        # Cannot synchronously wait for resubscribe result because we're on the connection's event-loop thread,
        # evaluate result with a callback instead.
        resubscribe_future.add_done_callback(on_resubscribe_complete)


def on_resubscribe_complete(resubscribe_future):
        resubscribe_results = resubscribe_future.result()
        print("Resubscribe results: {}".format(resubscribe_results))

        for topic, qos in resubscribe_results['topics']:
            if qos is None:
                sys.exit("Server rejected resubscribe to topic: {}".format(topic))


# Callback when the subscribed topic receives a message
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload))

    received_all_event.set()

def subscribe(topic_subscribe):
    # Subscribe
    print("Subscribing to topic '{}'...".format(topic_subscribe))
    subscribe_future, packet_id = mqtt_connection.subscribe(
        topic=topic_subscribe,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received)

    subscribe_result = subscribe_future.result()
    print("Subscribed with {}".format(str(subscribe_result['qos'])))

def publish(topic_publish, message):
    print('Begin Publish')

    mqtt_connection.publish(topic=topic_publish, payload=json.dumps(message), qos=mqtt.QoS.AT_LEAST_ONCE)
    print("Published: '" + json.dumps(message) + "' to the topic: " + topic_publish)
    time.sleep(1)
    print('Publish End')

if __name__ == '__main__':
    # Spin up resources
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)

    proxy_options = None

    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        # port=args.port,
        cert_filepath=PATH_TO_CERT,
        pri_key_filepath=PATH_TO_KEY,
        client_bootstrap=client_bootstrap,
        ca_filepath=PATH_TO_ROOT,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=CLIENT_ID,
        clean_session=False,
        keep_alive_secs=6
        )

    print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))

    connect_future = mqtt_connection.connect()

    # Future.result() waits until a result is available
    connect_future.result()
    print("Connected!")

    subscribe(TOPIC_SUBSCRIBE)
    publish(TOPIC_PUBLISH, MESSAGE)
    # Wait for all messages to be received.
    # This waits forever if count was set to 0.
    if received_all_event.is_set():
        print("Waiting for all messages to be received...")

    received_all_event.wait()
    print("message(s) received.")

    # Disconnect
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
