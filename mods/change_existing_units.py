from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *

from mods import helpers
from mods import storage

import logging
import time


logging.getLogger(__name__)

NAME = "change_existing_units"

def run_change_existing_units (df: DatFile):
    if (storage.lightmode):
        add_armored_unit_class (df)

    give_scorpion_lancer_damage (df)
    move_condo_trainbutton (df)
    give_steppelancers_lancer_class (df)
    buff_iron_pagoda (df)
    nerf_rattan_archers (df)

    logging.info("Successfully changed all existing units")

def add_armored_unit_class (df: DatFile):
    # Give all units whose base unit has more than 3 combined armor the armored unit class (= armor class) lancer have bonus against
    unitList: list[Unit] = []
    unitList = helpers.find_units_with_3_combined_armor(df)
    for civ in df.civs:
        for unit in unitList:
            if (AttackOrArmor (50,0) not in civ.units[unit.id].type_50.armours):
                civ.units[unit.id].type_50.armours.append(AttackOrArmor (50,0))
                print(f"Appended Armored Unit class to {civ.units[unit.id].name}")
    logging.info("Added Armored Unit Armor Class")
            



def give_scorpion_lancer_damage (df: DatFile):
    lancer_damage: AttackOrArmor = AttackOrArmor (51,3) #add lancer damage of scorpion
    heavy_lancer_damage: AttackOrArmor = AttackOrArmor (51,5) #add lancer damage of heavy scorpion
    for civ in df.civs:
        civ.units[279].type_50.attacks.append(lancer_damage)
        civ.units[542].type_50.attacks.append(heavy_lancer_damage)
    logging.debug("Gave Scorpions bonus damage vs lancers")

def move_condo_trainbutton (df: DatFile):
    for civ in df.civs:
        civ.units[882].creatable.train_locations[0].button_id = 14 # moves Condottiero train button to 14
    logging.debug("Moved Condo to Button 14")

def give_steppelancers_lancer_class (df: DatFile):
    lancer_class: AttackOrArmor = AttackOrArmor (51,0) #add lancer armor to Steppe Lancer
    for civ in df.civs:
        civ.units[1370].type_50.armours.append(lancer_class)
        civ.units[1372].type_50.armours.append(lancer_class)
    logging.debug("Gave Steppelancer-line the lancer class")

def buff_iron_pagoda (df: DatFile):
    # actually its a nerf, but since I change Jurchens Civ bonus, it's a buff. 2.28 -> 1.9 originally. Now 1.9 -> 2.0
    for civ in df.civs:
        civ.units[1908].type_50.reload_time = 2
        civ.units[1908].type_50.displayed_reload_time = 2
    logging.debug("Buffed Iron Pagoda Attack Speed")

def nerf_rattan_archers (df: DatFile):
    # actually its a buff, since I change Vietnamese Civ bonus. 40/45 HP originally, now 35/40 HP + 25% -> 44/50 HP
    for civ in df.civs:
        civ.units[1129].hit_points = 35
        civ.units[1131].hit_points = 40
    logging.debug("Nerfed Rattan Archer HP")

