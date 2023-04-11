import breakScript as brk
import playVid as PV
import multiprocessing as mult
import pokemon as pok

testData = {"rfid": "123456789","username": "kidNamedKid", "info" : {"pokemon_name": "", "pokemon_xp": 0, "attack_xp": 0, "defense_xp": 0, "speed_xp": 0, "health_xp": 0, "pokemon_name": "rachi"}}

def mainLoop():


    
    event = mult.Event()
    defProc = mult.Process(target=PV.instructionsVid, args=(event,))
    defProc.start()

    rfidVal = input("RFID")
    
    # Database check with RFID and return all relevant data
    # TODO RFIDData = DatabaseData() (JEWSKY)
    RFIDData = testData


    # Wait Until RFID Read
    event.set()
    defProc.join()


    pBreakBeam = mult.Process(target=brk.mainFunc)
    pVid = mult.Process(target=PV.chooseVideo, args=(event, RFIDData))

    eventMain = mult.Event()
    pBreakBeam.start()
    pVid.start()

    pBreakBeam.join()
    eventMain.set()
    pVid.join()

    breakBeam = pBreakBeam.exitcode
    newPok = pVid.exitcode
    
    if RFIDData["pokemon_name"] == True:
        RFIDData["pokemon_xp"] += 20
        if (RFIDData["pokemon_name"] not in pok.finalPok):
            if breakBeam ==3 or ["pokemon_xp"] > pok.FirstEvol:
                RFIDData["pokemon_name"] = pok.evolutionDict[RFIDData["pokemon_name"]]
                RFIDData["attack_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][0]
                RFIDData["defense_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][1]
                RFIDData["speed_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][3]
                RFIDData["health_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][4]
                if RFIDData["pokemon_name"] in pok.finalPok:
                    RFIDData["pokemon_xp"] = pok.LastEvol
                elif RFIDData["pokemon_name"] not in pok.finalPok:
                    RFIDData["pokemon_xp"] = pok.FirstEvol
            else:
                if breakBeam == 1:
                    RFIDData["attack_xp"] +=pok.attackInc
                elif breakBeam ==2:
                    RFIDData["defense_xp"] +=pok.defenseInc
                elif breakBeam ==4:
                    RFIDData["speed_xp"] +=pok.speedInc
                elif breakBeam ==5:
                    RFIDData["health_xp"] +=pok.healthInc

        elif (RFIDData["pokemon_name"] in pok.finalPok):
            if breakBeam == 3:
                RFIDData["attack_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][0]
                RFIDData["defense_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][1]
                RFIDData["speed_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][3]
                RFIDData["health_xp"] += pok.evolutionStatBoost[RFIDData["pokemon_name"]][4]
            elif breakBeam ==1:
                RFIDData["attack_xp"] +=pok.attackInc
            elif breakBeam ==2:
                RFIDData["defense_xp"] +=pok.defenseInc
            elif breakBeam ==4:
                RFIDData["speed_xp"] +=pok.speedInc
            elif breakBeam ==5:
                RFIDData["health_xp"] +=pok.healthInc
    else: # new
        if breakBeam ==3:
            RFIDData["pokemon_name"] = newPok[breakBeam]
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
        else:
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
            if breakBeam == 1:
                RFIDData["pokemon_name"] = "balbasaur"
                
            elif breakBeam ==2:
                RFIDData["pokemon_name"] = "squirtle"
            elif breakBeam ==4:
                RFIDData["pokemon_name"] = "charmander"
            elif breakBeam ==5:
                RFIDData["pokemon_name"] = "pikachu"
        RFIDData["attack_xp"] = pok.baseStats[RFIDData["pokemon_name"]][0]
        RFIDData["defense_xp"] = pok.baseStats[RFIDData["pokemon_name"]][1]
        RFIDData["speed_xp"] = pok.baseStats[RFIDData["pokemon_name"]][2]
        RFIDData["health_xp"] = pok.baseStats[RFIDData["pokemon_name"]][3]
        RFIDData["pokemon_xp"] = pok.baseStats[RFIDData["pokemon_name"]][4]

# TODO write code to display pokemon you received for x ammount of seconds
# The above will likely use concurrency 

# TODO Write Code to update database with RFIDData : Jewsky Code


if __name__ == "__main__":
    while True:
        mainLoop()