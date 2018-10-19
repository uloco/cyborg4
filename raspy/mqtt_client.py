#!/usr/bin/env python
import time
import cv2
import base64
import numpy as np
import paho.mqtt.client as mqtt
import imutils
import datetime

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set("user", password="password")
client.connect("10.48.153.110", 1883, 60)
#client.connect("10.48.26.128", 1883, 60)
#client.connect("10.48.149.123", 1883, 60)

client.loop_start()

bufmillis = int(round(time.time() * 1000))
waitms = 100
while True:
    retval, image = cap.read()
    millis = int(round(time.time() * 1000))
    if (bufmillis + waitms <= millis):
        bufmillis = millis
        #print(datetime.datetime.now())
        image = imutils.resize(image, width=500)
        retval, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        client.publish("cam/stream", jpg_as_text, 0, False)
        cv2.imshow("im", image)
        cv2.waitKey(1)
