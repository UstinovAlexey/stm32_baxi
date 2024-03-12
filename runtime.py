import pyb
import machine
import micropython

micropython.alloc_emergency_exception_buf(100)

import nic
from umqtt import MQTTClient
import time
import random
from board import CLIENT_ID as CLIENT_ID
from board import MQTT_PREFIX as MQTT_PREFIX


# Default  MQTT_BROKER to connect to
MQTT_BROKER = "192.168.20.55"

SUBSCRIBE_TOPIC = MQTT_PREFIX+"Tset"
PUBLISH_TOPIC = MQTT_PREFIX+"temp"

Tset_cur=30
Tset_new=30
Tset_need_set=False
Status_new=3
ExtCMD_need_send=False
ExtCMD_req=""



# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    global Tset_new,Tset_need_set,Status_new,Status_need_set,ExtCMD_need_send,ExtCMD_req
    print((topic, msg))
    if (topic==MQTT_PREFIX+"status"):#and (msg==b"PullGit"):
        try:
            Status_new=int(msg)
        except:
            Status_new=3
            
        if Status_new>=0 and Status_new<=3:
            pass
        else:
           Status_new=3

    if (topic==MQTT_PREFIX+"GitOTA") and (msg==b"PullGit"):   
        import machine
        machine.reset()
        
    if (topic==MQTT_PREFIX+"ExtCMD_req"):
        ExtCMD_need_send=True
        ExtCMD_req=msg

        
    if (topic==MQTT_PREFIX+"Tset"):
        Tset_new=float(msg)
        Tset_need_set=True
        #if (Tset_new!=Tset_cur):
        #    Tset_need_set=True
            


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
mqttClient.subscribe(MQTT_PREFIX+"status")
mqttClient.subscribe(MQTT_PREFIX+"GitOTA")
mqttClient.subscribe(MQTT_PREFIX+"ExtCMD_req")

mqttClient.publish(MQTT_PREFIX+"status", "Idle!!5")
mqttClient.publish(MQTT_PREFIX+"ExtCMD_req", "[0,1,0]")


print("Start3_2")

btn=pyb.Pin("C13")



class OpenTherm:
  cikles=0
  data=[]
  pin=0
  tim=0
    
  def __init__(self,pin="B0",timer_id=1): #B0-led

        OpenTherm.pin=pyb.Pin(pin,mode=pyb.Pin.OUT)
        OpenTherm.tim=pyb.Timer(timer_id,freq=2000) #timer_id,freq=2000,callback=self.mycallback())
  

  def mycallback (t):
      global pin_in_mode

      if OpenTherm.cikles>0:
          OpenTherm.cikles=OpenTherm.cikles-1 

              
          if OpenTherm.data[OpenTherm.cikles]:
          
           #OpenTherm.pin.on()
            OpenTherm.pin.off()
          else:
            #OpenTherm.pin.off()
            OpenTherm.pin.on()
         
          #OpenTherm.cikles=OpenTherm.cikles-1 
            
         
                 
      else:
          OpenTherm.tim.deinit()
          #OpenTherm.pin.off() # 
          OpenTherm.pin.on() #
          


        
  def send(self,data):
      
      OpenTherm.data=[0,1] #start bit
      #buf=0
      #data=0
      for i in range (32):
        if data & (1<<i):
          #print(1)
          OpenTherm.data.append(0)
          OpenTherm.data.append(1)
        else:
          #print(0)
          OpenTherm.data.append(1)
          OpenTherm.data.append(0)
          
      OpenTherm.data.append(0)
      OpenTherm.data.append(1)

      OpenTherm.cikles=len(OpenTherm.data)

      OpenTherm.tim.freq(2000)
      OpenTherm.tim.callback(OpenTherm.mycallback)

import time

ot=OpenTherm(pin="E11")
pin_in=pyb.Pin("E13")

#dt_start=time.ticks_us()
answer_l=0x00
answer_h=0x00
pin_in_mode=0 #0-disbale IN
bit_counter=0
dt_start=0 #len of start bit
prev_us=0

