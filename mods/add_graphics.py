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
    add_Billman_Maceman_attack (df)
    add_Scytheman_Sparabara_attack (df)
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


def add_Billman_Maceman_attack (df: DatFile):
    storage.billmanAttackID = len(df.graphics)
    billman_attacksound: Graphic = copy.deepcopy(df.graphics[16797]) # Billman attack Graphic (Hills Tribesman Attack)
    billman_attacksound.angle_sounds.clear()
    billman_attacksound.angle_count = 16
    billman_attacksound.sound_id = -1
    billman_attacksound.wwise_sound_id = 0 #-1768200429 # reverse engineered (search for reverse engineered to understand how) 
    billman_attacksound.angle_sounds = copy.deepcopy(df.graphics[15169].angle_sounds) # wwise sound id not needed because I use angle sounds, so I can use frame delay (sound delay)
    for angle_sound in billman_attacksound.angle_sounds:
        angle_sound.frame_num = 10
    df.graphics.append(billman_attacksound)
    
    storage.billmanAttackID2 = len(df.graphics)
    billman_attacksound_2: Graphic = copy.deepcopy(df.graphics[16802]) # Billman attack Graphic (Hills Tribesman Attack B)
    billman_attacksound_2.angle_sounds.clear()
    billman_attacksound_2.angle_count = 16
    billman_attacksound_2.angle_sounds_used = 1
    billman_attacksound_2.sound_id = -1
    billman_attacksound_2.wwise_sound_id = 0
    billman_attacksound_2.angle_sounds = copy.deepcopy(df.graphics[15169].angle_sounds)
    for angle_sound in billman_attacksound_2.angle_sounds:
        angle_sound.frame_num = 10
    df.graphics.append(billman_attacksound_2)


def add_Scytheman_Sparabara_attack (df: DatFile):
    storage.scythemanAttackID = len(df.graphics)
    scytheman_attacksound: Graphic = copy.deepcopy(df.graphics[16786]) # Scytheman attack Graphic (Indian Tribesman Attack)
    scytheman_attacksound.angle_sounds.clear()
    scytheman_attacksound.angle_count = 16
    scytheman_attacksound.angle_sounds_used = 0
    scytheman_attacksound.sound_id = 713
    scytheman_attacksound.wwise_sound_id = -1782155183
    df.graphics.append(scytheman_attacksound)


def change_yodit_death_scream (df: DatFile):
    storage.yoditDeathScreamID = len(df.graphics)
    yodit_death_scream: Graphic = copy.deepcopy(df.graphics[3901]) # Yodit Death Graphic
    yodit_death_scream.sound_id = 294 # generic man death scream
    yodit_death_scream.wwise_sound_id = -1501358160 # reversed engineered by getting the information from Militia Death (1099) Graphic
    yodit_death_scream.angle_count = 16
    df.graphics.append(yodit_death_scream)
    logging.info("Added Manly Yodit Death Scream")

def heavy_lancer_lancer_attack (df: DatFile):
    storage.heavylancerlancingID = len(df.graphics)
    heavy_lancer_attack: Graphic = copy.deepcopy(df.graphics[15138]) # Imperial Cavalry (Attack)
    heavy_lancer_attack.sound_id = 761 # companion cavalry attack
    heavy_lancer_attack.wwise_sound_id = -633533558 # reversed engineered by getting the information from Militia Death (1099) Graphic
    heavy_lancer_attack.angle_count = 16
    df.graphics.append(heavy_lancer_attack)
    logging.info("Heavy Lancer does lancing sound")