from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *

import copy
import logging

from mods import storage
from mods.helpers import amount_type_to_d

logging.getLogger(__name__)

NAME = "add_effects"

def run_add_effects (df: DatFile):
    make_avail_effect (df)
    unit_upgrades_e (df)
    thrower_upgrades_e (df)
    shield_boss_e (df)
    billman_auto_upgrade (df)
    logging.info("Added all new effects sucessfully")


def make_avail_effect (df: DatFile):
                                                                        
    make_billman_avail: Effect = Effect ("Billman (make avail)", [EffectCommand (2, storage.BillmanIDs[0], 1, -1, -1 )]) #Enable Unit (2), Billman ID, Mode 1, -1 -1
    storage.billmanAvailID = len(df.effects) #determining the ID and storing it
    df.effects.append (make_billman_avail) #add the effect
    logging.debug (f"Added Billman avail effect at ID {storage.billmanAvailID}")

    make_lancer_avail: Effect = Effect ("Lancer (make avail)", [EffectCommand (2, storage.LancerIDs[0], 1, -1, -1 )]) 
    storage.lancerAvailID = len(df.effects)
    df.effects.append(make_lancer_avail)
    logging.debug (f"Added Lancer avail effect at ID {storage.lancerAvailID}")

    make_dartthrower_avail: Effect = Effect ("Dart Thrower (make avail)", [EffectCommand (2, storage.ThrowerIDs[0], 1, -1, -1 )])
    storage.dartthrowerAvailID = len(df.effects)
    df.effects.append(make_dartthrower_avail)
    logging.debug (f"Added Dart Thrower avail effect at ID {storage.dartthrowerAvailID}")

    make_flamethrower_avail: Effect = Effect ("Flamethrower (make avail)", [EffectCommand (2, storage.FlameThrowerID, 1, -1, -1 )]) 
    storage.flamethrowerAvailID = len(df.effects)
    df.effects.append(make_flamethrower_avail)
    logging.debug (f"Added Flamethrower avail effect at ID {storage.flamethrowerAvailID}")
    logging.info ("Successfully added (make avail) effects for all units")

def unit_upgrades_e (df: DatFile):

                                                                                #Upgrade Unit (3), Billman [0], Scytheman [1], Mode -1, -1
    scyteman_upgrade_effect: Effect = Effect ("Scytheman", [EffectCommand (3, storage.BillmanIDs[0], storage.BillmanIDs[1], -1, -1)]) 
    storage.billmanUpgradeIDs.append(len(df.effects)) #determining the ID and storing it
    df.effects.append(scyteman_upgrade_effect)
    logging.debug (f"Added Scyteman upgrade effect at ID {storage.billmanUpgradeIDs[0]}")

                                                                                #Upgrade Unit (3), Scyteman [1], Flail Warrior [2], Mode -1, -1
    flail_warrior_upgrade_effect: Effect = Effect ("Flail Warrior", [EffectCommand (3, storage.BillmanIDs[1], storage.BillmanIDs[2], -1, -1)]) 
    storage.billmanUpgradeIDs.append(len(df.effects))
    df.effects.append(flail_warrior_upgrade_effect)
    logging.debug (f"Added Flailman upgrade effect at ID {storage.billmanUpgradeIDs[1]}")

    
                                                                                #Upgrade Unit (3), Lancer [0], Heavy Lancer [1], Mode -1, -1
    heavy_lancer_upgrade_effect: Effect = Effect ("Heavy Lancer", [EffectCommand (3, storage.LancerIDs[0], storage.LancerIDs[1], -1, -1)]) 
    storage.lancerUpgradeID = len(df.effects) #single ID because only one unit
    df.effects.append(heavy_lancer_upgrade_effect)
    logging.debug (f"Added Heavy Lancer upgrade effect at ID {storage.lancerUpgradeID}")


                                                                                #Upgrade Unit (3), Dart Thrower [0], Knife Thrower [1], Mode -1, -1
    knife_thrower_upgrade_effect: Effect = Effect ("Knife Thrower", [EffectCommand (3, storage.ThrowerIDs[0], storage.ThrowerIDs[1], -1, -1)]) 
    storage.throwerUpgradeIDs.append(len(df.effects))
    df.effects.append(knife_thrower_upgrade_effect)
    logging.debug (f"Added Knife Thrower upgrade effect at ID {storage.throwerUpgradeIDs[0]}")

                                                                                #Upgrade Unit (3), Knife Thrower [1], Hatchet Thrower [2], Mode -1, -1
    hatchet_thrower_upgrade_effect: Effect = Effect ("Hatchet Thrower", [EffectCommand (3, storage.ThrowerIDs[1], storage.ThrowerIDs[2], -1, -1)]) 
    storage.throwerUpgradeIDs.append(len(df.effects))
    df.effects.append(hatchet_thrower_upgrade_effect)
    logging.debug (f"Added Hatchet Thrower upgrade effect at ID {storage.throwerUpgradeIDs[1]}")
    logging.info ("Successfully added all unit Upgrades")

                                                                                 #Upgrade Unit (3), Knife Thrower [1], Ninja [3], Mode -1, -1
    ninja_upgrade_effect: Effect = Effect ("Ninja", [EffectCommand (3, storage.ThrowerIDs[1], storage.ThrowerIDs[3], -1, -1)]) 
    storage.throwerUpgradeIDs.append(len(df.effects))
    df.effects.append(ninja_upgrade_effect)
    logging.debug (f"Added Ninja upgrade effect at ID {storage.throwerUpgradeIDs[2]}")
    logging.info ("Successfully added all unit Upgrades")


