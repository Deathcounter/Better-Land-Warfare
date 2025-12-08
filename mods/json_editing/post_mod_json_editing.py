import json
import logging
import re
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
    create_modified_unitCategoriesJson()
    create_modified_futureAvailUnitsJson()
    create_modified_unitlinesJson()
    create_modified_civTechTreesJson()

def create_modified_unitCategoriesJson():
    iconFilePath = (storage.blwDatPath / "unitcategories.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data = json.load(f)    # Load the data of Json File
    

    
    for idx, billManName in enumerate(storage.billmanNames):
        dictEntry = {
            "Name": f"{billManName}",
            "ID": storage.BillmanIDs[idx]
        }
        infantry = data.setdefault("Infantry", [])
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
            civ = REPLACE_CIV_NAMES.get(civ)
        buildings = civdata.setdefault("Buildings", []) if isinstance(civdata, dict) else None
        techlist = CIV_TECH_MATRIX.get(civ)
        #print(idx) just helped me figuring out which civ names I couldnt spell
        for i in range(len(techlist)):
            for building in buildings:
                if (i in [1, 10, 11] and building.get("ID") == 12):
                    barrackTechs = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    barrackUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    if (i == 1): # just once
                        billmanUnitDict = {
                            "ID": storage.BillmanIDs[0],
                            "Name": storage.billmanNames[0],
                            "RequiredAge": 2
                        }
                        barrackUnits.append(billmanUnitDict) # billman is availale for all civs always, therefore there is no check
                    if (i == 1 and techlist[i] == 1):
                        RequiredAge = 3 if civ != "Armenians" else 2
                        shieldBossDict = {
                            "ID": storage.shieldBossTechId,
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

                if (i in [2, 6, 7] and building.get("ID") == 87):
                    rangeTech = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    rangeUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    if (i == 2):
                        dartThrowerUnitDict = {
                            "ID": storage.ThrowerIDs[0],
                            "Name": storage.throwerNames[0],
                            "RequiredAge": 2
                        }
                        rangeUnits.append(dartThrowerUnitDict)
                    if (i == 2 and civ == "Japanese"):
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
                if (i in [3, 4, 5] and building.get("ID") == 103):
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
                if (i in [8,9] and building.get("ID") == 101):
                    stableTechs = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    stableUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    
                    if (i == 9 and techlist[i] == 1):
                        lancerUnitDict = {
                            "ID": storage.LancerIDs[0],
                            "Name": storage.lancerNames[0],
                            "RequiredAge": 3
                        }
                        stableUnits.append(lancerUnitDict)
                    if (i == 10 and techlist[i] == 1):
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
                if (i == 1 and building.get("ID") == 49):
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
    REPLACE_CIV_NAMES.update({"Magyar": "Magyars"})

    civTechTreePath = (storage.blwDatPath / "civTechTrees.json").resolve() # Path of input json File
    with open(civTechTreePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File
    
    civs = data.setdefault("civs", [])
    

    throwerUnitAmount = len(storage.ThrowerIDs)
    billmanUnitAmount = len(storage.BillmanIDs)
    lancerUnitAmount = len(storage.LancerIDs)
    flamethrowerUnitAmount = 1
    for civ in civs:
        civname: str = civ.get("civ_id")
        civname = civname.capitalize() # civTechTree contains all civs with Uppercase letters: "AZTECS" - but both my global Dict use "Aztecs" -> capitalize() needed
        if (civname in REPLACE_CIV_NAMES):
            civname = REPLACE_CIV_NAMES.get(civname)
        if (civname not in CIV_TECH_MATRIX.keys()):
            continue

        unitDicts = build_BLW_unitDict(civname)
        units: list[dict] = civ.setdefault("civ_techs_units", [])
        for idx, unit in enumerate(units):
            # if "Cavalry Archer" in unit.values(): - to check if there even is an Cavalry Archer, but there should always be (unless non AoE2 civs)
            if unit.get("Name") == "Cavalry Archer":
                for unitindex in range(throwerUnitAmount-1):
                    units.insert(idx+unitindex, unitDicts[unitindex])
                break

    outputFilePath = (storage.datFolder / "civTechTrees.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)


def build_BLW_unitDict(civname: str) -> list[dict]:
    logging.debug("Added civTechTree for following civs" + civname)
    unitDict: list[dict] = []

    throwerAges = [2,3,4,4] # Feudal, Castle, Imp, Imp - might want to add that to storage if needed elsewhere
    LinkIDs = storage.ThrowerIDs.copy() # The link ID is always the ID of the previous Node ID. The NodeID is the Id of the Unit and links to other NodeIDs specified in "LinkID"
    LinkIDs.insert(0, -1) # Therefore the linked ID list always is one idx behind the thrower IDs and the base unit has no LinkID (therefore -1 inserted at 0)
    TriggerTechIDs = storage.throwerUpgradeTechs.copy() # Same goes for Trigger Tech ID
    TriggerTechIDs.insert(0, -1)

    from mods.change_existing_tech_tree import CIV_TECH_MATRIX

    availability = CIV_TECH_MATRIX.get(civname) 

    throwerAvailList = []
    throwerAvailList.extend((1, availability[6], availability[7]))
    
    for idx in range(len(storage.ThrowerIDs)-1):
        NodeType = "Unit" if idx == 0 else "UnitUpgrade" # the base unit is not an upgrade and just exists in Feudal (like archer)
        LinkNodeType = "Building Tech" if idx == 0 else "Unit" # also changes like Node Type and is another conditions for the lines to appear
        NodeStatus = "NotAvailable" if not throwerAvailList[idx] else "ResearchedCompleted"
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
        unitDict.append(throwerDict)
    """
    billmanAges = [2,3,4] 
    LinkIDs = storage.BillmanIDs.copy() 
    LinkIDs.insert(0, -1)
    TriggerTechIDs = storage.throwerUpgradeTechs.copy()
    TriggerTechIDs.insert(0, -1)
    for idx, thrower in enumerate(storage.ThrowerIDs):
        NodeType = "Unit" if idx == 0 else "UnitUpgrade" # the base unit is not an upgrade and just exists in Feudal (like archer)
        LinkNodeType = "Building Tech" if idx == 0 else "Unit" # also changes like Node Type and is another conditions for the lines to appear
        throwerDict = {
            "Age ID": throwerAges[idx],
            "Building ID": 87,
            "Draw Node Type": "UnitTech",
            "Help String ID": storage.throwerStringID + 100000 + idx,
            "Link ID": LinkIDs[idx],
            "Link Node Type": LinkNodeType,
            "Name": storage.throwerNames[idx],
            "Name String ID": storage.throwerStringID + 9000 + idx,
            "Node ID": thrower,
            "Node Status": "ResearchedCompleted",
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
        unitDict.append(throwerDict)
    """
    return unitDict