#! /usr/bin/env python3

import dataclasses
import argparse
import hashlib
import pickle
import logging
import json
import shutil

from pathlib import Path
from time import sleep

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
    print("Reading File structure")
    reading_blw_dat_folder()
    print("Create Modfolders")
    create_file_structure()
    print("Editing Jsons before ingame modifications")
    pre_mod_json_editing.run_pre_mod_json_editing()
    print("creating language files")
    creating_lang_files()
    print("Changing all the ingame units, techs etc.")
    make_ingame_modifications()
    print("Editing Jsons to fit the game")
    post_mod_json_editing.run_post_mod_json_editing() # some json files require data from the Ingame altering, such as Unit IDs
    print("Moving remaining files into place")
    #if (not storage.lightmode):
    creating_moving_files()

# this function checks if all folders and files exist in the directory. It also reads the first informations (languages in language file), last vanilla tech index etc.
def reading_blw_dat_folder():
    storage.blwDatPath = (Path(__file__).parent / "blw dat")
    storage.constantsPath = (storage.blwDatPath / "constants") 
    languageFilePath = (storage.blwDatPath / "constants" / "key-value-modded-strings-utf8.txt") 
    if (not storage.blwDatPath.exists()):
        print("Error creating mod, no folder called \"blw dat\" found.")
        print(f"\nSuggested Troubleshoot:\n* Create a blw dat named folder in {Path(__file__).parent}")
        quit()
    if (not storage.constantsPath.exists()):
        print("No folder named \"constants\" found in blw dat folder.")
        print(f"\nSuggested Troubleshoot:\n* If you do not have the constants folder, then there is something seriously wrong and you should probably pull the repo again")
        quit()
    if (not languageFilePath.exists()):
        print("No file named \"key-value-modded-strings-utf8.txt\" found in blw dat/constants folder.")
        print(f"\nSuggested Troubleshoot:\n* If you do not have the the language file, then there is something seriously wrong and you should probably pull the repo again")
        quit()

    check_opening_path() # Checks if all needed jsons are in place

    with open(languageFilePath, "r", encoding="utf-8") as langfile:
        for line in langfile:
            line = line.rstrip().rstrip('\n').lstrip("/") # turning //NewLang=en with any blanks and the \n at the end into just NewLang=en
            if line.startswith("NewLang="):
                langshort = line[-2:] # the last two characters after "NewLang="
                supported_languages.append(langshort)
    # This allows me to have all languages in a single file which later gets splitted up into their own files at create_file_structure():
    logging.info(f"Found a total of {len(supported_languages)} languages in the language file")    


    iconFilePath = (storage.blwDatPath / "icons.json")
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
        logging.info (f"Found last Vanilla Icon at {last_tech_key}")
        print(f"Last Vanilla Icon is at ID {last_tech_key} - you should check if that is correct")
        if not storage.lightmode:
            sleep(3)
    


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




# This function creates the language files
# The structure of the modded string.txt always has: //NewLang=[language] and then all the text in that language.
# Then again NewLang, and the last New Lang never ends until End of Document 
def creating_lang_files():
    idx = -2 # start with -2 because the file starts with NewLang (start read -1), and ends with NewLang (end read at 0)
    languageFilePath = (Path(__file__).parent / "blw dat" / "constants" / "key-value-modded-strings-utf8.txt") # open File
    filecontent = []
    with open(languageFilePath, "r", encoding="utf-8") as langfile:
        for line in langfile: # read document line for line
            if line.startswith("//NewLang"):
                idx+=1 # increase whenever reading "//NewLang"
                if idx>=0: # only at the start needed
                    with open(storage.languageFolders[idx] / "key-value-modded-strings-utf8.txt", "w", encoding="utf-8") as outputfile:
                        outputfile.write(''.join(filecontent)) # Writing like this reduces execution time compared to append (According to Reddit)
                        filecontent.clear() # File written, clear the variable to repeat the for loop
            else:
                filecontent.append(line) # if the line is not starting with NewLang, just append the line
        with open(storage.languageFolders[idx+1] / "key-value-modded-strings-utf8.txt", "w", encoding="utf-8") as outputfile:
            outputfile.write(''.join(filecontent)) # the last language file
            filecontent.clear() # just freeing up the variable