def pinRise(line):
    
    global dt_start,answer_l,answer_h,pin_in_mode,bit_counter,prev_us
    
    pin_value=pin_in.value()
    
    cur_us=time.ticks_us()
    
    dt=cur_us-prev_us
    prev_us=cur_us
    
    if pin_in_mode==0:
        return
    
    #if pin_value==1:
    #    print("s",end="")
    #else:
    #    print("r",end="")
    #print(pin_in_mode,end="")

        
    if pin_in_mode>1:
        #2- just start front received 3-medium_fall 4- medium rise 5- start fall 6-start rise 
        if (pin_value==1) & ((pin_in_mode%2)==0):

            print("Err: pin is 1 but waiting 0.",pin_in_mode,bit_counter)
            pin_in_mode=0
            return
        if (pin_value==0) & ((pin_in_mode%2)==1):
            
            print("Err: pin is 0 but waiting 1.",pin_in_mode,bit_counter)
            pin_in_mode=0
            return
        if dt>2000:
            pin_in_mode=0
            print("Err:dt timeout. Value is= ",dt)
            return
        
    if  pin_in_mode==1:
        pin_in_mode=2 # received START bit

    elif  (pin_in_mode==2):
        dt_start=dt
        answer_l=0
        answer_h=0
        bit_counter=0
        pin_in_mode=3 #3-medium_fall 4- medium rise 5- start fall 6-start
        
    elif pin_in_mode==3:
        if dt<700:
            pin_in_mode=6
        else:
            pin_in_mode=4
   
    elif pin_in_mode==4:
        if dt<700:
            pin_in_mode=5
        else:
            pin_in_mode=3
            
    elif pin_in_mode==5:
        if dt<700:
            pin_in_mode=4
        else:
            pin_in_mode=6
    
    elif pin_in_mode==6:
        if dt<700:
            pin_in_mode=3
        else:
            pin_in_mode=5

    if pin_in_mode==3:
        
        bit_counter+=1
        
        if (bit_counter>1) &(bit_counter<=17):
          answer_h=answer_h*2+1
          #print("1",end="")
        elif (bit_counter>17) &(bit_counter<34):
          answer_l=answer_l*2+1
          #print("1",end="")
        
    if pin_in_mode==4:
        bit_counter+=1
        
        if (bit_counter>1) &(bit_counter<=17):
          answer_h*=2
          #print("0",end="")
        elif (bit_counter>17) &(bit_counter<34):
          answer_l*=2
          #print("0",end="")    
extRise=pyb.ExtInt("E13",pyb.ExtInt.IRQ_RISING_FALLING,pyb.Pin.PULL_UP,pinRise)
#extFall=pyb.ExtInt("E13",pyb.ExtInt.IRQ_FALLING,pyb.Pin.PULL_UP,pinFall)

def buildRerquest(msg_type,data_id,data_value):
    
    request=(msg_type<<28)|(data_id<<16)
    
    if type(data_value)==int:
        request|=data_value
    if type(data_value)==float:
        request|=int(data_value*256)

    #calculate parity
    P=0
    for bit in range(32):
        if (request & (1<<bit)):
            P=0 if P else 1


    return (request|(P<<31))



#    0X90014000   01 001 40000
Status="0x??"

