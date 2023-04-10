import breakScript as brk
import playVid as PV
import multiprocessing as mult
import pokemon as pok

def mainLoop():


    
    event = mult.Event()
    defProc = mult.Process(target=PV.defaultVid, args=(event,))
    defProc.start()

    rfidVal = input("RFID")

    # Database check with RFID and return all relevant data
    # TODO RFIDData = DatabaseData() (JEWSKY)

    # Wait Until RFID Read
    event.set()
    defProc.join()


    pBreakBeam = mult.Process(target=PV.mainLoop)
    pVid = mult.Process(target=PV.chooseVideo, args=(event, RFIDData))

    eventMain = mult.Event()
    pBreakBeam.start()
    pVid.start()

    pBreakBeam.join()
    eventMain.set()
    pVid.join()

    breakBeam = pBreakBeam.exitcode
    newPok = pVid.exitcode
    
    if RFIDData[returning] == True:
        RFIDData[pokemon_xp] += 20
        if (RFIDData[pokemon_id] not in pok.finalPok):
            if breakBeam ==3 or pokemon_xp > pok.FirstEvol:
                RFIDData[pokemon_id] = pok.evolutionDict[RFIDData[pokemon_id]]
                RFIDData[attack] += pok.evolutionStatBoost[RFIDData[pokemon_id]][0]
                RFIDData[defense] += pok.evolutionStatBoost[RFIDData[pokemon_id]][1]
                RFIDData[speed] += pok.evolutionStatBoost[RFIDData[pokemon_id]][3]
                RFIDData[health] += pok.evolutionStatBoost[RFIDData[pokemon_id]][4]
                if RFIDData[pokemon_id] in pok.finalPok:
                    RFIDData[pokemon_xp] = pok.LastEvol
                elif RFIDData[pokemon_id] not in pok.finalPok:
                    RFIDData[pokemon_xp] = pok.FirstEvol
            else:
                if breakBeam == 1:
                    RFIDData[attack] +=pok.attackInc
                elif breakBeam ==2:
                    RFIDData[defense] +=pok.defenseInc
                elif breakBeam ==4:
                    RFIDData[speed] +=pok.speedInc
                elif breakBeam ==5:
                    RFIDData[health] +=pok.healthInc

        elif (RFIDData[pokemon_id] in pok.finalPok):
            if breakBeam == 3:
                RFIDData[attack] += pok.evolutionStatBoost[RFIDData[pokemon_id]][0]
                RFIDData[defense] += pok.evolutionStatBoost[RFIDData[pokemon_id]][1]
                RFIDData[speed] += pok.evolutionStatBoost[RFIDData[pokemon_id]][3]
                RFIDData[health] += pok.evolutionStatBoost[RFIDData[pokemon_id]][4]
            elif breakBeam ==1:
                RFIDData[attack] +=pok.attackInc
            elif breakBeam ==2:
                RFIDData[defense] +=pok.defenseInc
            elif breakBeam ==4:
                RFIDData[speed] +=pok.speedInc
            elif breakBeam ==5:
                RFIDData[health] +=pok.healthInc
    else: # new
        if breakBeam ==3:
            RFIDData[pokemon_id] = newPok[breakBeam]
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
        else:
            # TODO Pokemon Speed, Attack, Defense, Health, XP attributes Set
            if breakBeam == 1:
                RFIDData[pokemon_id] = "balbasaur"
                
            elif breakBeam ==2:
                RFIDData[pokemon_id] = "squirtle"
            elif breakBeam ==4:
                RFIDData[pokemon_id] = "charmander"
            elif breakBeam ==5:
                RFIDData[pokemon_id] = "pikachu"
        RFIDData[attack] = pok.baseStats[RFIDData.pokemon_id][0]
        RFIDData[defense] = pok.baseStats[RFIDData.pokemon_id][1]
        RFIDData[speed] = pok.baseStats[RFIDData.pokemon_id][2]
        RFIDData[health] = pok.baseStats[RFIDData.pokemon_id][3]
        RFIDData[pokemon_xp] = pok.baseStats[RFIDData.pokemon_id][4]

# TODO write code to display pokemon you received for x ammount of seconds
# The above will likely use concurrency 

# TODO Write Code to update database with RFIDData : Jewsky Code


if __name__ == "__main__":
    while True:
        mainLoop()