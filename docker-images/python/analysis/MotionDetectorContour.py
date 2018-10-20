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
import json


class Point:

    def __init__(self, xcoord=0, ycoord=0):
        self.x = xcoord
        self.y = ycoord


class Rectangle:

    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def intersects(self, other):
        return not (self.top_left.x > other.bottom_right.x or
                    self.bottom_right.x < other.top_left.x or
                    self.top_left.y > other.bottom_right.y or
                    self.bottom_right.y < other.top_left.y)


class MotionDetectorContour:

    mqtt_topic_stream = 'cam/stream'
    mqtt_topic_state = 'state/at_machine'
    mqtt_topic_area = 'state/definition'

    last_frame = None
    laste_state = None
    state_definition = None

    # for debugging
    json_state_definition_dummy = """
        {
            "points": [
                {
                    "name": "Productive_1",
                    "pnt_lft_up": [
                        0,
                        0
                    ],
                    "pnt_rght_dwn": [
                        100,
                        100
                    ]
                },
                {
                    "name": "Productive_2",
                    "pnt_lft_up": [
                        250,
                        250
                    ],
                    "pnt_rght_dwn": [
                        350,
                        350
                    ]
                }
            ]
                
        }
    """

    def __init__(self, user_name, user_password, broker_address, debug=False):
        self.debug = debug
        self.broker_address = broker_address
        self.user_name = user_name
        self.user_password = user_password

        self.client = mqtt.Client()
        self.client.username_pw_set(self.user_name, self.user_password)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.broker_address, 1883, 60)

        #if self.debug:
        #    self.state_definition = json.loads(
        #        self.json_state_definition_dummy)

    def run(self):
        self.client.loop_forever()
        # cleanup open windows
        cv2.destroyAllWindows()

    def on_connect(self, client, userdata, flags, rc):
        if self.debug:
            print("Connected with result code " + str(rc))
        self.client.subscribe(self.mqtt_topic_stream)
        self.client.subscribe(self.mqtt_topic_area)

    def parseToJson(self, state):
        data = {
            "state_data": {
                "timestamp": int(time.time() * 1000),
                "state": state
            }
        }
        return json.dumps(data)

    def rectangleInArea(self, x1, y1, x2, y2, pnt_lft_up, pnt_rght_dwn):
        rectangle1 = Rectangle(Point(x1, y1), Point(x2, y2))
        rectangle2 = Rectangle(Point(pnt_lft_up[0], pnt_lft_up[1]), Point(
            pnt_rght_dwn[0], pnt_rght_dwn[1]))
        return rectangle1.intersects(rectangle2)

    def findHuman(self, jpg_as_np):
        frame = cv2.imdecode(jpg_as_np, flags=1)
        state = self.laste_state

        # if the frame could not be grabbed, escape
        if frame is None:
            return

        blur = cv2.GaussianBlur(frame, (15, 15), 0)

        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # TODO find right color range
        lower = np.array([0, 75, 100], dtype="uint8")
        upper = np.array([5, 120, 200], dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)
        res = cv2.bitwise_and(blur, blur, mask=mask)
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

        # if the last frame is None, initialize it
        if self.last_frame is None:
            self.last_frame = res
            return False

        frameDelta = cv2.absdiff(self.last_frame, res)
        thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        humand_detected = False
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 100:  # 5000:  # TODO magic number min area
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the state
            (x, y, w, h) = cv2.boundingRect(c)
            state = 'HUMAN_DETECTED'
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            humand_detected = True
            break

        if humand_detected:
            if self.laste_state != None and self.laste_state != state:
                self.client.publish(self.mqtt_topic_state,
                                    self.parseToJson(state))
            state = 'ts'
            self.laste_state = state

            # show the frame and record if the user presses a key
            if self.debug:
                cv2.namedWindow("Motion Detection")
                cv2.moveWindow("Motion Detection", 0, 0)
                cv2.imshow("Motion Detection", frame)

                cv2.namedWindow("Human Detection")
                cv2.moveWindow("Human Detection", 500, 500)
                cv2.imshow("Human Detection", res)

                cv2.namedWindow("Blur Detection")
                cv2.moveWindow("Blur Detection", 1000, 500)
                cv2.imshow("Blur Detection", blur)

                # needed waitKey to show img - param is time in ms
                cv2.waitKey(1)

        self.last_frame = res

        return humand_detected

    def analyzeImage(self, jpg_as_np):
        frame = cv2.imdecode(jpg_as_np, flags=1)
        state = "Unproductive"

        # if the frame could not be grabbed, escape
        if frame is None:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the last frame is None, initialize it
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
            if cv2.contourArea(c) < 500:  # TODO magic number min area
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the state
            (x, y, w, h) = cv2.boundingRect(c)

            # check if rectangel is in defined area
            # print(self.state_definition)
            if self.state_definition is not None:
                for defined_state in self.state_definition:
                    state = "Productive"
                    if self.rectangleInArea(x, y, x+w, y+h, defined_state['pnt_lft_up'], defined_state['pnt_rght_dwn']):
                        state = defined_state['name']
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                      (255, 255, 0), 2)
                        break
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                      (0, 255, 0), 2)

        # publish state to mqtt broker
        if self.laste_state != None and self.laste_state != state:
            json_string = self.parseToJson(state)
            self.client.publish(self.mqtt_topic_state, json_string)

        # draw the state on the frame
        cv2.putText(frame, "Machine state: {}".format(state), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # show the frame and record if the user presses a key
        if self.debug:
            # check if there are defined areas
            if self.state_definition is not None:
                for defined_state in self.state_definition:
                    cv2.rectangle(frame, (int(defined_state['pnt_lft_up'][0]), int(defined_state['pnt_lft_up'][1])), (
                        int(defined_state['pnt_rght_dwn'][0]), int(defined_state['pnt_rght_dwn'][1])), (255, 0, 0), 2)

            cv2.namedWindow("Motion Detection")
            cv2.moveWindow("Motion Detection", 0, 0)
            cv2.imshow("Motion Detection", frame)

            cv2.namedWindow("Thresh")
            cv2.moveWindow("Thresh", 500, 500)
            cv2.imshow("Thresh", thresh)

            cv2.namedWindow("Frame Delta")
            cv2.moveWindow("Frame Delta", 0, 500)
            cv2.imshow("Frame Delta", frameDelta)

            # needed waitKey to show img - param is time in ms
            cv2.waitKey(1)

        self.last_frame = gray
        self.laste_state = state

    def on_message(self, client, userdata, msg):
        if msg.topic == self.mqtt_topic_area:
            self.state_definition = json.loads(msg.payload.decode("utf-8"))
        elif msg.topic == self.mqtt_topic_stream:
            jpg_original = base64.b64decode(msg.payload)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            # TODO intigrate humandetection
            # if not self.findHuman(jpg_as_np):
            self.analyzeImage(jpg_as_np)
        else:
            if self.debug:
                print('ELSE: ' + msg.payload)


mqtt_user_name = 'user'
mqtt_user_pw = 'password'
mqtt_broker_ip = '10.48.153.110'

mdc = MotionDetectorContour(
    mqtt_user_name, mqtt_user_pw, mqtt_broker_ip, debug=True)

mdc.run()
