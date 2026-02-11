from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, ResearchLocation, Tech
from genieutils.unit import *
import logging
import copy

from mods import helpers
from mods import storage

logging.getLogger(__name__)

NAME = "add_technologies"

def run_add_technologies (df: DatFile):
    make_avail_techs (df)
    armenian_barrack_req (df)
    unit_upgrades_t (df)
    thrower_upgrades_t (df)
    shield_boss_t (df)
    billman_auto_upgrade (df)

def make_avail_techs (df: DatFile):
    # @make available techs
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
    flamethrower_avail_tech.required_techs = (103, -1, -1, -1, -1, -1) 
    flamethrower_avail_tech.required_tech_count = 1
    flamethrower_avail_tech.name = "Flamethrower (make avail)"
    df.techs.append(flamethrower_avail_tech)
    logging.debug (f"Added Flamethrower (make avail) tech at ID {storage.flamethrowerAvailTechID}")


def armenian_barrack_req (df: DatFile):
    # @Armenian requirements
    #make extra requirement techs for Armenians
    #since Armenians have Barrack Upgrades available one age earlier, they need extra trickery to be enabled earlier compared to any other civ.
    #doing what other "requirement" civs do in A.G.E, you will understand how they work. You are smart after all
    storage.armenian_scyteman_req_ID = len(df.techs)
    armenian_scyteman_req_tech = helpers.create_empty_tech()
    armenian_scyteman_req_tech.repeatable = 1
    armenian_scyteman_req_tech.required_techs = (101, storage.billmanAvailTechID, -1, -1, -1, -1) 
    armenian_scyteman_req_tech.required_tech_count = 2
    armenian_scyteman_req_tech.name = "Scytheman requirement"
    armenian_scyteman_req_tech.civ = 44 # Armenians
    df.techs.append(armenian_scyteman_req_tech)
    logging.debug
    
    storage.armenian_flailWarrior_req_ID = len(df.techs)
    armenian_flailWarrior_req_tech = helpers.create_empty_tech()
    armenian_flailWarrior_req_tech.repeatable = 1
    armenian_flailWarrior_req_tech.required_techs = (102, -1, -1, -1, -1, -1) # this should actually read 102 = Castle Age and in Slot 2 contain the Scytheman Upgrade, which doesnt exist yet ***
    armenian_flailWarrior_req_tech.required_tech_count = 2
    armenian_flailWarrior_req_tech.name = "Flail Warrior requirement"
    armenian_flailWarrior_req_tech.civ = 44 # Armenians
    df.techs.append(armenian_flailWarrior_req_tech)

    storage.armenian_shieldBoss_req_ID = len(df.techs)
    armenian_shieldBoss_req_tech = helpers.create_empty_tech()
    armenian_shieldBoss_req_tech.repeatable = 1
    armenian_shieldBoss_req_tech.required_techs = (101, 875, -1, -1, -1, -1) # Feudal Age and Gambesons
    armenian_shieldBoss_req_tech.required_tech_count = 2
    armenian_shieldBoss_req_tech.name = "Shield Boss requirement"
    armenian_shieldBoss_req_tech.civ = 44 # Armenians
    df.techs.append(armenian_shieldBoss_req_tech)


