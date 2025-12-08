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
    give_scorpion_lancer_damage (df)
    give_steppelancers_lancer_class (df)
    give_firelancers_lancer_class (df)
    move_condo_trainbutton (df)
    move_genitour_trainbutton (df)
    buff_iron_pagoda (df)
    nerf_rattan_archers (df)
    if (not storage.lightmode):
        add_armored_unit_class (df)

    logging.info("Successfully changed all existing units")

def give_scorpion_lancer_damage (df: DatFile):
    lancer_damage: AttackOrArmor = AttackOrArmor (91,1) #add lancer damage of scorpion
    heavy_lancer_damage: AttackOrArmor = AttackOrArmor (91,2) #add lancer damage of heavy scorpion
    for civ in df.civs:
        civ.units[279].type_50.attacks.append(lancer_damage)
        civ.units[542].type_50.attacks.append(heavy_lancer_damage)
    logging.debug("Gave Scorpions bonus damage vs lancers")

def give_steppelancers_lancer_class (df: DatFile):
    lancer_class: AttackOrArmor = AttackOrArmor (91,0) #add lancer armor to Steppe Lancer
    for civ in df.civs:
        civ.units[1370].type_50.armours.append(lancer_class)
        civ.units[1372].type_50.armours.append(lancer_class)
    logging.debug("Gave Steppelancer-line the lancer class")

def give_firelancers_lancer_class (df: DatFile):
    lancer_class: AttackOrArmor = AttackOrArmor (91,0) #add lancer armor to Fire Lancer
    for civ in df.civs:
        civ.units[1901].type_50.armours.append(lancer_class)
        civ.units[1903].type_50.armours.append(lancer_class)
    logging.debug("Gave Firelancer-line the lancer class")

def move_condo_trainbutton (df: DatFile):
    for civ in df.civs:
        civ.units[882].creatable.train_locations[0].button_id = 14 # moves Condottiero train button to 14
    logging.debug("Moved Condo to Button 14")


def move_genitour_trainbutton (df: DatFile):
    for civ in df.civs:
        civ.units[1010].creatable.train_locations[0].button_id = 12 # moves Genitour train button to 12
        civ.units[1012].creatable.train_locations[0].button_id = 12 # moves Elite-Genitour train button to 12
    logging.debug("Moved Genitour to Button 12")

def buff_iron_pagoda (df: DatFile):
    # actually its a nerf, but since I change Jurchens Civ bonus, it's a buff. 2.15 -> 1.72 originally. Now 1.72 -> 1.85
    for civ in df.civs:
        civ.units[1908].type_50.reload_time = 1.85
        civ.units[1908].type_50.displayed_reload_time = 1.85
        civ.units[1910].type_50.reload_time = 1.85
        civ.units[1910].type_50.displayed_reload_time = 1.85
    logging.debug("Buffed Iron Pagoda Attack Speed")

def nerf_rattan_archers (df: DatFile):
    # actually its a buff, since I change Vietnamese Civ bonus. 40/45 HP originally, now 35/40 HP + 25% -> 44/50 HP
    for civ in df.civs:
        civ.units[1129].hit_points = 35
        civ.units[1131].hit_points = 40
    logging.debug("Nerfed Rattan Archer HP")

def add_armored_unit_class (df: DatFile):
    # Give all units whose base unit has more than 3 combined armor the armored unit class (= armor class) lancer have bonus against
    unitList: list[Unit] = []
    unitList = helpers.find_units_with_3_combined_armor(df)
    removeUnits = [6, 7, 1155, 1010, 1012] # Excluding Skirms
    for civ in df.civs:
        for unit in unitList:
            if (AttackOrArmor(90,0) not in civ.units[unit.id].type_50.armours):
                if (unit.id not in removeUnits):
                    civ.units[unit.id].type_50.armours.append(AttackOrArmor(90,0))
                    logging.debug(f"Appended Armored Unit class to {civ.units[unit.id].name}")
    logging.info("Added Armored Unit Armor Class")
            