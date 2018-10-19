#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
from MotionDetectorContour import MotionDetectorContour

folder_path = '/Users/jungbluth/Desktop/hackathon/'

onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

for name in onlyfiles:
    file_path = folder_path + name
    print(file_path)
    t = MotionDetectorContour(file_path)
    t.run()