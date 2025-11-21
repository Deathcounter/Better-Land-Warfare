from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *

import copy
import logging
from mods import storage

logging.getLogger(__name__)

NAME = "add_projectiles"

def run_add_projectiles(df: DatFile):
    add_thrower_projectiles(df)

def add_thrower_projectiles (df: DatFile):
    # adds dart projectile, changing the graphics from knife to arambai dart
    dart_thrower_projectile = copy.deepcopy (df.civs[0].units[1055]) # copy the knife projectiles from gbeto
    dart_thrower_projectile_id = len(df.civs[0].units)
    storage.ThrowerProjectileIDs.append(dart_thrower_projectile_id)
    dart_thrower_projectile.standing_graphic = [10251, -1]
    dart_thrower_projectile.dead_fish.walking_graphic = 10251
    dart_thrower_projectile.speed = 6
    dart_thrower_projectile.name = "Projectile DartThrower"

    # adds knife projectile, changing standind graphics not needed, already a knife
    knife_thrower_projectile = copy.deepcopy (df.civs[0].units[1055])
    knife_thrower_projectile_id = len(df.civs[0].units) + 1
    storage.ThrowerProjectileIDs.append(knife_thrower_projectile_id)
    knife_thrower_projectile.speed = 6
    knife_thrower_projectile.name = "Projectile KnifeThrower"


    hatchet_thrower_projectile = copy.deepcopy (df.civs[0].units[1055])
    hatchet_thrower_projectile_id = len(df.civs[0].units) + 2
    storage.ThrowerProjectileIDs.append(hatchet_thrower_projectile_id)
    hatchet_thrower_projectile.standing_graphic = [3380, -1]
    hatchet_thrower_projectile.dead_fish.walking_graphic = 3380
    hatchet_thrower_projectile.speed = 6
    hatchet_thrower_projectile.name = "Projectile HatchetThrower"

    ninja_projectile = copy.deepcopy (df.civs[0].units[1055])
    ninja_projectile_id = len(df.civs[0].units) + 3
    storage.ThrowerProjectileIDs.append(ninja_projectile_id)
    ninja_projectile.speed = 6
    ninja_projectile.name = "Projectile Shurikan" # currently still just a knife

    for civ in df.civs:
        civ.units.append(dart_thrower_projectile)
        civ.units.append(knife_thrower_projectile)
        civ.units.append(hatchet_thrower_projectile)
        civ.units.append(ninja_projectile)

    logging.info(f"SUCCESS: Throwing Projectiles added")    