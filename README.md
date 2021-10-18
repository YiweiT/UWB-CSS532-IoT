# UWB-CSS532-IoT
In this assignment, you need to create an AWS account, install AWS SDK onto your laptop, and implement a virtual IoT system using AWS and your laptop. The system shall support the following features (you may want to implement them step by step).

You are required to use **Python** as the programming language.
## Requirements:

1. Configure your laptop as an IoT device, which can communicate with AWS IoT.
2. Configure AWS IoT to receive messages from your device (laptop) and show the result in the AWS IoT console.
3. Configure AWS IoT to automatically respond to messages sent from your device (laptop), and your device can display the received responses. You may use the "republish feature" provided by AWS IoT.
4. Configure AWS IoT to take user commands (input through cloud console) and send user commands to your device (laptop). Your device shall respond to the command by automatically sending some messages back to AWS (not simply echoing!). Using the feature that you should have implemented in Step 2, the response from your device shall be displayed in the AWS IoT console.
5. Connect AWS Lambda to your AWS IoT to process received messages (e.g., modify the data, average the data, etc.) from devices and save the raw data (the data shall be abstracted from received messages) and the processed data (done by your Lambda) into S3.

## Tips:
Please pay attention to the QoS level in your AWS IoT setup, as well as in your coding. Sometimes, setting QoS level 1 may help resolve unreliable data delivery issues.
