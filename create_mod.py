#! /usr/bin/env python3


import argparse
import hashlib
import pickle
import logging
import json

from pathlib import Path

from genieutils.datfile import DatFile

from mods.json_editing import pre_mod_json_editing
from mods.json_editing import post_mod_json_editing

from mods import add_sounds
from mods import add_graphics
from mods import add_projectiles
from mods import add_units
from mods import add_effects
from mods import add_technologies
from mods import add_tasks
from mods import change_existing_units
from mods import change_existing_techs
from mods import change_existing_civs
from mods import change_existing_tech_tree

from mods import storage


logging.basicConfig(level=logging.INFO, filename="logs_BLL.txt", filemode="w", format="%(levelname)s - %(message)s")

supported_languages = []
# Overall, genieutils works by loading a .dat file into memory and constructing a DatFile object
# This is done with the DatFile.parse method
# Once the object has been parsed, you make the modifications you want to the object
# Once this is complete, you can write the new object to a new file using the DatFile.save method
def main():
    reading_blw_dat_folder()
    create_file_structure()
    pre_mod_json_editing.run_pre_mod_json_editing()
    creating_moving_mod_files()
    make_ingame_modifications()
    post_mod_json_editing.run_post_mod_json_editing() # some json files require data from the Ingame altering, such as Unit IDs


# this function checks if all folders and files exist in the directory. It also reads the first informations (languages in language file), last vanilla tech index etc.
def reading_blw_dat_folder():
    storage.blwDatPath = (Path(__file__).parent / "blw dat")
    iconFilePath = (Path(__file__).parent / "blw dat" / "icons.json") # Path of json File
    storage.constantsPath = (Path(__file__).parent / "blw dat" / "constants") 
    languageFilePath = (Path(__file__).parent / "blw dat" / "constants" / "key-value-modded-strings-utf8.txt") 
    if not iconFilePath.exists():
        print("No file named icons.json found in blw dat folder.")
        print(f"\nSuggested Troubleshoot:\n* Copy the icons.json from the gamefiles (\\Steam\\steamapps\\common\\AoE2DE\\widgetui) in the blw dat folder")
        quit()
    if not storage.blwDatPath.exists():
        print("Error creating mod, no folder called \"blw dat\" found.")
        print(f"\nSuggested Troubleshoot:\n* Create a blw dat folder name in {Path(__file__).parent}")
        quit()
    if not storage.constantsPath.exists():
        print("No folder named \"constants\" found in blw dat folder.")
        print(f"\nSuggested Troubleshoot:\n* If you do not have the constants folder, then there is something seriously wrong and you should probably download the repo again")
        quit()
    if not languageFilePath.exists():
        print("No file named \"key-value-modded-strings-utf8.txt\" found in blw dat/constants folder.")
        print(f"\nSuggested Troubleshoot:\n* If you do not have the the language file, then there is something seriously wrong and you should probably download the repo again")
        quit()

    with open(languageFilePath, "r", encoding="utf-8") as langfile:
        for line in langfile:
            line = line.rstrip().rstrip('\n').lstrip("/") # turning //NewLang=en with any blanks and the \n at the end into just NewLang=en
            if line.startswith("NewLang="):
                langshort = line[-2:] # the last two characters after "NewLang="
                supported_languages.append(langshort)

    logging.info(f"Found a total of {len(supported_languages)} languages in the language file")    



    with open(iconFilePath,"r") as f:
        data = json.load(f)    # Load the data of Json File
        
    tech_keys = data.get("Techs", {}) # Get the keys
    try:
        # find highest key and convert it to int
        last_tech_key = max(int(idx) for idx in tech_keys.keys() if idx.lstrip("0").isdigit() or idx.isdigit())
    except ValueError:
        # this should never happen
        last_tech_key = None

    # store for later use
    if last_tech_key is not None:
        storage.si = last_tech_key # store highest key as integer
    


