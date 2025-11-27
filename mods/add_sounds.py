import copy
import logging


from genieutils.datfile import DatFile
from genieutils.graphic import Graphic
from genieutils.sound import Sound, SoundItem
from genieutils.tech import Tech, ResearchResourceCost
from genieutils.unit import Unit, AttackOrArmor, Task, ResourceCost, ResourceStorage, Type50, Bird, Creatable, Building, TrainLocation

from mods import helpers
from mods import storage


logging.getLogger(__name__)

NAME = "add_sounds"

def run_add_sounds (df: DatFile):
    add_dart_projectile_sound (df)
    logging.info("Added all Sounds")

def add_dart_projectile_sound (df: DatFile):
    storage.dartSoundID = len(df.sounds)
    sound_dart: Sound = copy.deepcopy(df.sounds[0]) # hopefully they never change the first Sound
    sound_list: list[SoundItem] = []

    for idx in range(4):
        sound_list.append(SoundItem("blw_dartThrower"+str(idx+1), -1, 25, -1, -1))

    sound_dart.items = sound_list
    df.sounds.append(sound_dart) # Error as seen below
    logging.debug ("Dart Projectile sound added")
    