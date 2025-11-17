from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, ResearchLocation, Tech
from genieutils.unit import *
import logging

from mods import helpers
from mods import storage

logging.getLogger(__name__)
NAME = "helpers"

def run_add_technologies(df: DatFile):
    make_avail_techs (df)
    unit_upgrades_t (df)
    # thrower_upgrades_t (df)


def make_avail_techs (df: DatFile):
    storage.billmanAvailTechID = len(df.techs)
    billman_avail_tech = helpers.create_empty_tech()
    billman_avail_tech.repeatable = 1
    billman_avail_tech.effect_id = storage.billmanAvailID
    billman_avail_tech.required_techs = (101, -1, -1, -1, -1, -1) 
    billman_avail_tech.required_tech_count = 1
    billman_avail_tech.name = "Billman (make avail)"
    df.techs.append(billman_avail_tech)

    storage.lancerAvailTechID = len(df.techs)
    lancer_avail_tech = helpers.create_empty_tech()
    lancer_avail_tech.repeatable = 1
    lancer_avail_tech.effect_id = storage.lancerAvailID
    lancer_avail_tech.required_techs = (102, -1, -1, -1, -1, -1) 
    lancer_avail_tech.required_tech_count = 1
    lancer_avail_tech.name = "Lancer (make avail)"
    df.techs.append(lancer_avail_tech)

    storage.dartthrowerAvailTechID = len(df.techs)
    dartthrower_avail_tech = helpers.create_empty_tech()
    dartthrower_avail_tech.repeatable = 1
    dartthrower_avail_tech.effect_id = storage.dartthrowerAvailID
    dartthrower_avail_tech.required_techs = (101, -1, -1, -1, -1, -1) 
    dartthrower_avail_tech.required_tech_count = 1
    dartthrower_avail_tech.name = "Dartthrower (make avail)"
    df.techs.append(dartthrower_avail_tech)

    storage.flamethrowerAvailTechID = len(df.techs)
    flamethrower_avail_tech = helpers.create_empty_tech()
    flamethrower_avail_tech.repeatable = 1
    flamethrower_avail_tech.effect_id = storage.flamethrowerAvailID
    flamethrower_avail_tech.required_techs = (103, 47, 285, -1, -1, -1) 
    flamethrower_avail_tech.required_tech_count = 2
    flamethrower_avail_tech.name = "Flamethrower (make avail)"
    df.techs.append(flamethrower_avail_tech)


def unit_upgrades_t (df: DatFile):
    storage.billmanUpgradeTechs.append(len(df.techs))
    billman_upgrade_tech = helpers.create_empty_tech()
    billman_upgrade_tech.repeatable = 1
    billman_upgrade_tech.icon_id = 999 #need to fix later
    billman_upgrade_tech.effect_id = storage.billmanUpgradeIDs[0]
    billman_upgrade_tech.required_techs = (102, 950, -1, -1, -1, -1)
    billman_upgrade_tech.required_tech_count = 1
    billman_upgrade_tech.name = "Scytheman"
    billman_upgrade_tech.research_locations.append([ResearchLocation(12, 85, 8, 18260)]) # 12 in Barracks, 85 seconds ResearchtTime, Button 8 und Hotkey ID of Legionary
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 250, 1) # 0 food storage, 250 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 175, 1) # 3 gold storage,175 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) #  4 population headroom, 1 cost, 0 deduct no
    billman_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_scytheman_tech = 32330
    billman_upgrade_tech.language_dll_name = string_start_scytheman_tech
    billman_upgrade_tech.language_dll_description = string_start_scytheman_tech + 1000
    billman_upgrade_tech.language_dll_help = string_start_scytheman_tech + 21000