def thrower_upgrades_e (df: DatFile):
    #blacksmith upgrades and throwing techniques

    #Throwing techniques: Thrower-line +1 attack; Missed thrown weapons deal full damage. 
    throwing_techniques_ec: EffectCommand = []
    for thrower_id in range(len(storage.ThrowerIDs)):
                                    # Attr. Modifier +-(4), Thrower Unit (ID), Class (-1), Attr. Attack (9), Amount (1), Class Melee Attack (4)
        throwing_techniques_ec.append(EffectCommand(4, storage.ThrowerIDs[thrower_id], -1, 9, amount_type_to_d(1, 4))) 
    
    for thrower_projectile in range(len(storage.ThrowerProjectileIDs)):
                                                    #Attr. Modifier Set (0), Projectiles Unit (ID), Class (-1), Attr. Smart Projectile (19), = 2
        throwing_techniques_ec.append(EffectCommand (0, storage.ThrowerProjectileIDs[thrower_projectile], -1, 19, 2)) # 2 = No Balistics, but full damage on miss, like Arambai
    
    storage.throwingTechniquesID = len(df.effects)

    throwing_techniques_effect: Effect = Effect ("Throwing techniques", throwing_techniques_ec)        
    df.effects.append(throwing_techniques_effect)    
    logging.debug (f"Added Throwing techniques effect at ID {storage.throwingTechniquesID}")
    


    #Wooden Grip: Thrower-line +1 range; missed thrown weapons more accurate
    wooden_grip_ec: EffectCommand = []
    for thrower_id in range(len(storage.ThrowerIDs)):
                                # Attr. Modifier +-(4), Thrower Unit (ID), Class (-1), Attr. Range (12), Amount (1)
        wooden_grip_ec.append(EffectCommand(4, storage.ThrowerIDs[thrower_id], -1, 12, 1))
                                # Attr. Modifier +-(4), Thrower Unit (ID), Class (-1), Attr. LoS (1), Amount (1)
        wooden_grip_ec.append(EffectCommand(4, storage.ThrowerIDs[thrower_id], -1, 1, 1))
                                # Attr. Modifier +-(4), Thrower Unit (ID), Class (-1), Attr. Search Radius (23), Amount (1)
        wooden_grip_ec.append(EffectCommand(4, storage.ThrowerIDs[thrower_id], -1, 23, 1)) 

                                # Attr. Modifier Multiply (5), Thrower Unit (ID), Class (-1), Attr. attack dispersion (64), Amount (0.5 = halved)
        wooden_grip_ec.append(EffectCommand(5, storage.ThrowerIDs[thrower_id], -1, 64, 0.5)) 

    storage.throwerBlacksmithIDs.append(len(df.effects))

    wooden_grip_effect: Effect = Effect ("Wooden Grip", wooden_grip_ec)
    df.effects.append(wooden_grip_effect)
    logging.debug (f"Added Wooden Grip effect at ID {storage.throwerBlacksmithIDs[0]}")



    #Holster: Thrower-line attacks 20% (isn't it theorethically 25%?) faster; no minimum range
    holster_ec: EffectCommand = []
    for thrower_id in range(len(storage.ThrowerIDs)):
                                 # Attr. Modifier Multiply (5), Thrower Unit (ID), Class (-1), Attr. Reload Time (64), Amount (0.80 = 20% faster) 
        holster_ec.append(EffectCommand(5, storage.ThrowerIDs[thrower_id], -1, 10, 0.8))
                                  # Attr. Modifier Set (0), Thrower Unit (ID), Class (-1), Attr. Min Range (20), Amount (0)  
        holster_ec.append(EffectCommand(0, storage.ThrowerIDs[thrower_id], -1, 20, 0))

    storage.throwerBlacksmithIDs.append(len(df.effects))

    holster_effect: Effect = Effect ("Holster", holster_ec)
    df.effects.append(holster_effect)
    logging.debug (f"Added Holster effect at ID {storage.throwerBlacksmithIDs[1]}")



    #Balanced Weaponry: Thrower-line +1 attack; thrown weapons move faster
    balanced_weaponry_ec: EffectCommand = []
    for thrower_id in range(len(storage.ThrowerIDs)):
        
        balanced_weaponry_ec.append(EffectCommand(4, storage.ThrowerIDs[thrower_id], -1, 9, amount_type_to_d(1, 4))) # adds +1 melee attack

    for thrower_projectile in range(len(storage.ThrowerProjectileIDs)):
                                                    #Attr. Modifier +-(4), Projectiles Unit (ID), Class (-1), Attr. Speed (19), = 2 -> increases speed from 6 to 8
        balanced_weaponry_ec.append(EffectCommand (4, storage.ThrowerProjectileIDs[thrower_projectile], -1, 5, 2))

    storage.throwerBlacksmithIDs.append(len(df.effects))

    balanced_weaponry_effect: Effect = Effect ("Balanced Weaponry", balanced_weaponry_ec)
    df.effects.append(balanced_weaponry_effect)
    logging.debug (f"Added Balanced Weaponry effect at ID {storage.throwerBlacksmithIDs[2]}")
    logging.info ("Successfully added all Thrower Blacksmith Upgrades")

