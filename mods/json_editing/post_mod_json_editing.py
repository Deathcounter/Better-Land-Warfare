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

def run_post_mod_json_editing():
    create_modified_unitCategoriesJson()
    create_modified_futureAvailUnitsJson()

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
    iconFilePath = (storage.blwDatPath / "futuravailableunits.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File
    replaceCivNames = {"Franks": "French", "Britons": "British", "Byzantines": "Byzantine", "Indians": "Hindustanis", "Mayans": "Mayan"}
    for idx, civ in enumerate(CIV_NAMES):
        civdata = data.get(civ)
        if (civ in replaceCivNames):
            civ = replaceCivNames.get(civ)
        buildings = civdata.setdefault("Buildings", []) if isinstance(civdata, dict) else None
        techlist = CIV_TECH_MATRIX.get(civ)
        #print(idx) just helped me figuring out which civ names I couldnt spell
        for i in range(len(techlist)):
            for building in buildings:
                if (i in [1, 10, 11] and building.get("ID") == 12):
                    barrackTechs = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    barrackUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    if (i == 1):
                        billmanUnitDict = {
                            "ID": storage.BillmanIDs[0],
                            "Name": storage.billmanNames[0],
                            "RequiredAge": 2
                        }
                        barrackUnits.append(billmanUnitDict) # billman is availale for all civs always, therefore there is no check
                    if (i == 1 and techlist[i] == 1):
                        RequiredAge = 3 if civ is not "Armenians" else 2
                        shieldBossDict = {
                            "ID": storage.shieldBossTechId,
                            "Name": storage.shieldBossUpgradeName,
                            "RequiredAge": RequiredAge
                        }
                        barrackTechs.append(shieldBossDict)
                    if (i == 10 and techlist[i] == 1):
                        RequiredAge = 3 if civ is not "Armenians" else 2
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
                        RequiredAge = 4 if civ is not "Armenians" else 3
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
                    if (i == 2 and civ is "Japanese"):
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
                if (i in [9,10] and building.get("ID") == 101):
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
                            "Name": storage.lancerUpgradeName[1],
                            "RequiredAge": 4
                        }
                        stableUnits.append(heavyLancerUnitDict)
                        stableTechs.append(heavyLancerTechDict)
                if (building.get("ID") == 49):
                    siegeUnits = building.setdefault("Units", []) if isinstance(building, dict) else None
                    flameThrowerUnitDict = {
                        "ID": storage.FlameThrowerID,
                        "Name": storage.flamethrowerName,
                        "RequiredAge": 4   
                    }
                    siegeUnits.append(flameThrowerUnitDict)
    outputFilePath = (storage.blwDatPath / "newfuturavailableunits.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
    
    