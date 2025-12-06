import json
import logging
import re
from pathlib import Path
from mods import storage
from mods.change_existing_tech_tree import CIV_TECH_MATRIX, TECH_IDS_BY_SLOT

logging.getLogger(__name__)

NAME = "post_mod_json_editing"

#@NewCivs
CIV_NAMES = ["Aztecs", "Berbers", "Britons", "Burgundians", "Bulgarians", "Burmese", "Byzatines", "Celts", "Chinese", "Cumans", "Ethiopians", "Franks", "Goths", "Huns", "Incas",
             "Indians", "Italians", "Japenese", "Khmer", "Koreans", "Lithuanians", "Magyars", "Malay", "Malians", "Mayans", "Mongols", "Persians", "Portuguese", "Saracens", "Sicilians",
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
    iconFilePath = (storage.blwDatPath / "futureavailableunits.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File

    for civ in CIV_NAMES:
        civdata = data.get(str(civ))
        buildings = civdata.setdefault("Buildings", []) if isinstance(civdata, dict) else None
        for i, building in enumerate(buildings):
            for i, techAccess in enumerate(CIV_TECH_MATRIX.get(str(civ), None)):
                if (building.get("ID") == 87):
                    tech_archery = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    throwerRequiredAge = [3, 4, 4]
                    for idx, throwername in enumerate(storage.throwerUpgradeNames):
                        throwerTechDict = {
                            "ID": storage.throwerUpgradeTechs[idx],
                            "Name": f"{throwername}",
                            "RequiredAge": throwerRequiredAge [idx]
                        }
                        #if (CI)
                        tech_archery.append(throwerTechDict)
                if (building.get("ID") == 12 and techAccess[i]):
                    shieldBoss = building.setdefault("Techs", []) if isinstance(building, dict) else None
                    RequiredAge = 3
                    for idx, throwername in enumerate(storage.throwerUpgradeNames):
                        throwerTechDict = {
                            "ID": storage.shieldBossTechId,
                            "Name": f"{storage.shieldBossUpgradeName}",
                            "RequiredAge": RequiredAge
                        }
                        shieldBoss.append(shieldBoss)

    outputFilePath = (Path(__file__).parent / "blw dat" / "newfuturavailableunits.json").resolve() # Path of output Json File        
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
    
    