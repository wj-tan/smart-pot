import time
#import Pioneer600
import threading

def restart():
    print("123")

def main():
    while 1:
        t = threading.Timer(10, restart)
        t.start()

main()