def check_opening_path ():
    jsonNames = ["icons.json", "materials.json", "techtreepreviewpanel.json", "unitcategories.json", "futuravailableunits.json", "unitlines.json", "civTechTrees.json"] # Json File Names
    for idx, jsonName in enumerate(jsonNames): # Lopping
        Pathname = (storage.blwDatPath / jsonName)
        if (not Pathname.exists()): # if Path does not exist -> File not there
            if (idx in [0,2]): # if one of the widgetUI files not here
                print(f"No file named {jsonName} found in blw dat folder.")
                print(f"\nSuggested Troubleshoot:\n* Copy {jsonName} from the gamefiles (\\Steam\\steamapps\\common\\AoE2DE\\widgetui) in the blw dat folder")
            else:
                print(f"No file named {jsonName} found in blw dat folder.")
                print(f"\nSuggested Troubleshoot:\n* Copy {jsonName} from the gamefiles (\\Steam\\steamapps\\common\\AoE2DE\\resources\\_common\\dat) in the blw dat folder")
            quit()
    print("Found all JSON Files needed")
    logging.info("Success: Found all JSON Files needed")            


def make_ingame_modifications():
    print("Loading base data...")
    cache_file = None
    cache_file, dfBase = load_cache(Path("datfiles/base_game.dat"))
    if not dfBase:
        print("Parsing...")
        dfBase = DatFile.parse("datfiles/base_game.dat")
        write_cache(dfBase, cache_file)

    # print(json.dumps(dataclasses.asdict(dfBase.civs[0].units[280]), indent=2)) Here you can show all data of a unit, very useful to reverse engineer
    # print(json.dumps(dataclasses.asdict(dfBase.graphics[1099]), indent=2)) # needed for Yodit Death Scream graphic
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
    change_existing_civs.run_change_existing_civs (dfBase)
    change_existing_techs.run_change_existing_techs (dfBase)
    change_existing_tech_tree.run_change_tech_tree (dfBase)
    
    print("Modifications completed")

    # You can save it as whatever filename.dat you want, but when it is in a mod you will need it to be named empires2_x2_p1.dat
    print("Saving file...")
    if (not storage.lightmode):
        dfBase.save("datfiles/empires2_x2_p1.dat")
    print("Success: .dat file changed")

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


def creating_moving_files():
    for file in storage.constantsPath.iterdir(): # cycle through the constant folder in blw dat/constants
        if file.suffix == ".dds":
            for techidx, techname in enumerate(storage.techStrings, 1):
                if file.name.startswith("_"+techname[:5].lower()):
                    filenamestring = str(storage.si + techidx) + file.name
                    newFile = storage.techIconFolder / filenamestring
                    shutil.copy(file, newFile)
                    # How to copy (not moving), rename and overwrite (in case already exists)
        if file.suffix == ".wem":
            newFile = storage.soundFolder / file.name
            shutil.copy(file, newFile)
        if file.suffix == ".png":
            if file.stem.startswith("thumbnail Da"):
                newFile = storage.dataModFolder / "thumbnail.png"
                shutil.copy(file, newFile)
            if file.stem.startswith("thumbnail UI"):
                newFile = storage.UIModFolder / "thumbnail.png"
                shutil.copy(file, newFile)

if __name__ == "__main__":
    main()

def dat_to_json():
    parser = argparse.ArgumentParser(
        prog='dat-to-json',
        description='Read a genie engine dat file and print the json representation to stdout',
    )
    parser.add_argument('filename', type=Path, help='The dat file to read')
    args = parser.parse_args()

    dat_file = DatFile.parse(args.filename)
    print(json.dumps(dataclasses.asdict(dat_file), indent=2))
