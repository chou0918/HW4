import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as paho
import serial
import time

mqttc = paho.Client()

# Settings for connection
host = "localhost"
topic= "Mbed"
port = 1883

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

sample = 80

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe    

t = np.arange(0,sample/2,1)
x = np.arange(0,sample/2,1)
y = np.arange(0,sample/2,1)
z = np.arange(0,sample/2,1)
tilt = np.arange(0,sample/2,1)


s.write("+++".encode())

char = s.read(2)

print("Enter AT mode.")

print(char.decode())


s.write("ATMY 0x123\r\n".encode())

char = s.read(3)

print("Set MY 0x123.")

print(char.decode())


s.write("ATDL 0x223\r\n".encode())

char = s.read(3)

print("Set DL 0x223.")

print(char.decode())


s.write("ATID 0x1\r\n".encode())

char = s.read(3)

print("Set PAN ID 0x1.")

print(char.decode())


s.write("ATWR\r\n".encode())

char = s.read(3)

print("Write config.")

print(char.decode())


s.write("ATMY\r\n".encode())

char = s.read(4)

print("MY :")

print(char.decode())


s.write("ATDL\r\n".encode())

char = s.read(4)

print("DL : ")

print(char.decode())


s.write("ATCN\r\n".encode())

char = s.read(3)

print("Exit AT mode.")



# XBee setting

serdev = '/dev/ttyUSB0'

s = serial.Serial(serdev, baudrate = 9600)

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

for i in range(0, 50):
    # send RPC to remote

    s.write("/getAcc/run\r".encode())
    time.sleep(1)

    if i < 3 :
        s.write("/getAcc/run 0\r".encode())

    else :
        line=s.readline()
        mqttc.publish(topic, line)
        line=s.readline() 
        x[i-5] = float(line)
        line=s.readline()  
        y[i-5] = float(line)
        line=s.readline() 
        z[i-5] = float(line)
        line=s.readline() 
        tilt[i-5] = float(line)
        

fig, ax = plt.subplots(2, 1)
ax[0].stem(t,tilt)

ax[1].plot(t,x,y,z)


plt.show()
s.close()