import json
from mods import storage



def run_change_iconsJson():
    create_modified_iconsJson()

def create_modified_iconsJson():
    iconFilePath = (storage.blwDatPath / "icons.json").resolve() # Path of json File
    with open(iconFilePath,"r") as f:
        data = json.load(f)    # Load the data of Json File
    
    techstrings = ["Scytheman", "FlailWarrior", "HeavyLancer", "KnifeThrower", "HatchetThrower", "Ninja", 
                   "ThrowingTechniques", "WoodenGrip", "Holster", "BalancedWeaponry", "ShieldBoss"]
    Techidx = storage.si+1
    for techname in techstrings:
        data['Techs'].update({f"{Techidx}": "TechIconsT"+str(Techidx)+str(techname)})
        Techidx +=1

    outputFilePath = (storage.widgetUIFolder / "icons.json").resolve()         
    with open (outputFilePath, "w") as output:
        json.dump(data, output, indent=2)