import smbus                      # import SMBus module of I2C
import time                       # import time modules
import pyMPU6050                  # import C funtions for measuring MPU6050
import numpy as np                # import data array functions
import tensorflow as tf           # import machine learning functions
import paho.mqtt.client as mqtt   # import communication protocols
import json                       # import json library
import socket                     # for socket communication
import RPi.GPIO as GPIO           # for GPIO-based interrupt

# addresses for MPU6050 registers
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACC_X_ADDR   = 0x3B
ACC_Y_ADDR   = 0x3D
ACC_Z_ADDR   = 0x3F
GYRO_X_ADDR  = 0x43
GYRO_Y_ADDR  = 0x45
GYRO_Z_ADDR  = 0x47

# Method for initalizing MPU6050
def MPU_Init():
    # write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    # write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    # write to configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    # write to gyroscope configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    # write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

# Interrupt method
def ISR_Function(channel):
    global sentFalse
    
    print ("Falling!!")
    sentFalse = False
    GPIO.output(OUTPUT_PIN, GPIO.HIGH)
    
# Interrupt configuration
OUTPUT_PIN = 11           # GPIO Pin for sending interrupt signals
LISTEN_PIN = 12           # GPIO Pin for listening interrupt signals
GPIO.setwarnings(False)   # Turn off warnings for GPIO libraries
GPIO.setmode(GPIO.BOARD)  # Set GPIO to board mode
GPIO.setup(OUTPUT_PIN, GPIO.OUT) # Set OUTPUT_PIN to output mode
GPIO.setup(LISTEN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Set LISTEN_PIN to input mode
# Use LISTEN_PIN to listen for interupt on falling edge, and call ISR_Function when interrupted
GPIO.add_event_detect(LISTEN_PIN, GPIO.FALLING, callback = ISR_Function)
# Set output to high before starting program
GPIO.output(OUTPUT_PIN, GPIO.HIGH)

# TensorFlow Model Directory
TFModel = "testmodel-new-C-24x24.h5"

# Boolean to prevent false sent being spammed
sentFalse = False

# UDP configuration for buzzer RPi
UDP_IP = "192.168.43.252" # IP address for buzzer RPi
UDP_PORT = 5000           # port number for UDP

# Initialize and connect to ThingsBoard
iot_hub ="129.126.163.157"       # ThingsBoard IP address
port = 1883                      # ThingsBoard port
username ="xlvUXeTldA5fhOFxGfOJ" # ThingsBoard access token
topic ="v1/devices/me/telemetry" # address for data to be published to
client=mqtt.Client()             # intialize communication protocol
client.username_pw_set(username) # intialize token
client.connect(iot_hub,port)     # initialize address
print("Connection success")      # confirmation message
data=dict()                      # store data in dictionary

# -- Main Program -- #
bus = smbus.SMBus(1)                        # map smbus for initialization
Device_Address = 0x68                       # MPU6050 device address
MPU_Init()                                  # call MPU6050 initializer
fd = pyMPU6050.py_getFd(Device_Address)     # set-up device address for C functions
model = tf.keras.models.load_model(TFModel) # initialize machine learning model
print ("Tracking user movement") # indicate prediction start

while True:
    # get calculated accelerometer values
    acc_x = pyMPU6050.py_readAcc(fd, ACC_X_ADDR)
    acc_y = pyMPU6050.py_readAcc(fd, ACC_Y_ADDR)
    acc_z = pyMPU6050.py_readAcc(fd, ACC_Z_ADDR)
    
    # get calculated gyroscope values
    gyro_x = pyMPU6050.py_readGyro(fd, GYRO_X_ADDR)
    gyro_y = pyMPU6050.py_readGyro(fd, GYRO_Y_ADDR)
    gyro_z = pyMPU6050.py_readGyro(fd, GYRO_Z_ADDR)

    # print out values for testing
    # print ("Gx=%.2f" %gyro_x, u'\u00b0'+ "/s", "\tGy=%.2f" %gyro_y, u'\u00b0'+ "/s", "\tGz=%.2f" %gyro_z, u'\u00b0'+ "/s", "\tAx=%.2f g" %acc_x, "\tAy=%.2f g" %acc_y, "\tAz=%.2f g" %acc_z)
    
    # Load values into numpy array, and use tensorflow-keras to predict
    np_data = np.array([[[gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z]]])
    result = model.predict(np_data)[0,0,0]
    
    # trigger condition for falling signal
    # print ("result = ", result)

    if (result > 0.8): # prediction value
        # publish to ThingsBoard
        data["isFalling"] = "True" # flag fall as true
        # print(data)
        data_out=json.dumps(data) # convert object data to string
        client.publish(topic, data_out, 0) # push data to ThingsBoard

        # send signal to buzzer
        MESSAGE = "FALL" # send message to server to make beep sound
        send = MESSAGE.encode('ascii') # encode message to server
        sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # ipv4 address
        sock.sendto(send,(UDP_IP,UDP_PORT)) #send message to buzzer RPi
    
        GPIO.output (OUTPUT_PIN, GPIO.LOW) #print ("FALLING")

        time.sleep(1) # pause to prevent fall signal overlap
    else:
        if sentFalse == False:
            # publish to ThingsBoard
            data["isFalling"] = "False" # flag fall as false
            print (data)
            data_out=json.dumps(data) # convert object data to string
            client.publish(topic, data_out, 0) # publish data to ThingsBoard
            sentFalse = True