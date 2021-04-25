import time
from datetime import datetime
from max30100_pulse import *
import paho.mqtt.client as mqtt
import json

'''Filters'''
'''DC Removal IR'''
ALPHA = 0.95
dc_w = 0

'''DC Removal Red'''
ALPHA_RED = 0.95
dc_w_red = 0
filtered_red = 0

'''Mean Diff'''
MEAN_SIZE_FILTER = 15
md_sum = 0
md_values = [0] * MEAN_SIZE_FILTER
md_index = 0
md_count = 0

'''Butterworth Filter'''
bw_array = [0] * 2


'''Filtering Values'''
ir_value = 0
ir_filtered = 0

'''Detect Pulse'''
have_beat = False

''' Get BPM '''
bpm = 0
bpm_queue = []
start_time = time.time()

''' For Thingsboard '''
iot_hub ="129.126.163.157" 
port = 1883
username ="aG6V21JtciMXWLlOoqe5" #Access Token
password=""
topic ="v1/devices/me/telemetry"

client = mqtt.Client()
client.username_pw_set(username) #Use the access token to push data to telemetry
client.connect(iot_hub, port) #Connect to Thingsboard
print("Connection success")

data = dict()

#To remove DC signal and leave only AC
def dcRemoval(ir):
    global dc_w
    prev_w = dc_w
    dc_w = ir + ALPHA * prev_w
    result = dc_w - prev_w
    return result

def dcRemoval_red(red):
    global dc_w_red
    global filtered_red
    prev_w_red = dc_w_red
    dc_w_red = red + ALPHA_RED * prev_w_red
    result = dc_w_red - prev_w_red
    filtered_red = result    

#To calculate value changes from average
def meanDiff(dcRemoved):
    global md_values
    global md_index
    global md_count
    global md_sum
    
    avg = 0
    
    md_sum -= md_values[md_index]
    md_values[md_index] = dcRemoved
    md_sum += md_values[md_index]
    md_index+=1
    md_index = md_index % MEAN_SIZE_FILTER
    if(md_count < MEAN_SIZE_FILTER):
        md_count += 1
        
    avg =  md_sum / md_count
    return avg - dcRemoved

#To removal high level harmonies
def butterWorth(meanDiffed):
    global bw_array
    bw_array[0] = bw_array[1]
    bw_array[1] = (2.452372752527856026e-1 * meanDiffed) + (0.50952544949442879485 * bw_array[0]);
    return bw_array[0] + bw_array[1]

#Filter the raw values till butterworth
def filterValues(ir):
    global ir_prev_value
    global ir_value
    ir_prev_value = ir_value
    dcResult = dcRemoval(ir)
    mdAvg = meanDiff(dcResult)
    ir_value = butterWorth(mdAvg)
    return ir_value

#From the filtered value, check whether pulse is detected
def detectPulse(ir_value, red_value):
    global have_beat
    if ir_value > 45 and not have_beat:
        if ir_value < ir_prev_value:
            have_beat = True
            return True
    elif red_value < 20 and have_beat:
        have_beat = False
        
    return False
   
#Calculate the time interval and get the BPM   
def getBPM(ir_value, red_value):
    global bpm
    global bpm_queue
    global start_time
    if ir_value > 200:
        return None
    elif detectPulse(ir_value, red_value):
        time_now = time.time()
        bpm_value = 60/(float)(time_now - start_time)
        if bpm_value < 220:
            bpm = bpm_value
        else:
            return None
        if len(bpm_queue) > 10:
            bpm_queue = bpm_queue[1:]
        start_time = time.time()
        bpm_queue.append(bpm)
    return bpm

#Calculate average BPM
def getAvgBPM():
    if len(bpm_queue) != 0:
        return sum(bpm_queue)/len(bpm_queue)
    return None

def main():
    global client
    mx30=MAX30100() #Initialize MAX30100

    i = 0
    while True:
        mx30.set_mode_hr() #Change mode to HR
        mx30.update_values() #Update sensor values
        result = filterValues(mx30.current_ir)

        mx30.set_mode_spo2() #Change mode to SPO2
        mx30.update_values() #Update sensor values
        red_result = dcRemoval(mx30.current_red)
        
        bpm = getBPM(result, red_result)
        avg_bpm = getAvgBPM()
        
        if i % 100 == 0: #Pass data to Thingsboard every 0.1sec
            data["Pulse"] = str(avg_bpm)
            print(data)
            data_out=json.dumps(data)
            client.publish(topic, data_out, 0) #Push dictionary to Thingsboard
            
        i += 1
        time.sleep(0.01)
         
if __name__ == "__main__" :
    main()
