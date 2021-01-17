import RPi.GPIO as GPIO
import web

PIN = 7
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(PIN, GPIO.OUT)
        
urls = (
    '/', 'index',
    '/open','open',
    '/close', 'close'
)
app = web.application(urls, globals())

class index:        
    def GET(self):
        return '<a href="/open" >Open</a><a href="/close">Close</a>'
class open:
    def GET(self):
        GPIO.output(PIN,GPIO.LOW)
        return 'open'
class close:
    def GET(self):
        GPIO.output(PIN,GPIO.HIGH)
        return 'close'

if __name__ == "__main__":
    app.run()
    GPIO.cleanup()