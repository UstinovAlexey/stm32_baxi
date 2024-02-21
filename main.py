# main.py -- put your code here!
import nic
import time
import ugit
from board import CLIENT_ID as CLIENT_ID
from board import MQTT_PREFIX as MQTT_PREFIX


from umqtt import MQTTClient
MQTT_BROKER = "192.168.20.55"
#CLIENT_ID = "stm32_baxi"
SUBSCRIBE_TOPIC = MQTT_PREFIX+"GitOTA"
PUBLISH_TOPIC = MQTT_PREFIX+"GitOTA"
gitver="V2.5"
needGitOTAupdate=False

def sub_cb(topic, msg):
    global needGitOTAupdate
    print((topic, msg))
    if (topic==MQTT_PREFIX+"GitOTA") and (msg==b"PullGit"):
        needGitOTAupdate=True


mqttClient = MQTTClient(CLIENT_ID, MQTT_BROKER, port=1883,user="user",password="89127634678",keepalive=60)
mqttClient.set_callback(sub_cb)
mqttClient.connect()
mqttClient.subscribe(SUBSCRIBE_TOPIC)

for i in range (10):
    time.sleep(1)
    # Non-blocking wait for message
    mqttClient.check_msg()
            
    if needGitOTAupdate==True:
        mqttClient.publish(PUBLISH_TOPIC, "OTA: Now Git pulled...")

    else:
        mqttClient.publish(PUBLISH_TOPIC, "Waiting OTA Cmd {}".format(i))

if needGitOTAupdate==True:
        ugit.pull_all()
    
mqttClient.publish(PUBLISH_TOPIC, "Run application. GitVer={}".format(gitver))

#run application
import runtime