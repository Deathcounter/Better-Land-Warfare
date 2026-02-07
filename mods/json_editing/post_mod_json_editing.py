import json
import logging
import re
import copy
from pathlib import Path
from mods import storage


logging.getLogger(__name__)

NAME = "post_mod_json_editing"

#@NewCivs
CIV_NAMES = ["Aztecs", "Berbers", "Britons", "Burgundians", "Bulgarians", "Burmese", "Byzantines", "Celts", "Chinese", "Cumans", "Ethiopians", "Franks", "Goths", "Huns", "Incas",
             "Indians", "Italians", "Japanese", "Khmer", "Koreans", "Lithuanians", "Magyars", "Malay", "Malians", "Mayans", "Mongols", "Persians", "Portuguese", "Saracens", "Sicilians",
             "Slavs", "Spanish", "Tatars", "Teutons", "Turks", "Vietnamese", "Vikings", "Poles", "Bohemians", "Dravidians", "Bengalis", "Gurjaras", "Romans", "Armenians", "Georgians",
             "Shu", "Wu", "Wei", "Jurchens", "Khitans"
            ]

REPLACE_CIV_NAMES = {"Franks": "French", "Britons": "British", "Byzantines": "Byzantine", "Indians": "Hindustanis", "Mayans": "Mayan"}


def run_post_mod_json_editing():
    if (not storage.lightmode):
        create_modified_unitCategoriesJson()
        create_modified_futureAvailUnitsJson()
        create_modified_unitlinesJson()
        create_modified_civTechTreesJson()
        create_modified_techtreepreviewpanelJson()

