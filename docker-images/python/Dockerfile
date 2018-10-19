FROM nuveo/opencv:debian-python3-opencv2
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./lib/* /opt/lib/
COPY ./script.py /opt/script.py
ENTRYPOINT [ "python3",  "/opt/script.py" ] 
