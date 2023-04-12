import breakScript as brk
import playVid as PV
import multiprocessing as mult
import pokemon as pok
from pymongo import MongoClient
from bson.objectid import ObjectId
# import string
uri = "mongodb+srv://admin:aepibooth2023@booth.fvs2kjk.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client.booth
rfidmap = db.rfid_mappings
users = db.users
# testData = {"rfid": "123456789","username": "kidNamedKid", "info" : {"pokemon_xp": 0, "attack_xp": 0, "defense_xp": 0, "speed_xp": 0, "health_xp": 0, "pokemon_name": "raichu"}}

# def getInput():
#     rfidTag = input("Enter RFID Tag: ")
#     return rfidTag

def mainLoop():
    

    
    event = mult.Event()
    queue = mult.Queue()
    defProc = mult.Process(target=PV.instructionsVid, args=(event,queue))
    # rInput = mult.Process(target=getInput, )
    defProc.start()
    # rInput.start()
    # Database check with RFID and return all relevant data
    # TODO RFIDInfo = DatabaseData() (JEWSKY)


    # Wait Until RFID Read
    # rInput.join()
    defProc.join()
    rInput = queue.get()[:-1]
    print("rInput List" + str(list(rInput)))
    print("rInput: " + str(rInput))
    user = rfidmap.find_one({'rfid':rInput})
    print("user: " + str(user))

    username = user['username']
    RFIDData = users.find_one({'username':username})

    RFIDInfo = RFIDData["info"]
    print("RFIDInfo: " + str(RFIDInfo))

    # input("Press Enter to continue...")
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

    print("breakBeam exit code: " + str(breakBeam))
    newPok = secondQueue.get()
    print("newPok exit code: " + str(newPok))

    vidrcv = None
    videv = None
    vidName = ""
    vidNameev = ""
    
    if RFIDInfo["pokemon_name"]:
        print("RFIDInfo[pokemon_name]: " + str(RFIDInfo["pokemon_name"]))   
        RFIDInfo["pokemon_xp"] += pok.xpInc
        if (RFIDInfo["pokemon_name"] not in pok.finalPok):
            if breakBeam ==3 or RFIDInfo["pokemon_xp"] > pok.FirstEvol:
                RFIDInfo["pokemon_name"] = pok.evolutionDict[RFIDInfo["pokemon_name"]]
                RFIDInfo["attack_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_name"]][0]
                RFIDInfo["defense_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_name"]][1]
                RFIDInfo["speed_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_name"]][3]
                RFIDInfo["health_xp"] += pok.evolutionStatBoost[RFIDInfo["pokemon_name"]][4]
                if RFIDInfo["pokemon_name"] in pok.finalPok:
                    RFIDInfo["pokemon_xp"] = pok.LastEvol
                elif RFIDInfo["pokemon_name"] not in pok.finalPok:
                    RFIDInfo["pokemon_xp"] = pok.FirstEvol
                
                vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                if breakBeam !=3:
                    vidrcv = mult.Process(target=PV.displayItemYouGot, args=(vidName, pok.itemReceiveDuration))
                
                vidNameev = "../Videos/ev" + RFIDInfo["pokemon_name"] + ".mp4"
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
                print("breakBeam: " + str(breakBeam))
                vidName = "../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4"
                vidrcv = mult.Process(target=PV.displayItemYouGot, args=("../Videos/rec" + pok.boxPrizes[breakBeam -1] + ".mp4", pok.itemReceiveDuration))
                

        elif (RFIDInfo["pokemon_name"] in pok.finalPok):
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
        print("RFIDInfo[pokemon_name]: " + str(RFIDInfo["pokemon_name"]))   
        if breakBeam ==3:
            RFIDInfo["pokemon_name"] = newPok[breakBeam]
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
        else:
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
            if breakBeam == 1:
                RFIDInfo["pokemon_name"] = "balbasaur"
            elif breakBeam ==2:
                RFIDInfo["pokemon_name"] = "squirtle"
            elif breakBeam ==4:
                RFIDInfo["pokemon_name"] = "charmander"
            elif breakBeam ==5:
                RFIDInfo["pokemon_name"] = "pikachu"
        RFIDInfo["attack_xp"] = pok.baseStats[RFIDInfo["pokemon_name"]][0]
        RFIDInfo["defense_xp"] = pok.baseStats[RFIDInfo["pokemon_name"]][1]
        RFIDInfo["speed_xp"] = pok.baseStats[RFIDInfo["pokemon_name"]][2]
        RFIDInfo["health_xp"] = pok.baseStats[RFIDInfo["pokemon_name"]][3]
        RFIDInfo["pokemon_xp"] = pok.baseStats[RFIDInfo["pokemon_name"]][4]
        vidName = "../Videos/rec" + RFIDInfo["pokemon_name"] + ".mp4"
        vidrcv = mult.Process(target=PV.displayItemYouGot, args=("../Videos/rec" + RFIDInfo["pokemon_name"] + ".mp4", pok.itemReceiveDuration))

# TODO write code to display pokemon you received for x ammount of seconds
# The above will likely use concurrency 
    print("1:" + str(vidName))
    print("1:" + str(vidNameev))
    vidrcv.start()
    #Amazing code to update database
    print("2")
    vidrcv.join()
    print("3")
    if videv != None:
        print("4")
        videv.start()
        print("5")
        videv.join()
        print("6")

    print("RFIDData" + str(RFIDData))
    users.update_one({"username": RFIDData["username"]}, {"$set": RFIDData})
# TODO Write Code to update database with RFIDInfo : Jewsky Code


if __name__ == "__main__":
    while True:
        mainLoop()