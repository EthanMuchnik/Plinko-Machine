import RPi.GPIO as GPIO

# Return the breakbeam that got triggered
def mainFunc(secondQueue):
    BEAM_PIN = 24
    BEAM_PIN2 = 23
    BEAM_PIN3 = 27
    BEAM_PIN4 = 22
    BEAM_PIN5 = 25

    returnPin = -1

    def break_beam_callback(channel):
        nonlocal returnPin
        if channel == BEAM_PIN:
            returnPin = 1
        elif channel == BEAM_PIN2:
            returnPin = 2
        elif channel == BEAM_PIN3:
            returnPin = 3
        elif channel == BEAM_PIN4:
            returnPin = 4
        elif channel == BEAM_PIN5:
            returnPin = 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BEAM_PIN, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN2, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN3, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN4, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN5, GPIO.FALLING, callback=break_beam_callback)
    while True:
        if returnPin != -1:
            GPIO.cleanup()
            secondQueue.put(returnPin)
            return returnPin
        
if __name__ == "__main__":
    mainFunc()
