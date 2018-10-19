#!/usr/bin/env python

from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2


class MotionDetectorContour:

    def __init__(self, file_path, ceil=15):
        self.ceil = ceil
        self.file_path = file_path

    def run(self):
        vs = cv2.VideoCapture(self.file_path)

        # initialize the first frame in the video stream
        firstFrame = None

        i = 0
        # loop over the frames of the video
        while (vs.isOpened()):
            # grab the current frame and initialize the occupied/unoccupied
            frame = vs.read()
            frame = frame[1]

            text = "Unproductive"

            # if the frame could not be grabbed, then we have reached the end
            # of the video
            if frame is None:
                break

            # resize the frame, convert it to grayscale, and blur it
            frame = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
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
            cv2.namedWindow("Motion Detection")
            cv2.moveWindow("Motion Detection", 0, 0)
            cv2.imshow("Motion Detection", frame)

            cv2.namedWindow("Thresh")
            cv2.moveWindow("Thresh", 500, 500)
            cv2.imshow("Thresh", thresh)

            cv2.namedWindow("Frame Delta")
            cv2.moveWindow("Frame Delta", 0, 500)
            cv2.imshow("Frame Delta", frameDelta)

            if i % 2 != 0:
                firstFrame = gray
            i = i + 1

            key = cv2.waitKey(1) & 0xFF

            # if the `q` key is pressed, break from the lop
            if key == ord("q"):
                break

        # cleanup the camera and close any open windows
        vs.release()
        cv2.destroyAllWindows()
