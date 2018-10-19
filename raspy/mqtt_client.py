#!/usr/bin/env python
import time
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt

cap = cv2.VideoCapture(0)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
client = mqtt.Client()
client.on_connect = on_connect

client.connect("10.48.149.123", 1883, 60)

client.loop_start()

while True:
    retval, image = cap.read()
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    client.publish("cam/stream", jpg_as_text)