
# importing libraries
import cv2
import numpy as np
import random as rand
import ctypes

evolutionDict = {"charmander": "charmeleon", "charmeleon": "charizard", "squirtle": "wartortle", "wartortle": "blastoise", "bulbasaur": "ivysaur", "ivysaur": "venusaur", "pikachu": "raichu"}

# Read Video 
def readVideo(vidName):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(vidName)

    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    
    # Read until video is completed
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while(cap.isOpened()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
    # Break the loop
        else:
            break
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

def chooseVideo():
    #Choosing Vid Logic:
    if True:
        pokName = "pikachu"
        if pokName =="" or pokName == None:
            defaultPokList = ["chamander, squirtle, bulbasaur, pikachu"]
            pokName = defaultPokList[rand.randint(0,3)]
            vidName = "../Videos/" + pokName + ".mp4"

        elif (pokName not in ["charizard","blastoise","venusaur","raichu"]):
            vidName = "../Videos/" + "ret"+ evolutionDict[pokName] + ".mp4"
            print(vidName)
        else:
            vidName = "../Videos/" + "boxes.mp4"
        
    

    while True:
        readVideo(vidName)

def defaultVid():
    readVideo("defaultVid.mp4")

chooseVideo()