def unit_upgrades_t (df: DatFile):
    # @Unit Upgrade Techs
    storage.billmanUpgradeTechs.append(len(df.techs))
    scytheman_upgrade_tech = helpers.create_empty_tech()
    scytheman_upgrade_tech.repeatable = 1
    scytheman_upgrade_tech.icon_id = storage.si + 1
    scytheman_upgrade_tech.effect_id = storage.billmanUpgradeIDs[0]
    scytheman_upgrade_tech.required_techs = (102, storage.billmanAvailTechID, storage.armenian_scyteman_req_ID, -1, -1, -1)
    scytheman_upgrade_tech.required_tech_count = 2
    scytheman_upgrade_tech.name = "Scytheman"
    storage.billmanUpgradeNames.append(scytheman_upgrade_tech.name)
    scytheman_upgrade_tech.research_locations[0] = ResearchLocation (12, 75, 8, 418008) # 12 in Barracks, 80 seconds ResearchtTime, Button 8 and Hotkey ID (Incendiary Ship)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 185, 1) # 0 food storage, 185 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 135, 1) # 3 gold storage, 135 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0)
    scytheman_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_scytheman_tech = 32330
    scytheman_upgrade_tech.language_dll_name = string_start_scytheman_tech
    scytheman_upgrade_tech.language_dll_description = string_start_scytheman_tech + 1000
    scytheman_upgrade_tech.language_dll_help = string_start_scytheman_tech + 100000
    scytheman_upgrade_tech.language_dll_tech_tree = string_start_scytheman_tech + 149000
    df.techs.append(scytheman_upgrade_tech)
    logging.debug (f"Added Scytheman Upgrade tech at ID {storage.billmanUpgradeTechs[0]}")


    #*** now that the Scytheman Upgrade exists, I can add it as a required tech to the Flail Warrior requirement tech
    #since tuples are immutable, I also have to convert them again into a temp list, change them, and then change them back
    armenianTech: Tech = df.techs[storage.armenian_flailWarrior_req_ID]
    temp = list(armenianTech.required_techs)
    temp[1] = storage.billmanUpgradeTechs[0] #changes the Flail Warrior Requirement from just Castle Age, to require Castle Age [0] and Scytheman Upgrade [1]
    armenianTech.required_techs = tuple(temp)


    storage.billmanUpgradeTechs.append(len(df.techs))
    flailWarrior_upgrade_tech = helpers.create_empty_tech()
    flailWarrior_upgrade_tech.repeatable = 1
    flailWarrior_upgrade_tech.icon_id = storage.si + 2
    flailWarrior_upgrade_tech.effect_id = storage.billmanUpgradeIDs[1]
    flailWarrior_upgrade_tech.required_techs = (103, storage.billmanUpgradeTechs[0], storage.armenian_flailWarrior_req_ID, -1, -1, -1)
    flailWarrior_upgrade_tech.required_tech_count = 2
    flailWarrior_upgrade_tech.name = "Flail Warrior"
    storage.billmanUpgradeNames.append(flailWarrior_upgrade_tech.name)
    flailWarrior_upgrade_tech.research_locations[0] = ResearchLocation (12, 175, 8, 418008) # 12 in Barracks, 180 seconds ResearchTime, Button 8 and Hotkey ID (Incendiary Ship)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 625, 1) # 0 food storage, 650 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 625, 1) # 3 gold storage, 625 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # nothing
    flailWarrior_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_flailWarrior_tech = 32331
    flailWarrior_upgrade_tech.language_dll_name = string_start_flailWarrior_tech
    flailWarrior_upgrade_tech.language_dll_description = string_start_flailWarrior_tech + 1000
    flailWarrior_upgrade_tech.language_dll_help = string_start_flailWarrior_tech + 100000
    flailWarrior_upgrade_tech.language_dll_tech_tree = string_start_flailWarrior_tech + 149000
    df.techs.append(flailWarrior_upgrade_tech)
    logging.debug (f"Added Flail Warrior Upgrade tech at ID {storage.billmanUpgradeTechs[1]}")



    storage.lancerUpgradeTech = len(df.techs)
    heavyLancer_upgrade_tech = helpers.create_empty_tech()
    heavyLancer_upgrade_tech.repeatable = 1
    heavyLancer_upgrade_tech.icon_id = storage.si + 3
    heavyLancer_upgrade_tech.effect_id = storage.lancerUpgradeID
    heavyLancer_upgrade_tech.required_techs = (103, -1, -1, -1, -1, -1)
    heavyLancer_upgrade_tech.required_tech_count = 1
    storage.lancerUpgradeName = heavyLancer_upgrade_tech.name = "Heavy Lancer"
    heavyLancer_upgrade_tech.research_locations[0] = ResearchLocation (101, 115, 13, 418006) # 101 in Stable, 115 seconds ResearchTime, Button 13 and Hotkey ID (Bireme)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 1075, 1) # 0 food storage, 975 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 450, 1) # 3 gold storage, 550 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # nothing, nothing, nothing
    heavyLancer_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_heavyLancer_tech = 32332
    heavyLancer_upgrade_tech.language_dll_name = string_start_heavyLancer_tech
    heavyLancer_upgrade_tech.language_dll_description = string_start_heavyLancer_tech + 1000
    heavyLancer_upgrade_tech.language_dll_help = string_start_heavyLancer_tech + 100000
    heavyLancer_upgrade_tech.language_dll_tech_tree = string_start_heavyLancer_tech + 149000
    df.techs.append (heavyLancer_upgrade_tech)
    logging.debug (f"Added Heavy Lancer Upgrade tech at ID {storage.lancerUpgradeTech}")
    

    storage.throwerUpgradeTechs.append(len(df.techs))
    knifeThrower_upgrade_tech = helpers.create_empty_tech()
    knifeThrower_upgrade_tech.repeatable = 1
    knifeThrower_upgrade_tech.icon_id = storage.si + 4
    knifeThrower_upgrade_tech.effect_id = storage.throwerUpgradeIDs[0]
    knifeThrower_upgrade_tech.required_techs = (102, -1, -1, -1, -1, -1)
    knifeThrower_upgrade_tech.required_tech_count = 1
    knifeThrower_upgrade_tech.name = "Knife Thrower"
    storage.throwerUpgradeNames.append(knifeThrower_upgrade_tech.name)
    knifeThrower_upgrade_tech.research_locations[0] = ResearchLocation (87, 25, 14, 418007) # 87 in Archery Range, 25 seconds ResearchTime, Button 14 and Hotkey ID (Elite Galley)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 120, 1) # 0 food storage, 120 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 225, 1) # 3 gold storage, 225 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # nothing, nothing², nothing³
    knifeThrower_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_knifeThrower_tech = 32333
    knifeThrower_upgrade_tech.language_dll_name = string_start_knifeThrower_tech
    knifeThrower_upgrade_tech.language_dll_description = string_start_knifeThrower_tech + 1000
    knifeThrower_upgrade_tech.language_dll_help = string_start_knifeThrower_tech + 100000
    knifeThrower_upgrade_tech.language_dll_tech_tree = string_start_knifeThrower_tech + 149000
    df.techs.append (knifeThrower_upgrade_tech)
    logging.debug (f"Added Knife Thrower Upgrade tech at ID {storage.throwerUpgradeTechs[0]}")


    storage.throwerUpgradeTechs.append(len(df.techs))
    hatchetThrower_upgrade_tech = helpers.create_empty_tech()
    hatchetThrower_upgrade_tech.repeatable = 1
    hatchetThrower_upgrade_tech.icon_id = storage.si + 5
    hatchetThrower_upgrade_tech.effect_id = storage.throwerUpgradeIDs[1]
    hatchetThrower_upgrade_tech.required_techs = (103, storage.throwerUpgradeTechs[0], -1, -1, -1, -1)
    hatchetThrower_upgrade_tech.required_tech_count = 2
    hatchetThrower_upgrade_tech.name = "Hatchet Thrower"
    storage.throwerUpgradeNames.append(hatchetThrower_upgrade_tech.name)
    hatchetThrower_upgrade_tech.research_locations[0] = ResearchLocation (87, 45, 14, 418007) # 87 in Archery Range, 45 seconds ResearchTime, Button 14 and Hotkey ID (Elite Galley)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 325, 1) # 0 food storage, 325 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 550, 1) # 3 gold storage, 550 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # nothing, yep, still nothing
    hatchetThrower_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_hatchetThrower_tech = 32334
    hatchetThrower_upgrade_tech.language_dll_name = string_start_hatchetThrower_tech
    hatchetThrower_upgrade_tech.language_dll_description = string_start_hatchetThrower_tech + 1000
    hatchetThrower_upgrade_tech.language_dll_help = string_start_hatchetThrower_tech + 100000
    hatchetThrower_upgrade_tech.language_dll_tech_tree = string_start_hatchetThrower_tech + 149000
    df.techs.append (hatchetThrower_upgrade_tech)
    logging.debug (f"Added Hatchet Thrower Upgrade tech at ID {storage.throwerUpgradeTechs[1]}")


    storage.throwerUpgradeTechs.append(len(df.techs))
    ninja_upgrade_tech = helpers.create_empty_tech()
    ninja_upgrade_tech.repeatable = 1
    ninja_upgrade_tech.icon_id = storage.si + 6
    ninja_upgrade_tech.effect_id = storage.throwerUpgradeIDs[2]
    ninja_upgrade_tech.required_techs = (103, storage.throwerUpgradeTechs[0], -1, -1, -1, -1)
    ninja_upgrade_tech.required_tech_count = 2
    ninja_upgrade_tech.name = "Ninja"
    storage.throwerUpgradeNames.append(ninja_upgrade_tech.name)
    ninja_upgrade_tech.civ = 5 # Japanese
    ninja_upgrade_tech.research_locations[0] = ResearchLocation (87, 55, 14, 418007) # 87 in Archery Range, 55 seconds ResearchTime, Button 14 and Hotkey ID (Elite Galley)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 475, 1) # 0 food storage, 475 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 425, 1) # 3 gold storage, 425 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # thanks for keep reading this, not many will
    ninja_upgrade_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_ninja_tech = 32335
    ninja_upgrade_tech.language_dll_name = string_start_ninja_tech
    ninja_upgrade_tech.language_dll_description = string_start_ninja_tech + 1000
    ninja_upgrade_tech.language_dll_help = string_start_ninja_tech + 100000
    ninja_upgrade_tech.language_dll_tech_tree = string_start_ninja_tech + 149000
    df.techs.append (ninja_upgrade_tech)
    logging.debug (f"Added Ninja Upgrade tech at ID {storage.throwerUpgradeTechs[2]}")