def shield_boss_e (df: DatFile):
    affected_vanilla_unit_list = [74, 75, 77, 473, 567, 1793]
    shield_boss_ec: EffectCommand = []

    for unit_id in affected_vanilla_unit_list:
        shield_boss_ec.append(EffectCommand (4, unit_id, -1, 8, amount_type_to_d(1, 3)))

    for billman_id in storage.BillmanIDs:
        shield_boss_ec.append(EffectCommand (4, billman_id, -1, 8, amount_type_to_d(1, 3)))

    
    storage.shieldBossId = len(df.effects)  
    shield_boss_effect: Effect = Effect ("Shield Boss", shield_boss_ec)
    df.effects.append(shield_boss_effect)
    logging.info (f"Successfully added Shield Boss effect at ID {storage.shieldBossId}")
   

def billman_auto_upgrade (df: DatFile):
                                                #Attr. Modifier Multiply(5), Billman (ID), Class (-1), Attr. Train Time (101), * 0.425 = 40s -> 17s
    billman_auto_upgrade_effect: Effect = Effect ("Upgrade Billman in Age3", [EffectCommand (5, storage.BillmanIDs[0], -1, 101, 0.425)]) 
    storage.billmanAutoUpgradeAge3 = len(df.effects)
    df.effects.append(billman_auto_upgrade_effect)
    logging.debug (f"Added auto upgrade effect of Billman in Castle Age at ID {storage.billmanAutoUpgradeAge3}")