while (True):
    #while(btn()==1):
    #    pass
    #while(btn()==0):
    #    pass
    #print("cikles=",ot.cikles)
    #ot.send(0x90014000)
    
    if ExtCMD_need_send==True:
        ExtCMD_need_send=False
        import json
        try:
            ExtCMD=json.loads(ExtCMD_req)
                        
            pin_in_mode=0 #disable read answer
            ot.send(buildRerquest(ExtCMD[0],ExtCMD[1],ExtCMD[2]))
            time.sleep(0.06)
            pin_in_mode=1 #enable read answer
            time.sleep(0.5)

            answer=[hex((answer_h//4096)&7),answer_h % 256,answer_l,hex(answer_l),answer_l/256.0]
            mqttClient.publish(MQTT_PREFIX+"ExtCMD_ans", json.dumps(answer))      
            #print("ExtCMD is: ",type(json.loads(ExtCMD_req)))
        except:

            print("error json import ExtCMD_req=",ExtCMD_req)
       

    if Tset_need_set==True:
        Tset_need_set=False
        Tset_cur=Tset_new
        
        print("Set setpoint={}".format(Tset_new),end="")
        
        pin_in_mode=0 #disable read answer
        ot.send(buildRerquest(1,1,Tset_new))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(0.5)
        print("answer=",hex(answer_h*65536+answer_l),end=" ")
        print(" ")
    
    if 0:
        print("Reset Lock-Out")
        pin_in_mode=0 #disable read answer
        ot.send(buildRerquest(1,4,256))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer=",hex(answer_h*65536+answer_l))
        print(" ")

    if 0:
        print("CH water filling")
        pin_in_mode=0 #disable read answer
        ot.send(buildRerquest(1,4,512))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer=",hex(answer_h*65536+answer_l))
        print(" ")
        
    print(" ")    
    print("Read vars.",end=" ")
    pin_in_mode=0
    ot.send(buildRerquest(0,25,0))
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    Tboiler=answer_l/256.0
    #print(" answer",hex(answer_h*65536+answer_l),end=" ")
    #print(" Measured Tboiler temp=",answer_l/256.0)
    #print(" ")

    #print("Read  Ret Temperature.",end="")
    pin_in_mode=0
    ot.send(buildRerquest(0,28,0))
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    Tret=answer_l/256.0
    #print(" answer",hex(answer_h*65536+answer_l),end=" ")
    #print(" Measured Tret temp=",answer_l/256.0)
    #print(" ")
    
    #print("Read  DHW Temperature.",end="")
    pin_in_mode=0
    ot.send(buildRerquest(0,26,0))
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    Tdhw=answer_l/256.0
    #print(" answer",hex(answer_h*65536+answer_l),end=" ")
    #print(" Measured Tdhw temp=",answer_l/256.0)

    #print("Read  DHW Flow.",end="")
    pin_in_mode=0
    ot.send(buildRerquest(0,19,0))
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    #print(" answer",hex(answer_h*65536+answer_l),end=" ")
    #print(" Measured DHW flow=",answer_l/256.0)
    DHWFlow=answer_l/256.0
    #print(" ")

    print("Tboiler={} Tret={} Tdhw={} DHW Flow={}".format(Tboiler,Tret,Tdhw,DHWFlow))
    mqttClient.publish(MQTT_PREFIX+"Tboiler", str(Tboiler))
    mqttClient.publish(MQTT_PREFIX+"Tret", str(Tret))
    mqttClient.publish(MQTT_PREFIX+"Tdhw", str(Tdhw))
    mqttClient.publish(MQTT_PREFIX+"DHWFlow", str(DHWFlow))
    
#    print("Read Modulation level.",end="")
    pin_in_mode=0
    ot.send(buildRerquest(0,17,0))
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    #print("answer",hex(answer_h*65536+answer_l),end=" ")
    ModLevel=answer_l/256.0
    #print(" Modulation level=",answer_l/256.0)
    #print(" ")
    
    #print("Read  CH preasure.",end="")
    pin_in_mode=0
    ot.send(buildRerquest(0,5,0)) #ASF-flags/OEM-fault-codes
    time.sleep(0.06)
    pin_in_mode=1 #enable read answer
    time.sleep(0.5)
    ASF_OEM=hex(answer_l)
    #print(" answer",hex(answer_h*65536+answer_l),end=" ")
    #print(" Measured CH preasure=",answer_l/256.0)
    #print(" ")


    if 0:
       print("Read Status. ",end="")
       pin_in_mode=0
       ot.send(buildRerquest(0,0,Status_new*256)) #enable CH & DHW
       #ot.send(buildRerquest(0,0,0x000)) #-disable boiler

       time.sleep(0.06)
       pin_in_mode=1 #enable read answer
       time.sleep(0.5)
       #print("Answer",hex(answer_h*65536+answer_l))
       Status=hex(answer_l)
       #print("Status Measured temp=",answer_l/256.0)
    print("Status={} ASF_OEM={} ModulationLevel={} ".format(Status,ASF_OEM,ModLevel))
    mqttClient.publish(MQTT_PREFIX+"Status",Status)
    mqttClient.publish(MQTT_PREFIX+"ASF_OEM",ASF_OEM)
    mqttClient.publish(MQTT_PREFIX+"ModLevel",str(ModLevel))

    # Non-blocking wait for message
    mqttClient.check_msg()
    
    random_temp = get_temperature_reading()
    mqttClient.publish(PUBLISH_TOPIC, str(random_temp).encode())
    mqttClient.publish(MQTT_PREFIX+"output", "Hello, World {}".format(2*3))


    if 0:
        print("Read  5 Status")
        pin_in_mode=0
        ot.send(buildRerquest(0,5,0))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer",hex(answer_h*65536+answer_l))
        #print("Status Measured temp=",answer_l/256.0)
        print(" ")
        
        print("Read 115 Status")
        pin_in_mode=0
        ot.send(buildRerquest(0,115,0))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer",hex(answer_h*65536+answer_l))
        #print("Status Measured temp=",answer_l/256.0)
        print(" ")
    
    if 0:
        print("Read Water Preasure")
        pin_in_mode=0
        ot.send(buildRerquest(0,18,0))
        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer",hex(answer_h*65536+answer_l))
        print("Water Preasure=",answer_l/256.0)
        print(" ")

    if 0:
        print("Read Slave Version")
        pin_in_mode=0
        ot.send(buildRerquest(0,127,0))

        time.sleep(0.06)
        pin_in_mode=1 #enable read answer
        time.sleep(1)
        print("answer",hex(answer_h*65536+answer_l))
        print("Version=",hex(answer_l))
        print(" ")

#0x10013C00-reg1
    #0x400C8000 -req 2
    #print("cikles=",ot.cikles)

import time
time.sleep(1)
print("{} End2".format(bin(255-64)))

import asyncio

class aioOpenTherm:
  def __init__(self,pin="B0",timer_id=1):
        self.cikles=0
        self.pin=pyb.Pin(pin)
        self.tim=pyb.Timer(timer_id,freq=2000) #timer_id,freq=2000,callback=self.mycallback())
        
  async def send(self,data):
    print("Send")

    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    time.sleep_us(500)
    self.pin.on()
    time.sleep_us(500)
    self.pin.off()
    
aioOT=aioOpenTherm()

async def main ():
    while True:
        await aioOT.send(12)
        print(1)
        await asyncio.sleep(1)
        print(2)
        await asyncio.sleep(1)

#asyncio.run(main())

      





