
# importing libraries
import cv2
import numpy as np
import random as rand
import ctypes
import pokemon as pok
import tkinter as tk
import time

from pymongo import MongoClient
from bson.objectid import ObjectId

uri = "mongodb+srv://admin:aepibooth2023@booth.fvs2kjk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.booth
rfidMap = db.rfid_mappings
collectionMap = db.users





# Read Video 
def readVideo(vidName, event):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(vidName)
    print("vidName:" + str(vidName))
    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file")

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Read until video is completed
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # Read until video is completed
    while(cap.isOpened() and not event.is_set()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('frame', frame)
            
        # Press Q on keyboard to exit
            print("event.is_set(): " + str(event.is_set()))
            start_time = time.time()
            theInput = None
            while True:
                if time.time() - start_time > 0.03:
                    break
                theInput = input("gimmeRFID")
                print("theInput: " + str(theInput))

            if theInput or event.is_set():
                # returnVal = 
                break
    
    # Break the loop
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

# Read Video 
def readVideoTime(vidName, duration, origTime):
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(vidName)

    # Check if camera opened successfully
    if (cap.isOpened()== False):
        print("Error opening video file") 
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Read until video is completed
    cv2.namedWindow("frame", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    while(cap.isOpened()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('Frame', frame)
            
        # Press Q on keyboard to exit
            if (time.time() - origTime) > duration:
                break
    
    # Break the loop
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()

def chooseVideo(event, data):
    #Choosing Vid Logic:
    pokName = -1
    itemList = []
    if data["pokemon_name"]:
        print(data["pokemon_name"])
        pokName = data["pokemon_name"]
        if (pokName not in pok.finalPok):
            vidName = "../Videos/" + "ret"+ pok.evolutionDict[pokName] + ".mp4"
            itemList = ["attack", "defense",pok.evolutionDict[pokName], "speed", "health"]
        else:
            vidName = "../Videos/" + "retboxes.mp4"
            itemList = ["attack", "defense",pokName, "speed", "health"]
    else: # new with vidname corresponding to middle pokemon
        pokName = pok.evolutionDict[pok.starterPok[rand.randint(0,3)]]
        vidName = "../Videos/" + pokName + ".mp4"
        itemList = ["bulbasaur", "squirtle",pokName, "charmander", "pikachu"]

    readVideo(vidName, event)

    return itemList

# Initial Instructions Video
def instructionsVid(event):
    return readVideo("../Videos/defaultVid.mp4", event)

# 
def displayItemYouGot(pokemon, duration):
    readVideoTime(str(pokemon) + ".mp4", duration, time.time())

