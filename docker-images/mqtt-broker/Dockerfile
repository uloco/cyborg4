FROM eclipse-mosquitto
COPY users.txt /etc/mosquitto/users.txt
RUN mosquitto_passwd -U /etc/mosquitto/users.txt
COPY mosquitto.conf /mosquitto/config/mosquitto.conf