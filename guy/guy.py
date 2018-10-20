#!/usr/bin/env python

import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture("mov.MOV")
ret, frame = cap.read()
blur = cv2.GaussianBlur(frame, (21, 21), 0)

hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

lower = np.array([0, 75, 100], dtype = "uint8")
upper = np.array([5, 120, 200], dtype = "uint8")

mask = cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(blur,blur, mask=mask)
last_frame = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

while(cap.isOpened()):

    ret, frame = cap.read()
    blur = cv2.GaussianBlur(frame, (21, 21), 0)

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 75, 100], dtype = "uint8")
    upper = np.array([5, 120, 200], dtype = "uint8")

    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(blur,blur, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    frameDelta = cv2.absdiff(last_frame, res)
    last_frame = res
    thresh = cv2.threshold(frameDelta, 20, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 5000:  # TODO magic number min area
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the state
        (x, y, w, h) = cv2.boundingRect(c)
        print(cv2.contourArea(c))

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame',frame)
    cv2.imshow('res',res)

    cv2.waitKey(20)

cap.release()
cv2.destroyAllWindows()