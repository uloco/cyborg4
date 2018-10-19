from lib import MqttLibrary
import time

mqttClient = MqttLibrary.createClient("172.17.0.2", 1883)

state = 1

while 1:
    print("Publish state ", state)
    MqttLibrary.publishState(mqttClient, state)
    if state < 5:
        state += 1
    else:
        state = 1
    time.sleep(3)
