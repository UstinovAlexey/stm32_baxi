import nic
import time 
from umqtt import MQTTClient
MQTT_BROKER = "192.168.20.55"
CLIENT_ID = "stm32_baxi"
SUBSCRIBE_TOPIC = b"baxi/GitOTA"
PUBLISH_TOPIC = b"baxi/GitOTA"
gitver="V1"

def sub_cb(topic, msg):
    print((topic, msg))
    if (topic==b"baxi/GitOTA") and (msg==b"PullGit"):
        print ("!!!")

mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883,user="user",password="89127634678",keepalive=60)
mqttClient.set_callback(sub_cb)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)

for i in range (10):
    time.sleep(1)
    # Non-blocking wait for message
    mqttClient.check_msg()
    

    mqttClient.publish(PUBLISH_TOPIC, "Waiting OTA Cmd {}".format(i))

    
mqttClient.publish(PUBLISH_TOPIC, "Run application. GitVer={}".format(gitver))
 