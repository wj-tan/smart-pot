# Group 123 Smart Pot
| Name                   | Github ID   | Student ID |
| ---------------------- | ----------- | ---------- |
| CHIA CHENG YEE SHIRLEY | shircjy     | 1901894 |
| DAVID CHUA CHONG REN   | nynm94      | 1901870 |
| NG JIA CHENG           | jiachengng  | 1901825 |
| PUAN JIN YAO, DAREN    | darenpuan   | 1901864 |
| TAN WEI JIAN           | wj-tan      | 1901822 |

## About This Project
This project is about implementing a smart pot with the use of multiple embedded system sensors to gather data surrounding the pot. With the gathered data, we are able to perform machine learning to provide user with interesting information regarding the plant such as "Days to Germination", "Plant Health Status", "Evaporation Per Hour" .

## Video Demostration
Youtube Link : https://www.youtube.com/watch?v=vhHX5zLurIw

## Important

There are a few lines of code that looks for file in the Raspberry Pi directory, hence to ensure that there is no file directory error please create a folder called `pioneer600` on the Raspiberry Pi Desktop and copy everything inside the Code folder that you cloned into the pioneer600 folder you created on the desktop and run the code from there.

Should there be any file directory error, please check the `Sensor.py (line 143)`, `take_picture.py (line 18)`, `color_green.py (line 6)`, `color_brown.py (line 6)` and change it accordingly. Most likely the issue could be that the Raspberry Pi you are using is not on the default username 'pi' , if thats the case please modify the code accordingly `e.g /home/jamespi/Desktop/`

## Raspberry Pi Quick Start Guide

The main computing platform that was used to achieved this project was using the Raspberry Pi 3. Before we begin to install the Pioneer600 and different sensors onto the Raspberry Pi, we recommend that you first run the following commands to on the Raspberry Pi 3 terminal to install the required libraries for the project.

Firstly run the command `sudo apt-get update` on the terminal to re-synchronize the package index files from their sources before you begin installing the different libraries below.

### Pip3

By default, Pip should already installed. If it's not intalled run the following command

`sudo apt install python3-pip`

### Pillow

`sudo pip3 install pillow`

### NumPy

By default, Raspberry Pi OS should already have library NumPy installed. If it's not installed run the following command

`sudo pip3 install numpy`

### Paho-MQTT

`sudo pip3 install paho-mqtt`

### Adafruit DHT Library

`sudo pip3 install Adafruit-DHT`

### SMBus

`sudo pip3 install smbus`

### Pandas

`sudp pip3 install pandas`

`sudo apt-get install libatlas-base-dev`

### SKlearn 

`sudo pip3 install scikit-learn --index-url https://piwheels.org/simple`

### OpenCV

OpenCV will be used to faciliate the process of performing advance functions on the image taken by the Raspberry Pi Camera

`sudo apt-get install libhdf5-dev -y && sudo apt-get install libhdf5-serial-dev -y && sudo apt-get install libatlas-base-dev -y && sudo apt-get install libjasper-dev -y && sudo apt-get install libqtgui4 -y && sudo apt-get install libqt4-test -y`

`pip3 install opencv-contrib-python==4.1.0.25`