def create_modified_unitCategoriesJson():
    iconFilePath = (storage.blwDatPath / "unitcategories.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data = json.load(f)    # Load the data of Json File
    

    
    for idx, billManName in enumerate(storage.billmanNames): # Pretty simple, build the dictionary and then append it to the infantry for every billman unit
        dictEntry = {
            "Name": f"{billManName}",
            "ID": storage.BillmanIDs[idx]
        }
        infantry = data.setdefault("Infantry", []) # setdefault = gets a list of dictionaries
        infantry.append(dictEntry)

    for idx, throwerName in enumerate(storage.throwerNames):
        dictEntry = {
            "Name": f"{throwerName}",
            "ID": storage.ThrowerIDs[idx]
        }
        infantry = data.setdefault("Infantry", [])
        infantry.append(dictEntry)

    for idx, lancerName in enumerate(storage.lancerNames):
        dictEntry = {
            "Name": f"{lancerName}",
            "ID": storage.LancerIDs[idx]
        }
        cavalry = data.setdefault("Cavalry", [])
        cavalry.append(dictEntry)

    dictEntry = {
        "Name": f"{storage.flamethrowerName}",
        "ID": storage.FlameThrowerID
    }
    siege = data.setdefault("SiegeWeapons", [])
    siege.append(dictEntry)
    
    
       

    outputFilePath = (storage.datFolder / "unitcategories.json").resolve() # build path of output File        
    with open (outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)


def create_modified_futureAvailUnitsJson():
    from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    futurAvailFilePath = (storage.blwDatPath / "futuravailableunits.json").resolve() # Path of input json File
    with open(futurAvailFilePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File
    for civ in CIV_NAMES:
        civdata = data.get(civ)
        if (civ in REPLACE_CIV_NAMES):
            civ = REPLACE_CIV_NAMES.get(civ) # futureAvail Json uses civ names like "Britons", "Franks", etc. which are missmatched to the actual ingame data
        buildings = civdata.setdefault("Buildings", []) if isinstance(civdata, dict) else None
        techlist = CIV_TECH_MATRIX.get(civ)
        #print(idx) just helped me figuring out which civ names I couldnt spell
        for i in range(len(techlist)): # iterate through all the techs
            for building in buildings: # iterate through all the buildings
                if (i in [1, 10, 11] and building.get("ID") == 12): # 12 = Barracks, 1, 10 and 11 are the barrack techs (Shield Boss, Scythe and Flail)
                    barrackTechs = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    barrackUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    if (i == 1): # just once, could have also just been a boolean flag but "i" is already there
                        billmanUnitDict = {
                            "ID": storage.BillmanIDs[0],
                            "Name": storage.billmanNames[0],
                            "RequiredAge": 2
                        }
                        barrackUnits.append(billmanUnitDict) # billman is availale for all civs always, therefore there is no check
                    if (i == 1 and techlist[i] == 1): # Checks if Civ has Shieldboss (1) available. I actually just use the non Gambeson Shield Boss here because it will only show up if needed
                        RequiredAge = 3 if civ != "Armenians" else 2 # obviously armenians -.-
                        shieldBossDict = {
                            "ID": storage.shieldBossTechId2,
                            "Name": storage.shieldBossUpgradeName,
                            "RequiredAge": RequiredAge
                        }
                        barrackTechs.append(shieldBossDict)
                    if (i == 10 and techlist[i] == 1):
                        RequiredAge = 3 if civ != "Armenians" else 2
                        scythemanTechDict = {
                            "ID": storage.billmanUpgradeTechs[0],
                            "Name": storage.billmanUpgradeNames[0],
                            "RequiredAge": RequiredAge
                        }
                        scythemanUnitDict = {
                            "ID": storage.BillmanIDs[1],
                            "Name": storage.billmanNames[1],
                            "RequiredAge": RequiredAge
                        }
                        barrackTechs.append(scythemanTechDict)
                        barrackUnits.append(scythemanUnitDict)

                    if (i == 11 and techlist[i] == 1):
                        RequiredAge = 4 if civ != "Armenians" else 3
                        flailWarriorTechDict = {
                            "ID": storage.billmanUpgradeTechs[1],
                            "Name": storage.billmanUpgradeNames[1],
                            "RequiredAge": RequiredAge
                        }
                        flailWarriorUnitDict = {
                            "ID": storage.BillmanIDs[2],
                            "Name": storage.billmanNames[2],
                            "RequiredAge": RequiredAge
                        }
                        barrackTechs.append(flailWarriorTechDict)
                        barrackUnits.append(flailWarriorUnitDict)

                if (i in [2, 6, 7] and building.get("ID") == 87): # Archery Range and Archery Range Techs/Units (Throwing Techniques, Knife and Hatchet)
                    rangeTech = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    rangeUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    if (i == 2): # Dart Thrower always added, just once (could have also been i == 6 or 7)
                        dartThrowerUnitDict = {
                            "ID": storage.ThrowerIDs[0],
                            "Name": storage.throwerNames[0],
                            "RequiredAge": 2
                        }
                        rangeUnits.append(dartThrowerUnitDict)
                    if (i == 2 and civ == "Japanese"): # Japanese Unique Unit being added here
                        RequiredAge = 4
                        ninjaUnitDict = {
                            "ID": storage.ThrowerIDs[3],
                            "Name": storage.throwerNames[3],
                            "RequiredAge": RequiredAge
                        }
                        ninjaTechDict = {
                            "ID": storage.throwerUpgradeTechs[2],
                            "Name": storage.throwerUpgradeNames[2],
                            "RequiredAge": RequiredAge
                        }
                        rangeTech.append(ninjaTechDict)
                        rangeUnits.append(ninjaUnitDict)
                    
                    if (i == 2 and techlist[i] == 1): 
                        RequiredAge = 2
                        throwingTechniquesDict = {
                            "ID": storage.throwingTechniquesTechID,
                            "Name": storage.throwingTechniquesUpgradeName,
                            "RequiredAge": RequiredAge
                        }
                        rangeTech.append(throwingTechniquesDict)
                    if (i == 6 and techlist[i] == 1):
                        RequiredAge = 3
                        knifeThrowerTechDict = {
                            "ID": storage.throwerUpgradeTechs[0],
                            "Name": storage.throwerUpgradeNames[0],
                            "RequiredAge": RequiredAge
                        }
                        knifeThrowerUnitDict = {
                            "ID": storage.ThrowerIDs[1],
                            "Name": storage.throwerNames[1],
                            "RequiredAge": RequiredAge
                        }
                        rangeTech.append(knifeThrowerTechDict)
                        rangeUnits.append(knifeThrowerUnitDict)
                    if (i == 7 and techlist[i] == 1):
                        RequiredAge = 4
                        HatchetThrowerTechDict = {
                            "ID": storage.throwerUpgradeTechs[1],
                            "Name": storage.throwerUpgradeNames[1],
                            "RequiredAge": RequiredAge
                        }
                        HatchetThrowerUnitDict = {
                            "ID": storage.ThrowerIDs[2],
                            "Name": storage.throwerNames[2],
                            "RequiredAge": RequiredAge
                        }
                        rangeTech.append(HatchetThrowerTechDict)
                        rangeUnits.append(HatchetThrowerUnitDict)
                if (i in [3, 4, 5] and building.get("ID") == 103): # Blacksmith Techs (Wooden Grip, Holster, Balanced Weaponry)
                    blacksmithTech = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    if (i == 3):
                        woodenGripDict = {
                            "ID": storage.throwerBlacksmithTechIDs[0],
                            "Name": storage.throwerBlacksmithUpgradeNames[0],
                            "RequiredAge": 2
                        }
                        blacksmithTech.append(woodenGripDict)
                    
                    if (i == 4 and techlist[i] == 1):
                        holsterDict = {
                            "ID": storage.throwerBlacksmithTechIDs[1],
                            "Name": storage.throwerBlacksmithUpgradeNames[1],
                            "RequiredAge": 3
                        }
                        blacksmithTech.append(holsterDict)
                    if (i == 5 and techlist[i] == 1):
                        balancedWeaponryDict = {
                            "ID": storage.throwerBlacksmithTechIDs[2],
                            "Name": storage.throwerBlacksmithUpgradeNames[2],
                            "RequiredAge": 4
                        }
                        blacksmithTech.append(balancedWeaponryDict)
                if (i in [8,9] and building.get("ID") == 101): # Stable (Lancer/Heavy Lancer)
                    stableTechs = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    stableUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    
                    if (i == 8 and techlist[i] == 1):
                        lancerUnitDict = {
                            "ID": storage.LancerIDs[0],
                            "Name": storage.lancerNames[0],
                            "RequiredAge": 3
                        }
                        stableUnits.append(lancerUnitDict)
                    if (i == 9 and techlist[i] == 1):
                        heavyLancerUnitDict = {
                            "ID": storage.LancerIDs[1],
                            "Name": storage.lancerNames[1],
                            "RequiredAge": 4
                        }
                        heavyLancerTechDict = {
                            "ID": storage.lancerUpgradeTech,
                            "Name": storage.lancerUpgradeName,
                            "RequiredAge": 4
                        }
                        stableUnits.append(heavyLancerUnitDict)
                        stableTechs.append(heavyLancerTechDict)
                if (i == 1 and building.get("ID") == 49): # Siege Workshop 
                    siegeUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    flameThrowerUnitDict = {
                        "ID": storage.FlameThrowerID,
                        "Name": storage.flamethrowerName,
                        "RequiredAge": 4   
                    }
                    siegeUnits.append(flameThrowerUnitDict)
    outputFilePath = (storage.datFolder / "futuravailableunits.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)




def create_modified_unitlinesJson():
    unitLinesFilePath = (storage.blwDatPath / "unitlines.json").resolve() # Path of input json File
    with open(unitLinesFilePath,"r", encoding="utf-8") as f:
        data = json.load(f)    # Load the data of Json File
    UnitLines = data.setdefault("UnitLines", []) # get the list of dictionaries
    linelist = []
    availNumbers = []
    for line in UnitLines:
        linelist.append(line.get("LineID")) # get all line IDs

    for idx in range (-399,-199):
        if idx not in linelist: # if numbers from 399 to 200 are not in the already present line IDs = free available ID
            availNumbers.append(idx) # append the available ID
    if (len(availNumbers) <=4):
        print("Warning: unitlinesJson has run out of IDs within the valid -400, -199 range")

    # @TotalUnitLines = 3
    UnitLineNames = ["Thrower", "Billman", "Lancer"] # Flamethrower not needed here, units that only consist of a single unit (e.g Condos, Jian Swordsman, Flemish Militia), are not a "line"
    UnitLineIDs = [storage.ThrowerIDs, storage.BillmanIDs, storage.LancerIDs]
    for idx, unit in enumerate(UnitLineNames):
        lineDict = {
            "Name": unit + " Line",
            "Identifier": (unit + "-line").lower(),
            "LineID": availNumbers[idx],
            "IDChain": UnitLineIDs[idx]
        }
        UnitLines.append(lineDict)

    outputFilePath = (storage.datFolder / "unitlines.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)



def create_modified_civTechTreesJson():
    from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    REPLACE_CIV_NAMES.update({"Magyar": "Magyars"}) # Another file, Another inconsistency with civ names

    civTechTreePath = (storage.blwDatPath / "civTechTrees.json").resolve() # Path of input json File
    with open(civTechTreePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File
    
    civs = data.setdefault("civs", [])
    

    throwerUnitAmount = len(storage.ThrowerIDs)-1 # the only reason why -1 is that the Ninja is in ThrowerIDs but I dont actually care while creating the tech tree
    billmanUnitAmount = len(storage.BillmanIDs)
    lancerUnitAmount = len(storage.LancerIDs)

    armenianidx = 0
    armenian_techDicts = None
    moveUUcivs = []
    for cividx, civ in enumerate(civs):
        civname: str = civ.get("civ_id")
        civname = civname.capitalize() # civTechTree contains all civs with Uppercase letters: "AZTECS" - but both my global Dict use "Aztecs" -> capitalize() needed
        if (civname in REPLACE_CIV_NAMES):
            civname = REPLACE_CIV_NAMES.get(civname)
        if (civname not in CIV_TECH_MATRIX.keys()):
            continue # No civ, No service
        if civname == "Armenians":
            armenianidx = cividx    # store which ID is armenians so I can change civs[armenianidx] later
        
        if civname == "Tatars":
            tataridx = cividx
        
        if civname in ["Incas", "Jurchens", "Wei"]:
            moveUUcivs.append(cividx)

        unitDicts = build_BLW_unitDict(civname) # compounds all Dictionaries into a single list of Dictionaries
        techDicts = build_BLW_techDict(civname) # same with techs
        siegeDicts = build_BLW_siegeDict(civname)
        if civname == "Armenians":
            armenianidx = cividx    # store which ID is armenians so I can change civs[armenianidx] later
            armenian_techDicts = copy.deepcopy(techDicts)
        units: list[dict] = civ.setdefault("civ_techs_units", [])

        boolflag = [1,1] # bool flags for when I want to insert before something. 
        # Else it loops forever. cause - imagine a list of [0,2,1], if I say: if slot value = 1, insert x at that index -> [0,2,x,1], then in the next loop, idx+1 is "1" again causing infinite "x"s beinga dded


        # ORDER: All Units and Techs, as well as their Dictbuilding is done from left to right as they are in the Tech Tree - this is also how the tech tree system of the game does it (within one building)
        for idx, unit in enumerate(units):
            # if "Cavalry Archer" in unit.values(): - to check if there even is an Cavalry Archer, but there should always be (unless non AoE2 civs)
            if unit.get("Name") == "Cavalry Archer" and boolflag[0]: # Adding Thrower line before Cav Archer
                boolflag[0] = 0
                for unitindex in range(throwerUnitAmount): 
                    units.insert(idx+unitindex, unitDicts[unitindex]) # insert at unitindex too, but I can also just use (reversed(range)) like below
            if unit.get("Name") == "Thumb Ring" and boolflag[1]: # adding Throwing Techniques before Thumb Ring so all Techs are in the same column
                units.insert(idx, techDicts[0])
                boolflag[1] = 0
            if unit.get("Name") == "Halberdier": # adding Billman line after Halbadier
                for unitindex in reversed(range(throwerUnitAmount, billmanUnitAmount+throwerUnitAmount)):
                    units.insert(idx+1, unitDicts[unitindex])
            if unit.get("Name") == "Gambesons": # adding Shield Boss after Gambesons
                units.insert(idx+1, techDicts[1]) 
            if unit.get("Name") == "Squires":
                unit["Link ID"] = -1 # makes sure that Squares is in the first row of Castle Age

            if unit.get("Name") in ["Paladin", "Savar"]:    
                for unitindex in reversed(range(billmanUnitAmount+throwerUnitAmount,billmanUnitAmount+throwerUnitAmount+lancerUnitAmount)):
                    units.insert(idx+1, unitDicts[unitindex])

            if unit.get("Name") == "Heavy Scorpion": # adding it after Heavy Scorpion in hopes they wont add a second Scorpion Upgrade for another civ, if they do, move it after Houfnice and Traction Trebs  
                units.insert(idx+1, siegeDicts[0])
                
            if unit.get("Name") == "Plate Mail Armor": # adding the Thrower Upgrades after Infantry Defense Upgrades
                for techindex in reversed(range(2, len(storage.throwerBlacksmithIDs)+2)):
                    units.insert(idx+1, techDicts[techindex]) 
                break

            


    # ugh, let's just hope no new civ will ever, EVER have Archery or Stable techs one age earlier
    armenianunits: list[dict] = civs[armenianidx].setdefault("civ_techs_units", []) 

    # ARMENIANS
    # Essentially what this does (have the vanilla Armenian tech tree open to understand better, imagine Shield Boss below Gambesons):
    # Save Arson dict in a temporary variable (that actually gets done mulitple times because of the loop)
    # Add *' Gambesons and Shield Boss after Flailwarrior (flailWarrioridx+1 and +2 - overwrites arson and Gambesons - the overwritten Gambesons is already duplicate *' ), 
    # Add Arson back after where Gambesons was, and remove the duplicate Shield Boss
    # Done, and Squires(-1) and Spearman(+1) one Age earlier or later - and Link ID Squires with Arson so its below it (but no connection line due to lack of "Link Node Type": "Research)
    for idx, unit in enumerate(armenianunits): # this shuffeling around of dictionary entries works as long as no more techs are added between Squires and Arson, else gg
        if unit.get("Name") == "Spearman":
            unit["Age ID"] = 2
        if unit.get("Name") == "Flail Warrior":
            flailWarrioridx = idx
        if unit.get("Name") == "Arson":
            tempArson = unit
        if unit.get("Name") == "Gambesons":
            unit["Age ID"] = 2
            armenianunits[flailWarrioridx+1] = unit
            if armenian_techDicts is not None:
                armenian_techDicts[1]["Age ID"] = 2
                armenianunits.insert(flailWarrioridx+2, copy.deepcopy(armenian_techDicts[1])) 
            armenianunits[idx+1] = tempArson
            armenianunits.pop(idx+2) # Removes a duplicate Shield Boss
        if unit.get("Name") == "Squires":
            unit["Link ID"] = 602
            unit["Age ID"] = 2
            break # all done, all changed, lets break out of the loop to save time

    # Incas, Wei, Jurchens        
    # Here I essentially just move the UU to below the Elite Skirmisher. This makes it so that throwing technique doesnt need its own row
    UUnames = ["Slinger", "Xianbei Raider", "Grenadier"]
    for cividx, shuffleciv in enumerate(moveUUcivs):
        shufflecivUnits: list[dict] = civs[shuffleciv].setdefault("civ_techs_units", []) 
        for unitidx, unit in enumerate(shufflecivUnits):
            if unit.get("Name") == "Elite Skirmisher":
                newUUslot = unitidx + 1 # storing where I will insert it (after ES)
            if unit.get("Name") == UUnames[cividx]:
                unit["Link ID"] = 6 # I need to link it below the Skirmisher
                storeUUdict = unit # storing the UU
                shufflecivUnits.pop(unitidx) # delete UU from Tech tree since we stored it
                shufflecivUnits.insert(newUUslot, storeUUdict) # insert the dict
                # @MayBreak
                # I can't follow the code here, because Wei and Jurchens have Thumbring coming before Parthian Tactics, the order should actually be switched and Incas be the exception
            if unit.get("Name") == "Parthian Tactics": # for some reason, Parthian Tactics for civs with Archery Ranged UU comes before Thumbring, instead of after it
                tempPT = unit # storing Parthian tactics
                popidx = unitidx # storing index of old Parthian Tactics
            if unit.get("Name") == "Thumb Ring": # for civ with an archery UU the Thumbring is below that UU, being linked with the UU - makes sense for the base game but not blw
                unit["Link ID"] = -1 # removes that link
                shufflecivUnits.insert(unitidx+1, tempPT) # adds Parthian Tactics after TR
                break
        # this code is messy, its just that Incas is Slingers is followed by Parthian Tactics, then Thumbring. While Grenadier and Xianbei Raider are followed by Thumbring, then Parthian Tactics
        if cividx == 0:
            shufflecivUnits.pop(popidx) # remove the duplicate Parthian Tactics for Incas
        if cividx != 0:
            shufflecivUnits.pop(popidx+2) # remove the duplicate Parthian Tactics for Wei, Jurchens
    
    tatarunits: list[dict] = civs[tataridx].setdefault("civ_techs_units", []) 
    for unitidx, unit in enumerate(tatarunits):
        if unit.get("Name") == "Flaming Camel":
            unit["Link ID"] = 36 # Link to Bombard Cannon
            flaming_camel = unit
            tatarunits.pop(unitidx)
        if unit.get("Name") == "Bombard Cannon":
            tatarunits.insert(unitidx+1, flaming_camel)
            break

    outputFilePath = (storage.datFolder / "civTechTrees.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)

def build_BLW_techDict(civname: str) -> list [dict]:
    techDict: list [dict] = []
    from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    techAvailability = CIV_TECH_MATRIX.get(civname)

    # Adding Throwing Techniques

    NodeStatus = "NotAvailable" if not techAvailability[2] else "ResearchedCompleted"
    throwingtechniquesDict = {
        "Age ID": 2,
        "Building ID": 87,
        "Draw Node Type": "UnitTech",
        "Help String ID": storage.throwingTechniquesStringID + 100000,
        "Link ID": -1,
        "Link Node Type": "BuildingTech",
        "Name": storage.throwingTechniquesUpgradeName,
        "Name String ID": storage.throwingTechniquesStringID + 9000,
        "Node ID": storage.throwingTechniquesTechID,
        "Node Status": NodeStatus,
        "Node Type": "Research",
        "Picture Index": storage.si + 7,
        "Prerequisite IDs": [
          0,
          0,
          0,
          0,
          0
        ],
        "Prerequisite Types": [
          "None",
          "None",
          "None",
          "None",
          "None"
        ],
        "Trigger Tech ID": -1,
        "Use Type": "Tech"


    }
    techDict.append(throwingtechniquesDict)


    # Adding Shield Boss

    LinkNodeType = "Research"
    NodeID = storage.shieldBossTechId
    if (techAvailability[1] == 1): # if civ has no Gambesons but Shield Boss -> Remove connection line at tech tree and make it seperate tech
        LinkNodeType = "BuildingTech"
        NodeID = storage.shieldBossTechId2

    NodeStatus = "NotAvailable" if not techAvailability[0] else "ResearchedCompleted"
    shieldbossDict = {
        "Age ID": 3,
        "Building ID": 12,
        "Draw Node Type": "UnitTech",
        "Help String ID": storage.shieldBossStringID + 100000,
        "Link ID": 875, # Gambesons,
        "Link Node Type": LinkNodeType,
        "Name": storage.shieldBossUpgradeName,
        "Name String ID": storage.shieldBossStringID + 9000,
        "Node ID": NodeID,
        "Node Status": NodeStatus,
        "Node Type": "Research",
        "Picture Index": storage.si + 11,
        "Prerequisite IDs": [
          0,
          0,
          0,
          0,
          0
        ],
        "Prerequisite Types": [
          "None",
          "None",
          "None",
          "None",
          "None"
        ],
        "Trigger Tech ID": -1,
        "Use Type": "Tech"
    }
    
        
    techDict.append(shieldbossDict)

    techDict.extend(build_BLW_blacksmithDict(civname, techAvailability))

    return techDict

def build_BLW_unitDict(civname: str) -> list[dict]:
    logging.debug("Added civTechTree for following civs" + civname)
    unitDict: list[dict] = []
    from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    availability = CIV_TECH_MATRIX.get(civname) 

    unitDict.extend(build_throwerDict(civname, availability))
    unitDict.extend(build_billmanDict(civname, availability))
    unitDict.extend(build_lancerDict(civname, availability))
    
    
    return unitDict

def build_throwerDict(civname: str, availability: list[int]) -> list[dict]:
    throwerAges = [2,3,4,4] # Feudal, Castle, Imp, Imp - might want to add that to storage if needed elsewhere
    LinkIDs = storage.ThrowerIDs.copy() # The link ID is always the ID of the previous Node ID. The NodeID is the Id of the Unit and links to other NodeIDs specified in "LinkID"
    LinkIDs.insert(0, -1) # Therefore the linked ID list always is one idx behind the thrower IDs and the base unit has no LinkID (therefore -1 inserted at 0)
    TriggerTechIDs = storage.throwerUpgradeTechs.copy() # Same goes for Trigger Tech ID
    TriggerTechIDs.insert(0, -1)
    throwerDictList = []    

    throwerAvailList = []
    throwerAvailList.extend((1, availability[6], availability[7]))
    
    for idx in range(len(storage.ThrowerIDs)-1):
        NodeType = "Unit" if idx == 0 else "UnitUpgrade" # the base unit is not an upgrade and just exists in Feudal (like archer)
        if idx == 0:
            LinkNodeType = "Building Tech" # The first unit of a unit line has to be a "Building Tech"
        elif idx == 1:
            LinkNodeType = "Unit" # The second unit of a unit line has to be a "Unit"
        else:
            LinkNodeType = "UnitUpgrade" # The remaining ones have to be a "UnitUpgrade", why? well idk, just observing current civTechTree.json
        
        NodeStatus = "NotAvailable" if not throwerAvailList[idx] else "ResearchedCompleted" # Actual tech tree availability logic
        linkidx = 0
        if civname == "Japanese" and idx == 2:
            idx = 3
            NodeType = "UniqueUnit"
            linkidx = 1
            NodeStatus = "ResearchedCompleted"
        throwerDict = {
            "Age ID": throwerAges[idx],
            "Building ID": 87,
            "Draw Node Type": "UnitTech",
            "Help String ID": storage.throwerStringID + 100000 + idx,
            "Link ID": LinkIDs[idx-linkidx],
            "Link Node Type": LinkNodeType,
            "Name": storage.throwerNames[idx],
            "Name String ID": storage.throwerStringID + 9000 + idx,
            "Node ID": storage.ThrowerIDs[idx],
            "Node Status": NodeStatus,
            "Node Type": NodeType,
            "Picture Index": storage.throwerUnitIcons[idx],
            "Prerequisite IDs": [
              0,
              0,
              0,
              0,
              0
            ],
            "Prerequisite Types": [
              "None",
              "None",
              "None",
              "None",
              "None"
            ],
            "Trigger Tech ID": TriggerTechIDs[idx],
            "Use Type": "Unit"
        }
        throwerDictList.append(throwerDict)
    return throwerDictList

def build_billmanDict(civname: str, availability: list[int]) -> list[dict]:
    billmanAges = [2,3,4] 
    LinkIDs = storage.BillmanIDs.copy()
    LinkIDs.insert(0, -1) 
    TriggerTechIDs = storage.billmanUpgradeTechs.copy() 
    TriggerTechIDs.insert(0, -1)
    billmanDictList = []        
    billmanAvailList = []
    billmanAvailList.extend((1, availability[10], availability[11]))

    for idx in range(len(storage.ThrowerIDs)-1):
        NodeType = "Unit" if idx == 0 else "UnitUpgrade" 
        if idx == 0:
            LinkNodeType = "Building Tech" 
        elif idx == 1:
            LinkNodeType = "Unit" 
        else:
            LinkNodeType = "UnitUpgrade" 

        NodeStatus = "NotAvailable" if not billmanAvailList[idx] else "ResearchedCompleted"
        if civname == "Armenians": #ughh and thats the easier part than moving all the techs
            billmanAges = [2,2,3]      
        billmanDict = {
            "Age ID": billmanAges[idx],
            "Building ID": 12,
            "Draw Node Type": "UnitTech",
            "Help String ID": storage.billmanStringID + 100000 + idx,
            "Link ID": LinkIDs[idx],
            "Link Node Type": LinkNodeType,
            "Name": storage.billmanNames[idx],
            "Name String ID": storage.billmanStringID + 9000 + idx,
            "Node ID": storage.BillmanIDs[idx],
            "Node Status": NodeStatus,
            "Node Type": NodeType,
            "Picture Index": storage.billmanUnitIcons[idx],
            "Prerequisite IDs": [
              0,
              0,
              0,
              0,
              0
            ],
            "Prerequisite Types": [
              "None",
              "None",
              "None",
              "None",
              "None"
            ],
            "Trigger Tech ID": TriggerTechIDs[idx],
            "Use Type": "Unit"
        }
        billmanDictList.append(billmanDict)
    return billmanDictList

def build_lancerDict(civname: str, availability: list[int]) -> list[dict]:
    lancerAges = [3,4] 
    LinkIDs = storage.LancerIDs.copy()
    LinkIDs.insert(0, -1) 
    TriggerTechIDs = []
    TriggerTechIDs.insert(0, -1)
    TriggerTechIDs.insert(1, storage.lancerUpgradeTech)
    lancerDictList = []        
    lancerAvailList = []
    lancerAvailList.extend((availability[8], availability[9]))

    for idx in range(len(storage.LancerIDs)):
        NodeType = "Unit" if idx == 0 else "UnitUpgrade" 
        if idx == 0:
            LinkNodeType = "Building Tech" 
        elif idx == 1:
            LinkNodeType = "Unit" 
        else:
            LinkNodeType = "UnitUpgrade" 

        NodeStatus = "NotAvailable" if not lancerAvailList[idx] else "ResearchedCompleted"    
        lancerDict = {
            "Age ID": lancerAges[idx],
            "Building ID": 101,
            "Draw Node Type": "UnitTech",
            "Help String ID": storage.lancerStringID + 100000 + idx,
            "Link ID": LinkIDs[idx],
            "Link Node Type": LinkNodeType,
            "Name": storage.lancerNames[idx],
            "Name String ID": storage.lancerStringID + 9000 + idx,
            "Node ID": storage.LancerIDs[idx],
            "Node Status": NodeStatus,
            "Node Type": NodeType,
            "Picture Index": storage.lancerUnitIcons[idx],
            "Prerequisite IDs": [
              0,
              0,
              0,
              0,
              0
            ],
            "Prerequisite Types": [
              "None",
              "None",
              "None",
              "None",
              "None"
            ],
            "Trigger Tech ID": TriggerTechIDs[idx],
            "Use Type": "Unit"
        }
        lancerDictList.append(lancerDict)
    return lancerDictList

def build_BLW_blacksmithDict(civname: str, techAvailability) -> list [dict]:
    blacksmithAges = [2,3,4] 
    LinkIDs = storage.throwerBlacksmithTechIDs.copy()
    LinkIDs.insert(0, -1) 
    blacksmithAvailList = []
    blacksmithAvailList.extend((techAvailability[3], techAvailability[4], techAvailability[5])) 
    techDict: list [dict] = []
    from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    techAvailability = CIV_TECH_MATRIX.get(civname)

    # Adding Blacksmith Upgrades
    for idx in range (len(storage.throwerBlacksmithTechIDs)):
        if idx == 0:
            LinkNodeType = "Building Tech" 
        else:
            LinkNodeType = "Research" 
        NodeStatus = "NotAvailable" if not blacksmithAvailList[idx] else "ResearchedCompleted"
        blacksmithDict = {
            "Age ID": blacksmithAges[idx],
            "Building ID": 103,
            "Draw Node Type": "UnitTech",
            "Help String ID": storage.throwerBlacksmithStringIDs[idx] + 100000,
            "Link ID": LinkIDs[idx],
            "Link Node Type": LinkNodeType,
            "Name": storage.throwerBlacksmithUpgradeNames [idx],
            "Name String ID": storage.throwerBlacksmithStringIDs[idx] + 9000,
            "Node ID": storage.throwerBlacksmithTechIDs[idx],
            "Node Status": NodeStatus,
            "Node Type": "Research",
            "Picture Index": storage.si + 8 + idx,
            "Prerequisite IDs": [
              0,
              0,
              0,
              0,
              0
            ],
            "Prerequisite Types": [
              "None",
              "None",
              "None",
              "None",
              "None"
            ],
            "Trigger Tech ID": -1,
            "Use Type": "Tech"


        }
        techDict.append(blacksmithDict)
    return techDict

def build_BLW_siegeDict(civname: str) -> list [dict]:
    techDict: list [dict] = []
    # from mods.change_existing_tech_tree import CIV_TECH_MATRIX
    # techAvailability = CIV_TECH_MATRIX.get(civname)

    # Adding Flame Thrower

    # NodeStatus = "NotAvailable" if not techAvailability[2] else "ResearchedCompleted"
    flameThrowerDict = {
        "Age ID": 4,
        "Building ID": 49,
        "Draw Node Type": "UnitTech",
        "Help String ID": storage.flamethrowerStringID + 100000,
        "Link ID": 542,
        "Link Node Type": "BuildingTech",
        "Name": storage.flamethrowerName,
        "Name String ID": storage.flamethrowerStringID + 9000,
        "Node ID": storage.FlameThrowerID,
        "Node Status": "ResearchedCompleted",
        "Node Type": "Unit",
        "Picture Index": storage.flamethrowerUnitIcon,
        "Prerequisite IDs": [
          0,
          0,
          0,
          0,
          0
        ],
        "Prerequisite Types": [
          "None",
          "None",
          "None",
          "None",
          "None"
        ],
        "Trigger Tech ID": -1,
        "Use Type": "Unit"


    }
    techDict.append(flameThrowerDict)
    return techDict

def create_modified_techtreepreviewpanelJson():
    ttpreviewPath = (storage.blwDatPath / "techtreepreviewpanel.json").resolve() # Path of input json File
    with open(ttpreviewPath,"r", encoding="utf-8") as f:
        data = json.load(f)    # Load the data of Json File

    billmanDict =  {
                        "Widget":{
                            "Type": "TechTreeButton",
                            "Name": "",
                            "ViewPort": {
                                "xorigin": 0,
                                "yorigin": 0,
                                "width": 70,
                                "height": 65,
                                "alignment": "TopLeft"
                            },
                            "Help": "Billman Line",
                            "IconValues": [
                                {
                                    "TechId": storage.billmanAvailTechID,
                                    "UnitId": storage.BillmanIDs[0]
                                },
                                {
                                    "TechId": storage.billmanUpgradeTechs[0],
                                    "UnitId": storage.BillmanIDs[1]
                                },
                                {
                                    "TechId": storage.billmanUpgradeTechs[1],
                                    "UnitId": storage.BillmanIDs[2]
                                }
                            ]
                        }
                    }
    shieldBossDict =  {
                        "Widget":{
                            "Type": "TechTreeButton",
                            "Name": "",
                            "ViewPort": {
                                "xorigin": 0,
                                "yorigin": 0,
                                "width": 70,
                                "height": 65,
                                "alignment": "TopLeft"
                            },
                            "Help": "Shield Boss",
                            "IconValues": [
                                {
                                    "TechId": storage.shieldBossTechId
                                }
                            ]
                        }
                    }
    throwerDict =   {
                        "Widget":{
                            "Type": "TechTreeButton",
                            "Name": "",
                            "ViewPort": {
                                "xorigin": 0,
                                "yorigin": 0,
                                "width": 70,
                                "height": 65,
                                "alignment": "TopLeft"
                            },
                            "Help": "Thrower Line",
                            "IconValues": [
                                {
                                    "TechId": storage.dartthrowerAvailTechID,
                                    "UnitId": storage.ThrowerIDs[0]
                                },
                                {
                                    "TechId": storage.throwerUpgradeTechs[0],
                                    "UnitId": storage.ThrowerIDs[1]
                                },
                                {
                                    "TechId": storage.throwerUpgradeTechs[1],
                                    "UnitId": storage.ThrowerIDs[2],
                                    "ExcludeCivs": True,
                                        "CivIds": [
                                           "JAPANESE-CIV"
                                        ]
                                },
                                {
                                    "TechId": storage.throwerUpgradeTechs[2],
                                    "UnitId": storage.ThrowerIDs[3],
                                    "CivIds": [
                                       "JAPANESE-CIV"
                                        ]
                                }
                            ]
                        }

                    }
    throwingTechniquesDict = {
                        "Widget":{
                            "Type": "TechTreeButton",
                            "Name": "",
                            "ViewPort": {
                                "xorigin": 0,
                                "yorigin": 0,
                                "width": 70,
                                "height": 65,
                                "alignment": "TopLeft"
                            },
                            "Help": "Throwing Techniques",
                            "IconValues": [
                                {
                                    "TechId": storage.throwingTechniquesTechID
                                }
                            ]
                        }
                    }
    lancerDict =   {
                        "Widget":{
                            "Type": "TechTreeButton",
                            "Name": "",
                            "ViewPort": {
                                "xorigin": 0,
                                "yorigin": 0,
                                "width": 70,
                                "height": 65,
                                "alignment": "TopLeft"
                            },
                            "Help": "Lancer Line",
                            "IconValues": [
                                {
                                    "TechId": storage.lancerAvailTechID,
                                    "UnitId": storage.LancerIDs[0]
                                },
                                {
                                    "TechId": storage.lancerUpgradeTech,
                                    "UnitId": storage.LancerIDs[1]
                                }
                            ]
                        }
                    }
    flameThrowerDict =  {
                            "Widget":{
                                "Type": "TechTreeButton",
                                "Name": "",
                                "ViewPort": {
                                    "xorigin": 0,
                                    "yorigin": 0,
                                    "width": 70,
                                    "height": 65,
                                    "alignment": "TopLeft"
                                },
                                "Help": "Flamethrower",
                                "IconValues": [
                                    {
                                        "TechId": storage.flamethrowerAvailTechID,
                                        "UnitId": storage.FlameThrowerID
                                    }
                                ]
                            }
                        }
    blacksmithDict = {
                       "Widget": {
                          "Type": "TechTreeButton",
                          "Name": "",
                          "ViewPort": {
                             "xorigin": 0,
                             "yorigin": 0,
                             "width": 70,
                             "height": 65,
                             "alignment": "TopLeft"
                          },
                          "Help": "Wooden Grip",
                          "IconValues": [
                             {
                                "TechId": storage.throwerBlacksmithTechIDs[0]
                             },
                             {
                                "TechId": storage.throwerBlacksmithTechIDs[1]
                             },
                             {
                                "TechId": storage.throwerBlacksmithTechIDs[2]
                             }
                          ]
                       }
                    }


    entireDict = data.get("Collection")
    widgets = entireDict.setdefault("Widgets", [])
    widget = widgets[0].get("Widget", {}) # at first I didnt understand that Widget is just another Dict in Widgets, so asked AI why widgets[0].get("ChildWidgets")
    childWidgets = widget.get("ChildWidgets")
    # this is getting absurd
    subwidget = childWidgets[0].get("Widget", {}) # line 39 in the file
    realChildWidgets = subwidget.get("ChildWidgets", []) # line 59 in the file

    # And I didnt use AI for this
    
    for widgetDict in realChildWidgets:
        widget = widgetDict.get("Widget", {})
        # Barrack Widget
        if (widget.get("Name")=="Items1"): 
            inserted = 0
            lastWidget = widget.get("ChildWidgets", [])
            boolflag = False
            # Ok so the goal is to add a new unit and a new tech. Billman after Spearman, Shield Boss after Gambeson (no civ specific preview so I can't make shieldBoss and upgrade of Gambesons)
            for idx, unitWidget in enumerate(lastWidget, 1): # so I go through the Widget List of Items1
                realUnitWidget = unitWidget.get("Widget", {})  # get the real Widget not the fake one
                if (inserted != 0 and boolflag): # this adds xorigin and Button ID to all non added techs
                    realUnitWidget["Name"] = "Button" + str(idx) # idx starts at 1!!! this means my (desired) button ID is always my index
                    viewPortDict = realUnitWidget.get("ViewPort")
                    viewPortDict["xorigin"] = viewPortDict.get("xorigin") + (75 * inserted) # I need to add 75 for every insert, before each insert increases the objects xorigin by 75
                boolflag = True    # this flag is telling me that after I Insert, the tech I just inserted will NOT get an extra +1 or +75
                if (realUnitWidget.get("Help") == "Spearman Line"): # Add after Spearman ID
                    billmanWidget = billmanDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = billmanWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75 # I copy the xorigin of the Spearman, and add +75
                    billmanWidget["Name"] = "Button" + str(idx+1) # Same with Button
                    lastWidget.insert(idx, billmanDict) # this inserts it after the Spearman Line
                    inserted += 1 # one insert = +75 for everyone else
                    boolflag = False # bool flag to prevent the code to add additional values as they are already added

                # Listen, now that I am done with the code, I come to think what if I just increase everything by 75 including the tech I just added, but I messed up so I came up with that
                # But now it works also somehow adding the Archery Stuff broke it too?

                # Same with Shield Boss
                if (realUnitWidget.get("Help") == "Gambesons"):
                    shieldBossWidget = shieldBossDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = shieldBossWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75
                    shieldBossWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, shieldBossDict)
                    inserted += 1
                    boolflag = False
                #@MayBreak looks good, idk if actually future proof or if the next tech after Battle Drills will not have some messed up values           
                
        # Archery Range Widget
        if (widget.get("Name")=="Items2"):
            inserted = 0
            lastWidget = widget.get("ChildWidgets", [])
            boolflag = False
            for idx, unitWidget in enumerate((lastWidget), 1):
                realUnitWidget = unitWidget.get("Widget", {})
                if (inserted != 0 and boolflag):
                    realUnitWidget["Name"] = "Button" + str(idx)
                    viewPortDict = realUnitWidget.get("ViewPort")
                    viewPortDict["xorigin"] = viewPortDict.get("xorigin") + (75 * inserted)
                boolflag = True
                if (realUnitWidget.get("Help") == "Skirmisher Line"):
                    throwerWidget = throwerDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = throwerWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75
                    throwerWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, throwerDict)
                    inserted += 1
                    boolflag = False

                if (realUnitWidget.get("Help") == "Thumb Ring"): #@MayBreak - because I append it to the Elephant Archer, - but what if Ele Archer isnt the last Unit anymore
                    throwingTechniquesWidget = throwingTechniquesDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = throwingTechniquesWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75 # +100 instead of +75 because the techs are 25 px away from the units and TT is the first tech
                    throwingTechniquesWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, throwingTechniquesDict)
                    inserted += 1
                    boolflag = False     

        # Stable Widget
        if (widget.get("Name")=="Items3"):
            inserted = 0
            lastWidget = widget.get("ChildWidgets", [])
            boolflag = False
            for idx, unitWidget in enumerate((lastWidget), 1):
                realUnitWidget = unitWidget.get("Widget", {})
                if (inserted != 0 and boolflag):
                    realUnitWidget["Name"] = "Button" + str(idx)
                    viewPortDict = realUnitWidget.get("ViewPort")
                    viewPortDict["xorigin"] = viewPortDict.get("xorigin") + (75 * inserted)
                boolflag = True
                if (realUnitWidget.get("Help") == "Hei Guang Cavalry Line"):
                    lancerWidget = lancerDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = lancerWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75
                    lancerWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, lancerDict)
                    inserted += 1
                    boolflag = False

        # Workshop Widget
        if (widget.get("Name")=="Items4"):
            inserted = 0
            lastWidget = widget.get("ChildWidgets", [])
            boolflag = False
            for idx, unitWidget in enumerate((lastWidget), 1):
                realUnitWidget = unitWidget.get("Widget", {})
                if (inserted != 0 and boolflag):
                    realUnitWidget["Name"] = "Button" + str(idx)
                    viewPortDict = realUnitWidget.get("ViewPort")
                    viewPortDict["xorigin"] = viewPortDict.get("xorigin") + (75 * inserted)
                boolflag = True
                if (realUnitWidget.get("Help") == "Flaming Camel"):
                    flameThrowerWidget = flameThrowerDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = flameThrowerWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75
                    flameThrowerWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, flameThrowerDict)
                    inserted += 1
                    boolflag = False
        
        # Blacksmith Widget
        if (widget.get("Name")=="Items5"):
            inserted = 0
            lastWidget = widget.get("ChildWidgets", [])
            boolflag = False
            for idx, unitWidget in enumerate((lastWidget), 1):
                realUnitWidget = unitWidget.get("Widget", {})
                if (inserted != 0 and boolflag):
                    realUnitWidget["Name"] = "Button" + str(idx)
                    viewPortDict = realUnitWidget.get("ViewPort")
                    viewPortDict["xorigin"] = viewPortDict.get("xorigin") + (75 * inserted)
                boolflag = True
                if (realUnitWidget.get("Help") == "Mail Armor"):
                    blacksmithWidget = blacksmithDict.get("Widget")
                    vp = realUnitWidget.get("ViewPort")
                    currentorigin = vp.get("xorigin")
                    vpDict = blacksmithWidget.get("ViewPort", {})
                    vpDict["xorigin"] = currentorigin + 75
                    blacksmithWidget["Name"] = "Button" + str(idx+1)
                    lastWidget.insert(idx, blacksmithDict)
                    inserted += 1
                    boolflag = False

    
    outputFilePath = (storage.widgetUIFolder / "techtreepreviewpanel.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=3, ensure_ascii=False)