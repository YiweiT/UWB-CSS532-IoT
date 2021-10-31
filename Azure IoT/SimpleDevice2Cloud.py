# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
# import asyncio
from azure.iot.device import IoTHubDeviceClient


def main():
    # The connection string for a device should never be stored in code. For the sake of simplicity we're using an environment variable here.
    conn_str = "HostName=YiweiTu-PC.azure-devices.net;DeviceId=YiweiTWinPC;SharedAccessKey=NFRGuejL6Gwb55kLBKWNyqXWTIGuC+2qwvkORn9uGtg="
    # ("IOTHUB_DEVICE_CONNECTION_STRING")
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # Connect the client.
    device_client.connect()

    # Send a single message
    print("Sending message...")
    device_client.send_message("This is a message that is being sent")
    print("Message successfully sent!")

    # Finally, shut down the client
    device_client.shutdown()


if __name__ == "__main__":
    main()

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()
