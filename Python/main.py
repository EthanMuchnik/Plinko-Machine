import breakScript as brk
import playVid as PV
import multiprocessing as mult
import pokemon as pok
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

uri = "mongodb+srv://admin:aepibooth2023@booth.fvs2kjk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.booth
rfidmap = db.rfid_mappings
users = db.users

# Main Loop with multiple processes for RFID Read, Break Beam, and Video Display
def mainLoop():    
    event = mult.Event()
    queue = mult.Queue()
    defProc = mult.Process(target=PV.instructionsVid, args=(event,queue))
    defProc.start()

    # Wait Until RFID Read
    defProc.join()
    rInput = queue.get()[:-1]
    user = rfidmap.find_one({'rfid':rInput})
    if user !=None:
        username = user['username']
    else:
        nR = mult.Process(target = PV.readVideoTime, args = ("../Videos/notRegistered.mp4", 5, time.time()))
        nR.start()
        nR.join()
        return
    RFIDInfo = users.find_one({'username':username})

    eventMain = mult.Event()
    secondQueue = mult.Queue()
    pBreakBeam = mult.Process(target=brk.mainFunc, args=(secondQueue,))
    pVid = mult.Process(target=PV.chooseVideo, args=(eventMain, RFIDInfo, secondQueue))

    pBreakBeam.start()
    pVid.start()

    pBreakBeam.join()
    eventMain.set()
    breakBeam = secondQueue.get()
    pVid.join()

    newPok = secondQueue.get()

    vidrcv = None
    videv = None
    vidName = ""
    vidNameev = ""

    # Case on various fields in Database for uprgading Pokemon
    if RFIDInfo["pokemon_id"]:
        RFIDInfo["pokemon_xp"] += pok.xpInc
        if (RFIDInfo["pokemon_id"] not in pok.finalPok):
            if breakBeam ==3 or RFIDInfo["pokemon_xp"] > pok.FirstEvol:

                RFIDInfo["attack_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_id"]][0]
                RFIDInfo["defense_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_id"]][1]
                RFIDInfo["speed_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_id"]][3]
                RFIDInfo["health_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_id"]][4]
                RFIDInfo["pokemon_id"] = pok.evolutionDict[RFIDInfo["pokemon_id"]]
                if RFIDInfo["pokemon_id"] in pok.finalPok:
                    RFIDInfo["pokemon_xp"] = pok.LastEvol
                elif RFIDInfo["pokemon_id"] not in pok.finalPok:
                    RFIDInfo["pokemon_xp"] = pok.FirstEvol
                
                vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                if breakBeam !=3:
                    vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                    vidrcv = mult.Process(target=PV.displayItemYouGot, args=(vidName, pok.itemReceiveDuration))
                
                vidNameev = "../Videos/ev" + RFIDInfo["pokemon_id"] + ".mp4"
                videv = mult.Process(target=PV.displayItemYouGot, args=(vidNameev, pok.itemReceiveDuration))
            else:
                if breakBeam == 1:
                    RFIDInfo["attack_xp"] +=pok.attackInc
                elif breakBeam ==2:
                    RFIDInfo["defense_xp"] +=pok.defenseInc
                elif breakBeam ==4:
                    RFIDInfo["speed_xp"] +=pok.speedInc
                elif breakBeam ==5:
                    RFIDInfo["health_xp"] +=pok.healthInc
                vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                vidrcv = mult.Process(target=PV.displayItemYouGot, args=("../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4", pok.itemReceiveDuration))
                

        elif (RFIDInfo["pokemon_id"] in pok.finalPok):
            if breakBeam == 3:
                RFIDInfo["attack_xp"] += pok.largeAttackInc
                RFIDInfo["defense_xp"] += pok.largeDefenseInc
                RFIDInfo["speed_xp"] += pok.largeSpeedInc
                RFIDInfo["health_xp"] += pok.largeHealthInc
                RFIDInfo["health_xp"] += pok.largeXPInc - pok.xpInc
                vidName = "../Videos/recAllBoxPrizes.mp4"
                vidrcv = mult.Process(target=PV.displayItemYouGot, args=(vidName, pok.itemReceiveDuration))
            else:
                if breakBeam ==1:
                    RFIDInfo["attack_xp"] +=pok.attackInc
                elif breakBeam ==2:
                    RFIDInfo["defense_xp"] +=pok.defenseInc
                elif breakBeam ==4:
                    RFIDInfo["speed_xp"] +=pok.speedInc
                elif breakBeam ==5:
                    RFIDInfo["health_xp"] +=pok.healthInc
                
                vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                vidrcv = mult.Process(target=PV.displayItemYouGot, args=(vidName, pok.itemReceiveDuration))
                
    else: # new
        if breakBeam ==3:
            RFIDInfo["pokemon_id"] = newPok[breakBeam]
        else:
            if breakBeam == 1:
                RFIDInfo["pokemon_id"] = "bulbasaur"
            elif breakBeam ==2:
                RFIDInfo["pokemon_id"] = "squirtle"
            elif breakBeam ==4:
                RFIDInfo["pokemon_id"] = "charmander"
            elif breakBeam ==5:
                RFIDInfo["pokemon_id"] = "pikachu"
        RFIDInfo["attack_xp"] = pok.baseStats[RFIDInfo["pokemon_id"]][0]
        RFIDInfo["defense_xp"] = pok.baseStats[RFIDInfo["pokemon_id"]][1]
        RFIDInfo["speed_xp"] = pok.baseStats[RFIDInfo["pokemon_id"]][2]
        RFIDInfo["health_xp"] = pok.baseStats[RFIDInfo["pokemon_id"]][3]
        RFIDInfo["pokemon_xp"] = pok.baseStats[RFIDInfo["pokemon_id"]][4]
        vidName = "../Videos/rec" + RFIDInfo["pokemon_id"] + ".mp4"
        vidrcv = mult.Process(target=PV.displayItemYouGot, args=("../Videos/rec" + RFIDInfo["pokemon_id"] + ".mp4", pok.itemReceiveDuration))

    # Display Video
    if vidrcv != None:
        vidrcv.start()
    if vidrcv != None:
        vidrcv.join()
    if videv != None:
        videv.start()
        videv.join()

    users.update_one({"username": RFIDInfo["username"]}, {"$set": RFIDInfo})

if __name__ == "__main__":
    while True:
        mainLoop()