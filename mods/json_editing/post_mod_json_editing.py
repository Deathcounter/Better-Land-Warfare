import json
import logging
import re
from mods import storage

logging.getLogger(__name__)

NAME = "post_mod_json_editing"

def run_post_mod_json_editing():
    create_modified_unitcategoriesJson()

def create_modified_unitcategoriesJson():
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
    siege = data.setDefault("SiegeWeapons", [])
    siege.append(dictEntry)
    
    
       

    outputFilePath = (storage.datFolder / "unitcategories.json").resolve() # build path of output File        
    with open (outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)