# this function creates all the folders and stores all the paths needed for later
def create_file_structure():
    rel_directory = (Path(__file__).parent / "finished_mods").resolve()
    rel_directory.mkdir(parents=True, exist_ok=True)
    storage.datFolder = (Path(__file__).parent / "finished_mods" / "Better Land Warfare (Official Data Mod)" / "resources" / "_common" / "dat").resolve()
    storage.datFolder.mkdir(parents=True, exist_ok=True)
    storage.soundFolder = (storage.datFolder.parent / "drs" / "sounds").resolve()
    storage.soundFolder.mkdir(parents=True, exist_ok=True)
    storage.dataModFolder = (rel_directory / "Better Land Warfare (Official Data Mod)").resolve()


    # languages = ["br", "de", "en", "es", "fr", "hi", "it", "jp", "ko", "ms", "mx", "pl", "ru", "tr", "tw", "vi", "zh"] # all languages as of 29.11.25
    # checking all languages in supported languages (generated by reading "NewLang=" tags in the string file)

    for lang_shortcut in supported_languages:
        lang_folders = (Path(__file__).parent / "finished_mods" / "Better Land Warfare (Official Data Mod)" / "resources" / f"{lang_shortcut}" / "strings" / "key-value").resolve()
        lang_folders.mkdir(parents = True, exist_ok=True)
        storage.languageFolders.append(lang_folders)

    storage.UIModFolder = (rel_directory / "Better Land Warfare (Official UI Mod)" )
    storage.widgetUIFolder = (Path(__file__).parent / "finished_mods" / "Better Land Warfare (Official UI Mod)" / "widgetui").resolve()
    storage.widgetUIFolder.mkdir(parents=True, exist_ok=True)
    storage.techIconFolder = (Path(__file__).parent / "finished_mods" / "Better Land Warfare (Official UI Mod)" / "widgetui" / "textures" / "ingame" / "tech").resolve()
    storage.techIconFolder.mkdir(parents=True, exist_ok=True)




# this function actually creates or moves the file from blw dat to the mod folders, exlucding jsons that get altered in pre_mod_json_files()
def creating_moving_mod_files():
    idx = -2
    languageFilePath = (Path(__file__).parent / "blw dat" / "constants" / "key-value-modded-strings-utf8.txt") 
    filecontent = []
    with open(languageFilePath, "r", encoding="utf-8") as langfile:
        for line in langfile:
            if line.startswith("//NewLang"):
                idx+=1
                if idx>=0:
                    with open(storage.languageFolders[idx] / "key-value-modded-strings-utf8.txt", "w", encoding="utf-8") as outputfile:
                        outputfile.write(''.join(filecontent))
                        filecontent.clear()
                
            else:
                filecontent.append(line)
        with open(storage.languageFolders[idx+1] / "key-value-modded-strings-utf8.txt", "w", encoding="utf-8") as outputfile:
            outputfile.write(''.join(filecontent))
            filecontent.clear()

            


def make_ingame_modifications():
    print("Loading base data...")
    cache_file = None
    cache_file, dfBase = load_cache(Path("datfiles/base_game.dat"))
    if not dfBase:
        print("Parsing...")
        dfBase = DatFile.parse("datfiles/base_game.dat")
        write_cache(dfBase, cache_file)

    print("Base data loaded")
    print("Applying modifications")
    
    add_sounds.run_add_sounds (dfBase)
    add_graphics.run_add_graphics (dfBase)
    add_projectiles.run_add_projectiles (dfBase)
    add_units.run_add_units(dfBase)
    add_effects.run_add_effects (dfBase)
    add_technologies.run_add_technologies (dfBase)
    add_tasks.run_add_tasks (dfBase)
    change_existing_units.run_change_existing_units (dfBase)
    change_existing_techs.run_change_existing_techs (dfBase)
    change_existing_civs.run_change_existing_civs (dfBase)
    change_existing_tech_tree.run_change_tech_tree (dfBase)
    
    print("Modifications completed")

    # You can save it as whatever filename.dat you want, but when it is in a mod you will need it to be named empires2_x2_p1.dat
    print("Saving file...")
    dfBase.save("datfiles/empires2_x2_p1.dat")
    print("Process completed!")

# Since there is a lot of overhead accomplished by the parsing and saving, it may take a while
# To speed this up, genieutils-py allows for the option of caching this parsing
# However, this is completely optional and you can remove the load_cache and write_cache functions if they don't work correctly
def load_cache(input_file: Path) -> tuple[Path, DatFile | None]:
    file_hash = get_file_hash(input_file)
    cache_file = Path("/tmp/aoe2") / f"{file_hash}.pickle"
    data = None
    if cache_file.is_file():
        data = pickle.loads(cache_file.read_bytes())
    else:
        print("Cache file does not exist")
    return cache_file, data


def write_cache(data: DatFile, cache_file: Path):
    cache_file.parent.mkdir(exist_ok=True, parents=True)
    cache_file.write_bytes(pickle.dumps(data))


def get_file_hash(input_file: Path) -> str:
    with input_file.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()



if __name__ == "__main__":
    main()
