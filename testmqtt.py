import nic
from umqtt import MQTTClient
import time
import random

# Default  MQTT_BROKER to connect to
MQTT_BROKER = "192.168.20.55"
CLIENT_ID = "stm32_baxi"
SUBSCRIBE_TOPIC = b"baxi/temp"
PUBLISH_TOPIC = b"baxi/temp"

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))
    if (topic==b"baxi/status") and (msg==b"PullGit"):
        print ("!!!")

def reset():
    print("Resetting...")
    time.sleep(5)
    machine.reset()

def get_temperature_reading():
    return random.randint(20, 50)


mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883,user="user",password="89127634678",keepalive=60)
mqttClient.set_callback(sub_cb)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)
mqttClient.subscribe("baxi/status")

mqttClient.publish("baxi/status", "Idle")

while True:
    time.sleep(2)
    # Non-blocking wait for message
    mqttClient.check_msg()
    
    random_temp = get_temperature_reading()
    mqttClient.publish(PUBLISH_TOPIC, str(random_temp).encode())
    mqttClient.publish("baxi/output", "Hello, World {}".format(2*3))
    
    print(1)