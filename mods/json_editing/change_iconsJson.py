import json
import logging
from mods import storage

logging.getLogger(__name__)

NAME = "change_iconsJson"

def run_change_iconsJson():
    create_modified_iconsJson()

def create_modified_iconsJson():
    iconFilePath = (storage.blwDatPath / "icons.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data = json.load(f)    # Load the data of Json File
    
    # All tech Strings
    
    Techidx = storage.si+1
    for techname in storage.techStrings:
        # store all "TechIconsT[idx][Techname]"" in a list for later use
        storage.techIconList.append(f"TechIconsT"+str(Techidx)+techname)
        # Append keys to the "Tech" header(?)
        data['Techs'].update({f"{Techidx}": "TechIconsT"+str(Techidx)+str(techname)})
        Techidx +=1 # increment it

    outputFilePath = (storage.widgetUIFolder / "icons.json").resolve() # build path of output File        
    with open (outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2)