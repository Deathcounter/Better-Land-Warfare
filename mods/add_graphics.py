import copy
import logging


from genieutils.datfile import DatFile
from genieutils.graphic import Graphic
from genieutils.civ import Civ
from genieutils.tech import Tech, ResearchResourceCost
from genieutils.unit import Unit, AttackOrArmor, Task, ResourceCost, ResourceStorage, Type50, Bird, Creatable, Building, TrainLocation

from mods import helpers
from mods import storage


logging.getLogger(__name__)

NAME = "add_graphics"

def run_add_graphics (df: DatFile):
    add_projectile_graphics (df)
    add_silent_norse_warrior_attack (df)
    add_silent_ninja_attack (df)
    change_yodit_death_scream (df)
    logging.info("Added all Graphics")


def add_projectile_graphics (df: DatFile):
    storage.dartProjectileGraphicID = len(df.graphics)
    projectile_dart: Graphic = copy.deepcopy(df.graphics[10251])
    projectile_dart.sound_id = storage.dartSoundID
    df.graphics.append(projectile_dart)
    logging.info("Added Dart Projectile Graphics")


def add_silent_norse_warrior_attack (df: DatFile):
    storage.silentNorseWarriorID = len(df.graphics)
    silent_norse_warrior_attack: Graphic = copy.deepcopy(df.graphics[7626]) # Norse Warrior Attack Graphic
    silent_norse_warrior_attack.angle_sounds.clear()
    silent_norse_warrior_attack.sound_id = -1 # just in case
    silent_norse_warrior_attack.angle_count = 16
    silent_norse_warrior_attack.angle_sounds_used = 0
    df.graphics.append(silent_norse_warrior_attack)
    logging.info("Added Silent Norse Warrior")


def add_silent_ninja_attack (df: DatFile):
    storage.silentNinjaID = len(df.graphics)
    silent_norse_warrior_attack: Graphic = copy.deepcopy(df.graphics[1031]) # Ninja Attack A is the correct one that is more of a throw animation.
    silent_norse_warrior_attack.angle_sounds.clear()
    silent_norse_warrior_attack.sound_id = -1 # just in case
    silent_norse_warrior_attack.angle_count = 16
    silent_norse_warrior_attack.angle_sounds_used = 0
    df.graphics.append(silent_norse_warrior_attack)
    logging.info("Added Silent Ninja")


def change_yodit_death_scream (df: DatFile):
    storage.yoditDeathScreamID = len(df.graphics)
    yodit_death_scream: Graphic = copy.deepcopy(df.graphics[3901]) # Yodit Death Graphic
    yodit_death_scream.sound_id = 294 # generic man death scream
    yodit_death_scream.angle_count = 16
    df.graphics.append(yodit_death_scream)
    logging.info("Added Manly Yodit Death Scream")
