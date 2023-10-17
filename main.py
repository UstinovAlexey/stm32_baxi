# main.py -- put your code here!
import nic
import time
import ugit

from umqtt import MQTTClient
MQTT_BROKER = "192.168.20.55"
CLIENT_ID = "stm32_baxi"
SUBSCRIBE_TOPIC = b"baxi/GitOTA"
PUBLISH_TOPIC = b"baxi/GitOTA"
gitver="V1"
needGitOTAupdate=False

def sub_cb(topic, msg):
    global needGitOTAupdate
    print((topic, msg))
    if (topic==b"baxi/GitOTA") and (msg==b"PullGit"):
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
        print("ww")

    else:
        mqttClient.publish(PUBLISH_TOPIC, "Waiting OTA Cmd {}".format(i))
        print("w")

if needGitOTAupdate==True:
        ugit.pull_all()
    
mqttClient.publish(PUBLISH_TOPIC, "Run application. GitVer={}".format(gitver))

#run application
import runtime