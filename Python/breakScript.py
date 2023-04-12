import RPi.GPIO as GPIO

def mainFunc(secondQueue):
    BEAM_PIN = 24
    BEAM_PIN2 = 23
    BEAM_PIN3 = 27
    BEAM_PIN4 = 22
    BEAM_PIN5 = 26

    returnPin = -1

    def break_beam_callback(channel):
        print("Channel" + str(channel))
        nonlocal returnPin
        if channel == BEAM_PIN:
            print("Beam 1 Falling")
            returnPin = 1
        elif channel == BEAM_PIN2:
            print("Beam 2 Falling")
            returnPin = 2
        elif channel == BEAM_PIN3:
            print("Beam 3 Falling")
            returnPin = 3
        elif channel == BEAM_PIN4:
            print("Beam 4 Falling")
            returnPin = 4
        elif channel == BEAM_PIN5:
            print("Beam 5 Falling")
            returnPin = 5

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BEAM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BEAM_PIN4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BEAM_PIN, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN2, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN3, GPIO.FALLING, callback=break_beam_callback)
    GPIO.add_event_detect(BEAM_PIN4, GPIO.FALLING, callback=break_beam_callback)

    while True:
        if returnPin != -1:
            print("omg wadi")
            GPIO.cleanup()
            secondQueue.put(returnPin)
            return returnPin
        
if __name__ == "__main__":
    mainFunc()
