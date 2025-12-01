import json
import logging
from mods import storage



def run_change_materialsJson():
    create_modified_materialsJson()

def create_modified_materialsJson():
    iconFilePath = (storage.blwDatPath / "materials.json").resolve() # Path of input json File
    with open(iconFilePath,"r", encoding="utf-8") as f:
        data: dict = json.load(f)    # Load the data of Json File
    

    # Actually I do not need two different functions here, I could pass the dictonary names (Materials, MaterialDef and Name)
# as function parameters, whoever I think this makes it easier to understand > having cleaner code

    def insert_mat_after_prefix(data: dict, prefix: str, new_entry: dict) -> bool:
        # Insert new_entry into data['Materials'] immediately after first MaterialDef with Name starting with prefix.
        mats = data.setdefault("Materials", [])
        for i, item in enumerate(mats):
            md = item.get("MaterialDef") if isinstance(item, dict) else None
            name = md.get("Name") if isinstance(md, dict) else None
            if isinstance(name, str) and name.startswith(prefix):
                mats.insert(i + 1, new_entry)
                return True # Successfully inserted at found last vanilla item
        mats.append(new_entry)
        return False # Just appended at the end because no TechIconsT[int] name found
    
    def insert_atlas_after_prefix(data: dict, prefix: str, new_entry: dict) -> bool:
        # Insert new_entry into data['AtlasTextures'] immediately after first Texture with Name starting with prefix.
        atlas = data.setdefault("AtlasTextures", [])
        for i, item in enumerate(atlas):
            AtlasD = item.get("AtlasDef") if isinstance(item, dict) else None
            name = AtlasD.get("Name") if isinstance(AtlasD, dict) else None
            if isinstance(name, str) and name.startswith("ingametechs"):
                textureList = AtlasD.setdefault("Textures", [])
                for i, texture in enumerate(textureList):
                    refName = texture.get("RefName") if isinstance(texture, dict) else None
                    if isinstance(refName, str) and refName.startswith(prefix):
                        textureList.insert(i + 1, new_entry)
                        return True
        
                atlas.append(new_entry)
                return False # Just appended at the end because no TechIconsT[int] name found
    


    #The JSON directory where I need to add my for the AtlasTextures stuff is actually one directory deeper than Materials
    #dataAtlasTexture = data.setdefault("AtlasTextures", [])

    # Here I say that my JSON Key/Values should be appended after the last Vanilla Tech
    prefix = f"TechIconsT{storage.si}"
    # debugging counters
    counter = 0
    counter2 = 0
    # Example: iterate a list from storage and add one custom Material after the other
    # I need to reverse it because the entry is ALWAYS, added after the last Vanilla Tech, therefore without reversed it would append items like that:
    # First iteration: x 1 ... second iteration: x 2 1 ... third: x 3 2 1 - as it is always adding it after the x (= last vanilla tech), the last one comes first
    for tech_value in reversed(storage.techIconList):

       
        # Build the material entry you want to add. Adjust fields as needed.
        materialDef= {
            "MaterialDef": {
                "Name": f"{tech_value}",
                "Type": "Atlas",
                "Blend": "AlphaPlayerColor",
                "TextureRef": f"{tech_value}",
                "AtlasRef": "ingametechs"
            }
        }
        # inserting data in Material header of the json File
        inserted = insert_mat_after_prefix(data, prefix, materialDef)
        if(not inserted):
            counter+=1


        textures= {
            "Textures": {
                "RefName": f"{tech_value}",
                "FileName": "textures/ingame/tech/",
                "imageTLX": "0.588350",
                "imageTLY": "0.470703",
                "imageBRX": "0.646944",
                "imageBRY": "0.529297"

            }
        }
        insertedAtlas = insert_atlas_after_prefix(data, prefix, textures)
        if(not insertedAtlas):
            counter2+=1
    logging.info (f"added MaterialDefs with {counter}, and Textures at Atlas with {counter2} failed insertions (appendings)")
    outputFilePath = (storage.widgetUIFolder / "materials.json").resolve() # Path of output Json File
    with open(outputFilePath, "w", encoding="utf-8") as output:
        json.dump(data, output, indent=2, ensure_ascii=False)