def thrower_upgrades_t (df: DatFile):
    # @Thrower Upgrade Techs
    storage.throwingTechniquesTechID = len(df.techs)
    throwing_techniques_tech = helpers.create_empty_tech()
    throwing_techniques_tech.repeatable = 1
    throwing_techniques_tech.icon_id = storage.si + 7
    throwing_techniques_tech.effect_id = storage.throwingTechniquesID
    throwing_techniques_tech.required_techs = (101, -1, -1, -1, -1, -1)
    throwing_techniques_tech.required_tech_count = 1
    storage.throwingTechniquesUpgradeName = throwing_techniques_tech.name = "Throwing Techniques"
    throwing_techniques_tech.research_locations[0] = ResearchLocation (87, 20, 10, 418005) # 87 in Archery Range, 20 seconds ResearchTime, Button 10 and Hotkey ID (Hypozomata)
    foodcost: ResearchResourceCost = ResearchResourceCost (0, 45, 1) # 0 food storage, 45 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 145, 1) # 3 gold storage, 145 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # you see, you might expect something here... WRONG
    throwing_techniques_tech.resource_costs = (foodcost, goldcost, nothing)

    storage.throwingTechniquesStringID = string_start_throwing_techniques_tech = 32336
    throwing_techniques_tech.language_dll_name = string_start_throwing_techniques_tech
    throwing_techniques_tech.language_dll_description = string_start_throwing_techniques_tech + 1000
    throwing_techniques_tech.language_dll_help = string_start_throwing_techniques_tech + 100000
    throwing_techniques_tech.language_dll_tech_tree = string_start_throwing_techniques_tech + 149000
    df.techs.append (throwing_techniques_tech)
    logging.debug (f"Added Throwing techniques tech at ID {storage.throwingTechniquesTechID}")


    storage.throwerBlacksmithTechIDs.append(len(df.techs))
    wooden_grip_tech = helpers.create_empty_tech()
    wooden_grip_tech.repeatable = 1
    wooden_grip_tech.icon_id = storage.si + 8
    wooden_grip_tech.effect_id = storage.throwerBlacksmithIDs[0]
    wooden_grip_tech.required_techs = (101, -1, -1, -1, -1, -1)
    wooden_grip_tech.required_tech_count = 1
    wooden_grip_tech.name = "Wooden Grip"
    storage.throwerBlacksmithUpgradeNames.append(wooden_grip_tech.name)
    wooden_grip_tech.research_locations[0] = ResearchLocation (103, 20, 8, 418010) # 103 in Blacksmith, 20 seconds ResearchTime, Button 8 and Hotkey ID (Onager Ship)
    foodcost: ResearchResourceCost = ResearchResourceCost (1, 120, 1) # 1 wood storage, 120 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 30, 1) # 3 gold storage, 30 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # still reading these huh? ... really dedicated
    wooden_grip_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_wooden_grip_tech = 32337
    storage.throwerBlacksmithStringIDs.append(string_start_wooden_grip_tech)
    wooden_grip_tech.language_dll_name = string_start_wooden_grip_tech
    wooden_grip_tech.language_dll_description = string_start_wooden_grip_tech + 1000
    wooden_grip_tech.language_dll_help = string_start_wooden_grip_tech + 100000
    wooden_grip_tech.language_dll_tech_tree = string_start_wooden_grip_tech + 149000
    df.techs.append (wooden_grip_tech)
    logging.debug (f"Added Wooden Grip tech at ID {storage.throwerBlacksmithTechIDs[0]}")



    storage.throwerBlacksmithTechIDs.append(len(df.techs))
    holster_tech = helpers.create_empty_tech()
    holster_tech.repeatable = 1
    holster_tech.icon_id = storage.si + 9
    holster_tech.effect_id = storage.throwerBlacksmithIDs[1]
    holster_tech.required_techs = (102, storage.throwerBlacksmithTechIDs[0], -1, -1, -1, -1)
    holster_tech.required_tech_count = 2
    holster_tech.name = "Holster"
    storage.throwerBlacksmithUpgradeNames.append(holster_tech.name)
    holster_tech.research_locations[0] = ResearchLocation (103, 25, 8, 418010) # 103 in Blacksmith, 25 seconds ResearchTime, Button 8 and Hotkey ID (Onager Ship)
    foodcost: ResearchResourceCost = ResearchResourceCost (1, 225, 1) # 1 wood storage, 225 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 75, 1) # 3 gold storage, 75 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # I added this:
    holster_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_holster_tech = 32338
    storage.throwerBlacksmithStringIDs.append(string_start_holster_tech)
    holster_tech.language_dll_name = string_start_holster_tech
    holster_tech.language_dll_description = string_start_holster_tech + 1000
    holster_tech.language_dll_help = string_start_holster_tech + 100000
    holster_tech.language_dll_tech_tree = string_start_holster_tech + 149000
    df.techs.append (holster_tech)
    logging.debug (f"Added Holster tech at ID {storage.throwerBlacksmithTechIDs[1]}")



    storage.throwerBlacksmithTechIDs.append(len(df.techs))
    balanced_weaponry_tech = helpers.create_empty_tech()
    balanced_weaponry_tech.repeatable = 1
    balanced_weaponry_tech.icon_id = storage.si + 10
    balanced_weaponry_tech.effect_id = storage.throwerBlacksmithIDs[2]
    balanced_weaponry_tech.required_techs = (103, storage.throwerBlacksmithTechIDs[1], -1, -1, -1, -1)
    balanced_weaponry_tech.required_tech_count = 2
    balanced_weaponry_tech.name = "Balanced Weaponry"
    storage.throwerBlacksmithUpgradeNames.append(balanced_weaponry_tech.name)
    balanced_weaponry_tech.research_locations[0] = ResearchLocation (103, 30, 8, 418010) # 103 in Blacksmith, 30 seconds ResearchTime, Button 8 and Hotkey ID of Fortified Wall
    foodcost: ResearchResourceCost = ResearchResourceCost (1, 350, 1) # 1 wood storage, 350 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 175, 1) # 3 gold storage, 175 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # man, I have probably worked a total of 16 hours already on this? - damn if only I wouldn't procrastinate so much
    balanced_weaponry_tech.resource_costs = (foodcost, goldcost, nothing)

    string_start_balanced_weaponry = 32339
    storage.throwerBlacksmithStringIDs.append(string_start_balanced_weaponry)
    balanced_weaponry_tech.language_dll_name = string_start_balanced_weaponry
    balanced_weaponry_tech.language_dll_description = string_start_balanced_weaponry + 1000
    balanced_weaponry_tech.language_dll_help = string_start_balanced_weaponry + 100000
    balanced_weaponry_tech.language_dll_tech_tree = string_start_balanced_weaponry + 149000
    df.techs.append (balanced_weaponry_tech)
    logging.debug (f"Added Balanced Weaponry tech at ID {storage.throwerBlacksmithTechIDs[2]}")




