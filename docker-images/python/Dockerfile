FROM nuveo/opencv:debian-python3-opencv2
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./analysis/MotionDetectorContour.py /opt/script.py
ENTRYPOINT [ "python3",  "/opt/script.py" ] 
