import Adafruit_DHT
import paho.mqtt.client as mqtt
import json
import smbus
import time
import datetime
import pandas as pd
from sklearn import linear_model
import random
import take_picture
import ctypes

#setup the thingsboard
address = "129.126.163.157"
port = 1883
username = "Sjv7opkPaZ1fJ7ASQ2XG"
password = ""
topic = "v1/devices/me/telemetry"

client=mqtt.Client() #open a new connection
client.username_pw_set(username,password) #set username and password
client.connect(address,port) #connect to thingsboard with port
print("Connection Success")

#create empty dictionaries to be publish into thingsboard
data = dict()
data2 = dict()
data3 = dict()
data4 = dict()
data5 = dict()
data6 = dict()
data7 = dict()

#setup the temperature & humidity sensor
DHT_SENSOR = Adafruit_DHT.AM2302
DHT_PIN = 4

#setup the pioneer600's ADC
bus = smbus.SMBus(1)
address = 0x48
A0 = 0x40
A1 = 0x41
A2 = 0x42
A3 = 0x43

#function get LDR data from KY-018
def get_LDR(array):
    bus.write_byte(address,A1) #write to address to the adc register (I2C Protocol)
    ldr = bus.read_byte(address) #read the data sent back from the register
    if ldr > 0:
        data["LDR"] = ldr #put the ldr data into dictionary
        output = json.dumps(data) #dump the dictionary into json
        client.publish(topic,output) #push the json data into thingsboard
        array.append(ldr) #append to the array to be returned to the pioneer600
        return array
    else:
        ldr = "Error"
        data["LDR"] = ldr #put the ldr data into dictionary
        output = json.dumps(data) #dump the dictionary into json
        client.publish(topic,output) #push the json data into thingsboard
        array.append(ldr) #append to the array to be returned to the pioneer600
        return array

#function to get moisture sensor data
def get_Moisture(array):
    #bus.write_byte(address,A0) #write to address to the adc register (I2C Protocol)
    #moisture = bus.read_byte(address) #read the data sent back from the register
    #if moisture is not None:
        #data2["Moisture"] = moisture #put the moisture data into dictionary
        #output2 = json.dumps(data2) #dump the dictionary into json
        #client.publish(topic,output2) #push the json data into thingsboard
        #array.append(moisture) #append to the array to be returned to the pioneer600
        #return array
    #else:
        #moisture = "Error"
        #data2["Moisture"] = moisture #put the moisture data into dictionary
        #output2 = json.dumps(data2) #dump the dictionary into json
        #client.publish(topic,output2) #push the json data into thingsboard
        #array.append(moisture) #append to the array to be returned to the pioneer600
        #return array
    moisture = random.uniform(58,59) #random due to clash of ADC address
    data2["Moisture"] = moisture #put the moisture data into dictionary
    output2 = json.dumps(data2) #dump the dictionary into json
    client.publish(topic,output2) #push the json data into thingsboard
    array.append(moisture) #append to the array to be returned to the pioneer600
    return array

#function to get temperature & humidity sensor data
def get_TempHum(array):
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN) #read data from DHT_22 through AdaFruit Library
    if not [data for data in (temperature, humidity) if data is None]:
        data3["Temperature"] = temperature #put the temperature data into dictionary
        output3 = json.dumps(data3) #dump the dictionary into json
        client.publish(topic,output3) #push the json data into thingsboard
        array.append(temperature) #append to the array to be returned to the pioneer600
        data4["Humidity"] = humidity #put the humidity data into dictionary
        output4 = json.dumps(data4) #dump the dictionary into json
        client.publish(topic,output4) #push the json data into thingsboard
        array.append(humidity) #append to the array to be returned to the pioneer600
        return array
    else:
        temperature = "Error"
        humidity = "Error"
        data3["Temperature"] = temperature #put the temperature data into dictionary
        output3 = json.dumps(data3) #dump the dictionary into json
        client.publish(topic,output3) #push the json data into thingsboard
        array.append(temperature) #append to the array to be returned to the pioneer600
        data4["Humidity"] = humidity #put the humidity data into dictionary
        output4 = json.dumps(data4) #dump the dictionary into json
        client.publish(topic,output4) #push the json data into thingsboard
        array.append(humidity) #append to the array to be returned to the pioneer600
        return array

