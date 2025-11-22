#! /usr/bin/env python3


import argparse
import hashlib
import pickle
from pathlib import Path

from genieutils.datfile import DatFile

from mods import add_projectiles
from mods import add_units
from mods import add_effects
from mods import add_technologies
from mods import change_existing_units
from mods import change_existing_techs
from mods import change_existing_civs
from mods import change_existing_tech_tree


# Overall, genieutils works by loading a .dat file into memory and constructing a DatFile object
# This is done with the DatFile.parse method
# Once the object has been parsed, you make the modifications you want to the object
# Once this is complete, you can write the new object to a new file using the DatFile.save method
def main():
    print("Loading base data...")
    cache_file = None
    cache_file, dfBase = load_cache(Path("datfiles/base_game.dat"))
    if not dfBase:
        print("Parsing...")
        dfBase = DatFile.parse("datfiles/base_game.dat")
        write_cache(dfBase, cache_file)

    print("Base data loaded")
    print("Applying modifications")
  
    add_projectiles.run_add_projectiles (dfBase)
    add_units.run_add_units(dfBase)
    add_effects.run_add_effects (dfBase)
    add_technologies.run_add_technologies (dfBase)
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
