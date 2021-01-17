from picamera import PiCamera
from time import sleep
import color_brown
import color_green

def take_picture():
    # Create a Pi Camera object
    camera = PiCamera()
    
    # Set the Pi Camera Resolution to 1280x720
    camera.resolution = (1280, 720)
    
    # Sleep the Camera for 5 seconds before taking a picture
    # This gives the camera sensor time to sense the light levels
    sleep(5)
    
    # Image is captured and stored on the Desktop
    camera.capture('/home/pi/Desktop/test.jpg')
    
    # Release the camera resources
    camera.close()
    
    # Call the color detection algorithmn for detecting brown
    # This would return the amount of brown pixel in percentage
    brown = color_brown.get_Brown()
    
    # Call the color detection algorithmn for detecting green
    # This would return the amount of green pixel in percentage
    green = color_green.get_Green()
    
    # The idea is that there should be a threshold for the percentage of green/brown pixel to compare it with
    # The health status would be updated accordingly if the percentage of green/brown pixel is within or out of the threshold
    # Due to time constrain to find out the threshold we are unable to do it
    # Hence for demostration sake we'll just compare the percentage of green to brown pixel to show our proof of concept
    # Compare the percentage of green and brown pixel to determine the healthiness of the plant
    if (green > brown):
        return ('Plant is healthy')
    else:
        return ('Plant is unhealthy')


