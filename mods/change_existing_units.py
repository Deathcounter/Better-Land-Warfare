from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *
import logging


logging.getLogger(__name__)
NAME = "change_existing_units"

def run_change_existing_units(df: DatFile):
    give_scorpion_lancer_damage (df)
    move_condo_trainbutton (df)
    give_steppelancers_lancer_class (df)


def give_scorpion_lancer_damage (df: DatFile):
    lancer_damage: AttackOrArmor = AttackOrArmor (51,3) #add lancer damage of scorpion
    heavy_lancer_damage: AttackOrArmor = AttackOrArmor (51,5) #add lancer damage of heavy scorpion
    for civ in df.civs:
        civ.units[279].type_50.attacks.append(lancer_damage)
        civ.units[542].type_50.attacks.append(heavy_lancer_damage)
    logging.info("Gave Scorpions bonus damage vs lancers")

def move_condo_trainbutton (df: DatFile):
    for civ in df.civs:
        civ.units[882].creatable.train_locations[0].button_id = 14 # moves Condottiero train button to 14
    logging.info("Moved Condo to Button 14")

def give_steppelancers_lancer_class (df: DatFile):
    lancer_class: AttackOrArmor = AttackOrArmor (51,0) #add lancer armor to Steppe Lancer
    for civ in df.civs:
        civ.units[1370].type_50.armours.append(lancer_class)
        civ.units[1372].type_50.armours.append(lancer_class)
    logging.info("Gave Steppelancer-line the lancer class")

def buff_iron_pagoda (df: DatFile):
    # actually its a nerf, but since I change Jurchens Civ bonus, it's a buff. 2.28 -> 1.9 originally. Now 1.9 -> 2.0
    for civ in df.civs:
        civ.units[1908].type_50.reload_time = 2
        civ.units[1908].type_50.displayed_reload_time = 2