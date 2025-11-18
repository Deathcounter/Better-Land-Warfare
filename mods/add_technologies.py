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
    logging.debug (f"Added Billman (make avail) tech at ID {storage.billmanAvailTechID}")

    storage.lancerAvailTechID = len(df.techs)
    lancer_avail_tech = helpers.create_empty_tech()
    lancer_avail_tech.repeatable = 1
    lancer_avail_tech.effect_id = storage.lancerAvailID
    lancer_avail_tech.required_techs = (102, -1, -1, -1, -1, -1) 
    lancer_avail_tech.required_tech_count = 1
    lancer_avail_tech.name = "Lancer (make avail)"
    df.techs.append(lancer_avail_tech)
    logging.debug (f"Added Lancer (make avail) tech at ID {storage.lancerAvailTechID}")

    storage.dartthrowerAvailTechID = len(df.techs)
    dartthrower_avail_tech = helpers.create_empty_tech()
    dartthrower_avail_tech.repeatable = 1
    dartthrower_avail_tech.effect_id = storage.dartthrowerAvailID
    dartthrower_avail_tech.required_techs = (101, -1, -1, -1, -1, -1) 
    dartthrower_avail_tech.required_tech_count = 1
    dartthrower_avail_tech.name = "Dartthrower (make avail)"
    df.techs.append(dartthrower_avail_tech)
    logging.debug (f"Added Dart Thrower (make avail) tech at ID {storage.dartthrowerAvailTechID}")

    storage.flamethrowerAvailTechID = len(df.techs)
    flamethrower_avail_tech = helpers.create_empty_tech()
    flamethrower_avail_tech.repeatable = 1
    flamethrower_avail_tech.effect_id = storage.flamethrowerAvailID
    flamethrower_avail_tech.required_techs = (103, 47, 285, -1, -1, -1) 
    flamethrower_avail_tech.required_tech_count = 2
    flamethrower_avail_tech.name = "Flamethrower (make avail)"
    df.techs.append(flamethrower_avail_tech)
    logging.debug (f"Added Flamethrower (make avail) tech at ID {storage.flamethrowerAvailTechID}")


def unit_upgrades_t (df: DatFile):

    storage.billmanUpgradeTechs.append(len(df.techs))
    scytheman_upgrade_tech = helpers.create_empty_tech()
    scytheman_upgrade_tech.repeatable = 1
    scytheman_upgrade_tech.icon_id = 999 #need to fix later
    scytheman_upgrade_tech.effect_id = storage.billmanUpgradeIDs[0]
    scytheman_upgrade_tech.required_techs = (102, 950, -1, -1, -1, -1)
    scytheman_upgrade_tech.required_tech_count = 1
    scytheman_upgrade_tech.name = "Scytheman"
    scytheman_upgrade_tech.research_locations[0] = ResearchLocation(12, 200, 8, 18260) # 12 in Barracks, 85 seconds ResearchtTime, Button 8 und Hotkey ID of Legionary
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 250, 1) # 0 food storage, 250 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 175, 1) # 3 gold storage, 175 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) #  4 population headroom, 1 cost, 0 deduct no
    scytheman_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_scytheman_tech = 32330
    scytheman_upgrade_tech.language_dll_name = string_start_scytheman_tech
    scytheman_upgrade_tech.language_dll_description = string_start_scytheman_tech + 1000
    scytheman_upgrade_tech.language_dll_help = string_start_scytheman_tech + 100000
    df.techs.append(scytheman_upgrade_tech)
    logging.debug (f"Added Scytheman Upgrade tech at ID {storage.billmanUpgradeTechs[0]}")




    storage.billmanUpgradeTechs.append(len(df.techs))
    flailWarrior_upgrade_tech = helpers.create_empty_tech()
    flailWarrior_upgrade_tech.repeatable = 1
    flailWarrior_upgrade_tech.icon_id = 999 #need to fix later
    flailWarrior_upgrade_tech.effect_id = storage.billmanUpgradeIDs[0]
    flailWarrior_upgrade_tech.required_techs = (103, 950, -1, -1, -1, -1)
    flailWarrior_upgrade_tech.required_tech_count = 1
    flailWarrior_upgrade_tech.name = "Flail Warrior"
    flailWarrior_upgrade_tech.research_locations[0] = ResearchLocation(12, 200, 8, 18260) # 12 in Barracks, 200 seconds ResearchtTime, Button 8 und Hotkey ID of Legionary
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 775, 1) # 0 food storage, 775 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 450, 1) # 3 gold storage, 450 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) #  4 population headroom, 1 cost, 0 deduct no
    flailWarrior_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_scytheman_tech = 32331
    flailWarrior_upgrade_tech.language_dll_name = string_start_scytheman_tech
    flailWarrior_upgrade_tech.language_dll_description = string_start_scytheman_tech + 1000
    flailWarrior_upgrade_tech.language_dll_help = string_start_scytheman_tech + 100000
    df.techs.append(flailWarrior_upgrade_tech)
    logging.debug (f"Added Flail Warrior Upgrade tech at ID {storage.billmanUpgradeTechs[1]}")



    storage.lancerUpgradeTech = len(df.techs)
    heavyLancer_upgrade_tech = helpers.create_empty_tech()
    heavyLancer_upgrade_tech.repeatable = 1
    heavyLancer_upgrade_tech.icon_id = 999 #need to fix later
    heavyLancer_upgrade_tech.effect_id = storage.lancerUpgradeID
    heavyLancer_upgrade_tech.required_techs = (103, -1, -1, -1, -1, -1)
    heavyLancer_upgrade_tech.required_tech_count = 1
    heavyLancer_upgrade_tech.name = "Heavy Lancer"
    heavyLancer_upgrade_tech.research_locations[0] = ResearchLocation(101, 115, 13, 18260) # 101 in Stable, 115 seconds ResearchtTime, Button 13 und Hotkey ID of Savar
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 1075, 1) # 0 food storage, 975 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 450, 1) # 3 gold storage, 550 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) #  4 population headroom, 1 cost, 0 deduct no
    heavyLancer_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_scytheman_tech = 32332
    heavyLancer_upgrade_tech.language_dll_name = string_start_scytheman_tech
    heavyLancer_upgrade_tech.language_dll_description = string_start_scytheman_tech + 1000
    heavyLancer_upgrade_tech.language_dll_help = string_start_scytheman_tech + 100000
    df.techs.append (heavyLancer_upgrade_tech)
    logging.debug (f"Added Heavy Lancer Upgrade tech at ID {storage.lancerUpgradeTech}")
    
