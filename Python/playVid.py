
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
    buf = ""
    while(cap.isOpened() and not event.is_set()):
        
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('frame', frame)
            
        # Press Q on keyboard to exit
            print("event.is_set(): " + str(event.is_set()))
            key = cv2.waitKey(20)
            
            if key != -1:
                print("key: " + str(key))
                buf += chr(key)
                while True:
                    theKey = cv2.waitKey(100)
                    if theKey != -1:
                        buf += chr(theKey)
                    else:
                        break
                print("buf: " + str(buf))
                # returnVal = 
                break
            elif(event.is_set()):
                break
    
    # Break the loop
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()
    print("buf final: " + str(buf))
    return buf
# Read Video 
def readVideoTime(vidName, duration, origTime):
    # Create a VideoCapture object and read from input file
    print("pogs" + str(time.time()) + " " + str(origTime))
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
        print("hi")
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
        # Display the resulting frame
            
            frame = cv2.resize(frame, (screen_width, screen_height))
            cv2.imshow('frame', frame)
            
        # Press Q on keyboard to exit
            wait_key = cv2.waitKey(20)
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
    root.destroy()

def chooseVideo(event, data, secondQueue):
    #Choosing Vid Logic:
    pokName = -1
    itemList = []
    print("pokemon_id: " + str(data["pokemon_id"]))
    if data["pokemon_id"]:
        print(data["pokemon_id"])
        pokName = data["pokemon_id"]
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
    
    readVideoEvent(vidName, event)
    secondQueue.put(itemList)
    return itemList

def readVideoEvent(vidName, event):
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
            key = cv2.waitKey(20)
        
            if(event.is_set()):
                break
    
    # Break the loop
        else:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    # When everything done, release
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()
    return

# Initial Instructions Video
def instructionsVid(event,queue):
    
    queue.put(readVideo("../Videos/defaultVid.mp4", event))
    return 0

# 
def displayItemYouGot(pokemon, duration):
    readVideoTime(str(pokemon), duration, time.time())

