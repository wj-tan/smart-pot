import cv2
import numpy as np

def get_Green():
    # Open the image you want to process
    image = cv2.imread('/home/pi/Desktop/test.jpg')

    # Convert RGB to HSV (Hue Saturation Value) for better color segmentation result
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Setting the upper and lower range for the spectrum of green
    lower_green = np.array([20, 40, 20]) 
    upper_green = np.array([75, 255, 255])

    #Filter out the color green in the image
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

     # Using the mask we are able to count the number of pixel which are green in the image
    count_green = cv2.countNonZero(green_mask)

    # Convert the amount of green pixel to percentage
    # The total amount of green pixel in this case is 921600 as the camera resolution is set to 1280 x 720
    percent_green = count_green/921600*100

    return (percent_green)
