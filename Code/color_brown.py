import cv2
import numpy as np

def get_Brown():
    # Open the image you want to process
    image = cv2.imread('/home/pi/Desktop/test.jpg')

    # Convert RGB to HSV (Hue Saturation Value) for better color segmentation result
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Setting the upper and lower range for the spectrum of brown
    lower_brown = np.array([0, 100, 20]) 
    upper_brown = np.array([20, 255, 255])

    # With the upper and lower range, construct a brown mask
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

    # Using the mask we are able to count the number of pixel which are brown in the image
    count_brown = cv2.countNonZero(brown_mask)
    
    # Convert the amount of brown pixel to percentage
    # The total amount of brown pixel in this case is 921600 as the camera resolution is set to 1280 x 720
    percent_brown = count_brown/921600*100

    return (percent_brown)