def shield_boss_t (df: DatFile):
    # @Shield boss Tech
    storage.shieldBossTechId = len(df.techs)
    shield_boss_tech = helpers.create_empty_tech()
    shield_boss_tech.repeatable = 1
    shield_boss_tech.icon_id = storage.si + 11
    shield_boss_tech.effect_id = storage.shieldBossId
    shield_boss_tech.required_techs = (102, 875, storage.armenian_shieldBoss_req_ID, -1, -1, -1) #Castle Age and Gambesons are required or Armenians earlier techs
    shield_boss_tech.required_tech_count = 2
    storage.shieldBossUpgradeName = shield_boss_tech.name = "Shield Boss"
    shield_boss_tech.research_locations[0] = ResearchLocation (12, 30, 11, 18090) # 12 in Barracks, 30 seconds ResearchTime, Button 11 and Hotkey ID (Gambesons)
    foodcost: ResearchResourceCost = ResearchResourceCost (1, 160, 1) # 1 wood storage, 160 cost, 1 deduct yes
    goldcost: ResearchResourceCost = ResearchResourceCost (3, 115, 1) # 3 gold storage, 115 cost, 1 deduct yes
    nothing: ResearchResourceCost = ResearchResourceCost (-1, 0, 0) # have a nice day
    shield_boss_tech.resource_costs = (foodcost, goldcost, nothing)

    storage.shieldBossStringID = string_start_shield_boss = 32340
    shield_boss_tech.language_dll_name = string_start_shield_boss
    shield_boss_tech.language_dll_description = string_start_shield_boss + 1000
    shield_boss_tech.language_dll_help = string_start_shield_boss + 100000
    shield_boss_tech.language_dll_tech_tree = string_start_shield_boss + 149000
    df.techs.append (shield_boss_tech)
    logging.debug (f"Added Shield Boss tech at ID {storage.shieldBossTechId}")


    storage.shieldBossTechId2 = len(df.techs)
    shield_boss_tech_2 = copy.deepcopy (shield_boss_tech) # This tech is for all civ that have Shield Boss but no Gambesons. Shield Boss will still be available for some, they just dont need Gambesons
    shield_boss_tech_2.required_techs = (102, -1, -1, -1, -1, -1)
    shield_boss_tech_2.name = "Shield Boss (without Gambesons)"
    shield_boss_tech_2.required_tech_count = 1
    df.techs.append (shield_boss_tech_2)
    logging.debug (f"Added Shield Boss tech at ID {storage.shieldBossTechId2}")

    

def billman_auto_upgrade (df: DatFile):
    # @Billman Auto Upgrade Tech in Castle Age
    billman_auto_upgrade_tech = helpers.create_empty_tech()
    billman_auto_upgrade_tech.name = "BillmanAutoUpgrade Age3"
    billman_auto_upgrade_tech.required_techs = (102, storage.billmanAvailTechID, -1, -1, -1, -1)
    billman_auto_upgrade_tech.effect_id = storage.billmanAutoUpgradeAge3
    billman_auto_upgrade_tech.repeatable = 1
    billman_auto_upgrade_tech.required_tech_count = 2
    df.techs.append(billman_auto_upgrade_tech)