#MLR #1 to plot and predict the number of hours before germination
def get_Germination(ldr, moisture, temperature, humidity, array):
    #read the training data
    mlrdata = pd.read_csv("plant_data.csv")
    
    #fits the data into the x and y axis
    X1 = mlrdata[['Temperature', 'Humidity', 'Moisture', 'Light']]
    y1 = mlrdata['Hours to Germinate']

    #input the data into the model and form multiple linear regression
    mlr = linear_model.LinearRegression()
    mlr.fit(X1, y1)
    
    if not [data for data in (temperature, humidity, moisture, ldr) if data is None or data == "Error"]:
        predictedGermination = mlr.predict([[temperature, humidity, moisture, ldr]]) #insert the sensor data into the graph and get the predicted hours to germination
        predictedGermination = round(predictedGermination[0],2) #round off the hours to 2 decimal place
        data5["Germination"] = predictedGermination #put the germination hours data into dictionary
        output5 = json.dumps(data5) #dump the dictionary into json
        client.publish(topic,output5) #push the json data into thingsboard
        array.append(predictedGermination) #append to the array to be returned to the pioneer600
        return array
    else:
        predictedGermination = "Error"
        data5["Germination"] = predictedGermination #put the germination hours data into dictionary
        output5 = json.dumps(data5) #dump the dictionary into json
        client.publish(topic,output5) #push the json data into thingsboard
        array.append(predictedGermination) #append to the array to be returned to the pioneer600
        return array

#MLR #2 to plot and predict the number of hours the moisture can last before reaching threshold
def get_EPH(moisture, temperature, humidity, array):
    #read the training data
    mlrdata2 = pd.read_csv("plant_data_evaporation.csv")
    
    #fits the data into the x and y axis
    X2 = mlrdata2[['Temperature', 'Humidity']]
    y2 = mlrdata2['EPH']

    #input the data into the model and form multiple linear regression
    mlr2 = linear_model.LinearRegression()
    mlr2.fit(X2, y2)

    if not [data for data in (temperature, humidity) if data is None or data == "Error"]:
        EPH = mlr2.predict([[temperature, humidity]]) #insert the sensor data into the graph and get the predicted evaporation per hour
        threshhold = 53 #indicate the treshold
        formular = (((moisture-threshhold)/EPH[0])*-1) #perform the formular to calculate the number of hours the moisture level can last before reaching the threshold
        
        #if the moisture level > threshold
        if formular > 0:
            data6["EPH"] = formular #put the MLR data into dictionary
            output6 = json.dumps(data6) #dump the dictionary into json
            client.publish(topic,output6) #push the json data into thingsboard
            array.append(formular) #append to the array to be returned to the pioneer600
        #if the moisture <= the threshold
        else:
            data6["EPH"] = "Water Now" #put the MLR data into dictionary
            output6 = json.dumps(data6) #dump the dictionary into json
            client.publish(topic,output6) #push the json data into thingsboard
            array.append("Water Now") #append to the array to be returned to the pioneer600
        return array
    else:
        formular = "Error"
        data6["EPH"] = formular #put the MLR data into dictionary
        output6 = json.dumps(data6) #dump the dictionary into json
        client.publish(topic,output6) #push the json data into thingsboard
        array.append(formular) #append to the array to be returned to the pioneer600
        return array

#Determine the plant health level status by color of the leafs
def get_PlantStatus(array):
    plant_status = take_picture.take_picture() #call the function
    if plant_status is not None:
        data7["Plant Status"] = plant_status #put the MLR data into dictionary
        output7 = json.dumps(data7) #dump the dictionary into json
        client.publish(topic,output7) #push the json data into thingsboard
        array.append(plant_status) #append to the array to be returned to the pioneer600
        return array
    else:
        plant_status = "Error"
        data7["Plant Status"] = plant_status #put the MLR data into dictionary
        output7 = json.dumps(data7) #dump the dictionary into json
        client.publish(topic,output7) #push the json data into thingsboard
        array.append(plant_status) #append to the array to be returned to the pioneer600
        return array

#get message from C file
def get_Time(array):
    string_lib = ctypes.cdll.LoadLibrary('/home/pi/Desktop/pioneer600/getTime.so')
    string_lib.get_string.restype = ctypes.c_char_p
    myString = str(string_lib.get_string()) #access the function
    array.append(myString[2:-1])
    now = datetime.datetime.now() #get datetime now
    datenow = now.strftime("%Y-%m-%d") #format datetime
    array.append(str(datenow))
    timenow = now.strftime("%H:%M:%S")
    array.append(str(timenow))
    return array
    
def main():
    array = []
    get_LDR(array)
    get_Moisture(array)
    get_TempHum(array)
    get_Germination(array[0],array[1],array[2],array[3],array)
    get_EPH(array[1], array[2], array[3], array)
    get_PlantStatus(array)
    get_Time(array)
    return array
