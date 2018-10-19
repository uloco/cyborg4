import paho.mqtt.client as mqtt    
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("machine/data/state")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def createClient(server, port):
    if not server or port <= 0:
        print("No server or port given couldn't create client")
        return
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(server, port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_start()
    return client

def publishState(client, state):
    client.publish("machine/data/state", state)

def subscribeState(client):
    client.subscribe("machine/data/state")
