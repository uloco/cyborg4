#!/usr/bin/env python

from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import paho.mqtt.client as mqtt
import base64
import numpy as np


class MotionDetectorContour:
    
    last_frame = None

    def __init__(self, user_name, user_password, broker_address, debug=False):
        self.debug = debug
        self.broker_address = broker_address
        self.user_name = user_name
        self.user_password = user_password

    def run(self):
        client = mqtt.Client()
        client.username_pw_set(self.user_name, self.user_password)
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect(self.broker_address, 1883, 60)

        client.loop_forever()

        # cleanup open windows
        #cv2.destroyAllWindows()

    def on_connect(self, client, userdata, flags, rc):
        if(self.debug):
            print("Connected with result code " + str(rc))
        client.subscribe("cam/stream")

    def on_message(self, client, userdata, msg):
        jpg_original = base64.b64decode(msg.payload)
        jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        frame = cv2.imdecode(jpg_as_np, flags=1)
        text = "Unproductive"

        # if the frame could not be grabbed, escape
        if frame is None:
            return

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if self.last_frame is None:
            self.last_frame = gray
            return

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(self.last_frame, gray)
        thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:  # TODO magic numver min area
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Productive"

        # draw the state on the frame
        cv2.putText(frame, "Machine state: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the frame and record if the user presses a key
        if(self.debug):
            """ cv2.namedWindow("Motion Detection")
            cv2.moveWindow("Motion Detection", 0, 0)
            cv2.imshow("Motion Detection", frame)

            cv2.namedWindow("Thresh")
            cv2.moveWindow("Thresh", 500, 500)
            cv2.imshow("Thresh", thresh)

            cv2.namedWindow("Frame Delta")
            cv2.moveWindow("Frame Delta", 0, 500)
            cv2.imshow("Frame Delta", frameDelta) """

        self.last_frame = gray

        # needed waitKey to show img - param is time in ms
        cv2.waitKey(1)


mdc = MotionDetectorContour('user', 'password', '10.48.26.128', debug=False)
mdc.run()
