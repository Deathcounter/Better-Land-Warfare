import copy
import logging


from genieutils.datfile import DatFile
from genieutils.effect import EffectCommand, Effect
from genieutils.civ import Civ
from genieutils.tech import Tech, ResearchResourceCost
from genieutils.unit import Unit, AttackOrArmor, Task, ResourceCost, ResourceStorage, Type50, Bird, Creatable, Building, TrainLocation

from mods import helpers
from mods import storage



logging.getLogger(__name__)

NAME = "add_units"

def run_add_units(df: DatFile):

    add_Lancer_Dead_Unit (df)
    logging.info("Adding Units one by one")
    logging.info("Billman-line")
    add_Billman_line (df)
    logging.info("Lancer-line")
    add_Lancer_line (df)
    logging.info("Thrower-line")
    add_Thrower_line (df)
    logging.info("Flamethrower")
    add_FlameThrower (df)
    # print("1." + str(helpers.does_civ_have_unit(df, 1, 329))) # false
    

def add_Lancer_Dead_Unit (df: DatFile):
    lancer_dead_unit: Unit = copy.deepcopy(df.civs[47].units[570]) # copy dead unit from Imperial Cavalry by using the Paladin unit but from any Chronical Civ (I chose 47)
    storage.deadLancerUnitID = len(df.civs[0].units)
    for civ in df.civs:
        civ.units.append(lancer_dead_unit)
    logging.info(f"SUCCESS: Dead Lancer Unit added")   

def add_Billman_line(df: DatFile):
    # @Billman
    base = copy.deepcopy(df.civs[0].units[74]) # make a base unit that has all the stats that stay the same within the whole unit-line
    base.enabled = 0

    base.line_of_sight = 4
    base.bird.search_radius = 4

    base.type_50.reload_time = 2.25
    base.type_50.displayed_reload_time = 2.25

    base.creatable.min_conversion_time_mod = -2 # make Unit easier to convert
    base.creatable.max_conversion_time_mod = -2
    
    base.creatable.idle_attack_graphic = -1

    base.type_50.attacks.clear() # delete all info from militia to future proof
    base.type_50.armours.clear()
    base.type_50.attacks = [AttackOrArmor(21,0), AttackOrArmor(15, 0)] # add attacks every infantry has to get (for Arson, Khitan Teambonus)
    base.type_50.armours = [AttackOrArmor(31,0)] # Leitis Armor

    base.creatable.train_locations.clear()
    
    train_location_final: TrainLocation = TrainLocation(17, 12, 3, 416009) # 17s train time, barracks (12), button 3, hotkey ID (Incendiary Raft)
    base.creatable.train_locations.append(train_location_final)

    
    # base.resource_storages - not needed, militia has correct values.... for now
    foodcost: ResourceCost = ResourceCost (0, 45, 1) # 0 food storage, 45 cost, 1 deduct yes
    goldcost: ResourceCost = ResourceCost (3, 45, 1) # 3 gold storage, 45 cost, 1 deduct yes
    headroom: ResourceCost = ResourceCost (4, 1, 0) #  4 population headroom, 1 cost, 0 deduct no
    base.creatable.resource_costs = (foodcost, goldcost, headroom)
    
    name_list = ('Billman', 'Scytheman', 'Flail Warrior')
    storage.billmanNames = name_list
    hp_list = (55, 60, 70) 
    speed_list = (1.08, 1.12, 1.2) 

    displayed_attack_list = (7, 8, 9)
    displayed_m_armor_list = (2, 3, 4)
    base.creatable.displayed_pierce_armour = 0

    # armored units are units whose combined base armor 3 or higher, new armor class needed
                                        # melee,              cavalry,        armored units,        elephant,              billman          standard building
    attack_list_billman         = (AttackOrArmor(4,7), AttackOrArmor(8,3), AttackOrArmor(90,2), AttackOrArmor(5,8),  AttackOrArmor(92,2), AttackOrArmor(21,0))
    attack_list_scytheman       = (AttackOrArmor(4,8), AttackOrArmor(8,3), AttackOrArmor(90,3), AttackOrArmor(5,14), AttackOrArmor(92,3), AttackOrArmor(21,0))
    attack_list_flail_warrior   = (AttackOrArmor(4,9), AttackOrArmor(8,3), AttackOrArmor(90,4), AttackOrArmor(5,18), AttackOrArmor(92,4), AttackOrArmor(21,1))

                                    # melee,                pierce,             infantry,     shock infantry (eagle)    billman
    armor_list_billman  =       (AttackOrArmor(4,2), AttackOrArmor(3,0), AttackOrArmor(1,0), AttackOrArmor(29,0), AttackOrArmor(92,0))
    armor_list_scytheman =      (AttackOrArmor(4,3), AttackOrArmor(3,0), AttackOrArmor(1,0), AttackOrArmor(29,0), AttackOrArmor(92,0))
    armor_list_flail_warrior =  (AttackOrArmor(4,4), AttackOrArmor(3,0), AttackOrArmor(1,0), AttackOrArmor(29,0), AttackOrArmor(92,0))

    storage.billmanUnitIcons = icon_list = (706, 705, 703) # Hills Tribeman, Indian Tribesman, Rhompahaia Warrior

    attack_graphic_list = (storage.billmanAttackID, storage.scythemanAttackID, 15813)
    attack_graphic2_list = (storage.billmanAttackID2, -1, -1)
    dead_unit_list = (2454, 2450, 2394)
    standing_graphic_list= ([16799, -1],[16788, -1],[15816, -1]) # Keep in mind, standing_graphic, despite being singular, requires two int (or rather a tuple)
    dying_graphic_list = (16798, 16787, 15815)
    walking_graphic_list = (16801, 16790, 15818)

    storage.billmanStringID = string_start_billman = 300630

    for idx in range(len(name_list)):
        billman_variant = copy.deepcopy(base) # copy each billman type from the base copy
        billman_variant.id = len(df.civs[0].units) # add ID and loop
        storage.BillmanIDs.append(billman_variant.id) # storage BillmanIDs for later use
        billman_variant.name = name_list[idx] # now go through all these tuples and list and set the stats of each unit
        logging.info(f"Adding {name_list[idx]} at id {billman_variant.id}")

        billman_variant.hit_points = hp_list[idx]

        billman_variant.speed = speed_list[idx]

        billman_variant.icon_id = icon_list [idx]

        billman_variant.type_50.displayed_attack = displayed_attack_list [idx]
        billman_variant.type_50.displayed_melee_armour = displayed_m_armor_list [idx]

        if idx == 0:
            billman_variant.creatable.train_locations[0] = TrainLocation(40, 12, 3, 416009) #billman is 40s in Feudal, then 17 in Castle Age

        for index in range(len(attack_list_billman)):
            if idx == 0:
                attack_billman: AttackOrArmor = attack_list_billman [index] 
                billman_variant.type_50.attacks.append (attack_billman)
            elif idx == 1:
                attack_scytheman: AttackOrArmor = attack_list_scytheman [index] 
                billman_variant.type_50.attacks.append (attack_scytheman)
            elif idx == 2:
                attack_flail_warrior: AttackOrArmor = attack_list_flail_warrior [index] 
                billman_variant.type_50.attacks.append (attack_flail_warrior)
            else:
                print ("Error: Atleast one too much Billman Variant")

        for index in range(len(armor_list_billman)):
            if idx == 0:
                armor_billman: AttackOrArmor = armor_list_billman [index]
                billman_variant.type_50.armours.append (armor_billman)
            elif idx == 1:
                armor_scytheman: AttackOrArmor = armor_list_scytheman [index] 
                billman_variant.type_50.armours.append (armor_scytheman)
            elif idx == 2:
                armor_flail_warrior: AttackOrArmor = armor_list_flail_warrior [index] 
                billman_variant.type_50.armours.append (armor_flail_warrior)
            else:
                print ("Error: Atleast one too much Billman Variant")

        billman_variant.type_50.attack_graphic = attack_graphic_list [idx]
        billman_variant.type_50.attack_graphic_2 = attack_graphic2_list [idx]
        billman_variant.standing_graphic = standing_graphic_list [idx]
        billman_variant.dying_graphic = dying_graphic_list [idx]
        billman_variant.dead_fish.walking_graphic = walking_graphic_list [idx]

        billman_variant.dead_unit_id = dead_unit_list [idx]

        billman_variant.language_dll_name = string_start_billman + idx
        billman_variant.language_dll_creation = string_start_billman + 1000 + idx
        billman_variant.language_dll_help = string_start_billman + 100000 + idx
    
        for civ in df.civs:
            logging.debug(f'adding {billman_variant.name} for civ {civ.name}')
            civ.units.append(billman_variant)


        logging.info(f"SUCCESS: {billman_variant.name} added")    


def add_Lancer_line(df: DatFile):
    # @Lancer
    base = copy.deepcopy(df.civs[0].units[40]) # copy cataphract
    base.enabled = 0

    base.line_of_sight = 4
    base.bird.search_radius = 4

    base.type_50.reload_time = 2
    base.type_50.displayed_reload_time = 2

    base.type_50.max_range = 0.5
    base.type_50.displayed_range = 0.5
    
    base.creatable.idle_attack_graphic = -1

    base.type_50.attacks.clear() # delete all info from cataphract to future proof
    base.type_50.armours.clear()

                            # adds the base attacks of Cavalry so that they can benefit from effects like "cavalry +2 attack vs siege, buildings etc." from various civ- and teambonuses
    base.type_50.attacks = [AttackOrArmor(11,0), AttackOrArmor(15, 0), AttackOrArmor(20, 0), AttackOrArmor(21, 0), AttackOrArmor(38, 0), AttackOrArmor(39, -3) ]
    base.type_50.armours = [AttackOrArmor(31,0)] # Leitis Armor

    base.creatable.train_locations.clear()
    
    train_location_final: TrainLocation = TrainLocation(35, 101, 13, 416007) # 35s train time, stable (101), button 13 - gets changed below, hotkey ID (Monoreme)
    base.creatable.train_locations.append(train_location_final)

    
    # base.resource_storages - not needed, cataphract has correct values.... for now
    foodcost: ResourceCost = ResourceCost (0, 90, 1) # 0 food storage, 90 cost, 1 deduct yes
    goldcost: ResourceCost = ResourceCost (3, 50, 1) # 3 gold storage, 50 cost, 1 deduct yes
    headroom: ResourceCost = ResourceCost (4, 1, 0) #  4 population headroom, 1 cost, 0 deduct no
    base.creatable.resource_costs = (foodcost, goldcost, headroom)

    name_list = ('Lancer', 'Heavy Lancer')
    storage.lancerNames = name_list
    hp_list = (115, 145)
    speed_list = (1.25, 1.3) 

    displayed_attack_list = (8, 10)
    displayed_m_armor_list = (3, 5)
    displayed_p_armor_list = (0, 1)

    # armored units are units whose combined base armor 3 or higher, new armor class needed
                                # melee,                camel               armored units
    attack_list_lancer      = (AttackOrArmor(4,8),  AttackOrArmor(30,2), AttackOrArmor(90,6)) 
    attack_list_heavylancer = (AttackOrArmor(4,10), AttackOrArmor(30,3), AttackOrArmor(90,9))

                                # melee,                pierce,             cavalry           lancer unit
    armor_list_lancer       = (AttackOrArmor(4,3), AttackOrArmor(3,0), AttackOrArmor(8,4), AttackOrArmor(91,0))
    armor_list_heavylancer  = (AttackOrArmor(4,5), AttackOrArmor(3,1), AttackOrArmor(8,8), AttackOrArmor(91,0))

    storage.lancerUnitIcons = icon_list = (709, 612) # Companion Cavalry, Imperial Cavalry
    attack_graphic_list = (15801, 15138)
    attack_graphic2_list = (-1, -1)
    dead_unit_list = (2392, storage.deadLancerUnitID)
    standing_graphic_list= ([15804, 15802], [15140, 15764]) # Keep in mind, standing_graphic, despite being singular, requires two int (or rather a tuple)
    dying_graphic_list = (15803, 15139)
    walking_graphic_list = (15806, 15143)

    storage.lancerStringID = string_start_lancer = 300637

    for idx in range(len(name_list)):
        lancer_variant = copy.deepcopy(base) # copy each lancer type from the base copy
        lancer_variant.id = len(df.civs[0].units) # add ID and loop
        storage.LancerIDs.append(lancer_variant.id)
        lancer_variant.name = name_list[idx] # now go through all these tuples and list and set the stats of each unit
        logging.info(f"Adding {name_list[idx]} at id {lancer_variant.id}")

        lancer_variant.hit_points = hp_list[idx]

        lancer_variant.speed = speed_list[idx]

        lancer_variant.icon_id = icon_list [idx]

        lancer_variant.type_50.displayed_attack = displayed_attack_list [idx]
        lancer_variant.type_50.displayed_melee_armour = displayed_m_armor_list [idx]
        lancer_variant.creatable.displayed_pierce_armour = displayed_p_armor_list [idx]

        for index in range(len(attack_list_lancer)):
            if idx == 0:
                attack_lancer: AttackOrArmor = attack_list_lancer [index] 
                lancer_variant.type_50.attacks.append (attack_lancer)
            elif idx == 1:
                attack_scyteman: AttackOrArmor = attack_list_heavylancer [index] 
                lancer_variant.type_50.attacks.append (attack_scyteman)
            else:
                logging.error("Error: Atleast one too much Lancer Variant")

        for index in range(len(armor_list_lancer)):
            if idx == 0:
                armor_lancer: AttackOrArmor = armor_list_lancer [index]
                lancer_variant.type_50.armours.append (armor_lancer)
            elif idx == 1:
                armor_heavylancer: AttackOrArmor = armor_list_heavylancer [index] 
                lancer_variant.type_50.armours.append (armor_heavylancer)
            else:
                logging.error("Error: Atleast one too much Lancer Variant")

        lancer_variant.type_50.attack_graphic = attack_graphic_list [idx]
        lancer_variant.type_50.attack_graphic_2 = attack_graphic2_list [idx]
        lancer_variant.standing_graphic = standing_graphic_list [idx]
        lancer_variant.dying_graphic = dying_graphic_list [idx]
        lancer_variant.dead_fish.walking_graphic = walking_graphic_list [idx]

        lancer_variant.dead_unit_id = dead_unit_list [idx]

        lancer_variant.language_dll_name = string_start_lancer + idx
        lancer_variant.language_dll_creation = string_start_lancer + 1000 + idx
        lancer_variant.language_dll_help = string_start_lancer + 100000 + idx

        lancer_variant_4 = copy.deepcopy(lancer_variant)
        lancer_variant_4.creatable.train_locations[0].button_id = 4
        lancer_variant_13 = copy.deepcopy(lancer_variant)
        lancer_variant_13.creatable.train_locations[0].button_id = 13  
        lancer_variant_2 = copy.deepcopy(lancer_variant)
        lancer_variant_2.creatable.train_locations[0].button_id = 2  

        for idx in range(len(df.civs)):
            if helpers.does_civ_have_unit (df, idx, 329) and idx is not 53: # if civ has Camels and is not Khitans
                if helpers.does_civ_have_unit (df, idx, 1370): # if civ has Camels AND Steppe Lancers
                    button = 13
                    df.civs[idx].units.append(lancer_variant_13) # put the Lancer in Slot 13 (even tho those civs won't get lancers) - also Full tech tree is another can of worms
                else:
                    button = 4
                    df.civs[idx].units.append(lancer_variant_4) # put the Lancer-line in Slot 4
            elif idx == 53: # Khitans get Lancer on Button 2
                button = 2
                df.civs[idx].units.append(lancer_variant_2)
            else:
                button = 3
                lancer_variant.creatable.train_locations[0].button_id = 3 # put the Lancer-line in Slot 3 (normal stable slot)
                df.civs[idx].units.append(lancer_variant)
            logging.debug(f'adding {lancer_variant.name} for civ {df.civs[idx].name} at button {button}')
        logging.info(f"SUCCESS: {lancer_variant.name} added")       

def add_Thrower_line(df: DatFile):
    # @Thrower
    base = copy.deepcopy(df.civs[0].units[74]) # make a base unit that has all the stats that stay the same within the whole unit-line
    base.enabled = 0

    base.type_50.min_range = 1
    base.type_50.accuracy_dispersion = 0.6

    base.type_50.reload_time = 1.5
    base.type_50.displayed_reload_time = 1.5
    
    base.creatable.idle_attack_graphic = -1

    base.type_50.blast_attack_level = 3
    base.type_50.blast_damage = 1

    base.creatable.creatable_type = 5 # this makes it so that in a unit formation, the Thrower is at the back, and not mixed like gbetos are in the base game

    base.type_50.graphic_displacement = [0, 0.5, 1.5]

    base.type_50.attacks.clear() #delete all info from cataphract to future proof
    base.type_50.armours.clear()

    base.type_50.attacks = [AttackOrArmor(15, 0)] # add attacks every infantry has to get (Khitan Teambonus)
    base.type_50.armours = [AttackOrArmor(31,0)] # Leitis Armor

    base.creatable.train_locations.clear()
    
    train_location_final: TrainLocation = TrainLocation(30, 87, 9, 416008) # 30s train time, archery range (87), button 9, hotkey ID (Galley - Antiquity)
    base.creatable.train_locations.append(train_location_final)

    # thrower.resource_storages - not needed, militia has correct values.... for now
    foodcost: ResourceCost = ResourceCost (0, 35, 1) # 0 food storage, 35 cost, 1 deduct yes
    goldcost: ResourceCost = ResourceCost (3, 35, 1) # 3 gold storage, 35 cost, 1 deduct yes
    headroom: ResourceCost = ResourceCost (4, 1, 0) #  4 population headroom, 1 cost, 0 deduct no
    base.creatable.resource_costs = (foodcost, goldcost, headroom)

    name_list = ('Dart Thrower', 'Knife Thrower', 'Hatchet Thrower', 'Ninja')
    storage.throwerNames = name_list
    hp_list = (35, 40, 45, 45)
    speed_list = (1, 1.05, 1.05, 1.1) 
    frame_delay_list = (16, 14, 14, 12)

    range_list = (3, 4, 5, 6)
    displayed_range_list = (3, 4, 5, 6)
    accuracy_list = (65, 70, 75, 90)

    displayed_attack_list = (3, 4, 5, 4)
    displayed_m_armor_list = (0, 1, 1, 1)
    displayed_p_armor_list = (0, 0, 1, 0)

                                    # melee,                skirmisher,        standard building,    armored units           
    attack_list_dart_thrower    = (AttackOrArmor(4,3), AttackOrArmor(38,2), AttackOrArmor(21,0), AttackOrArmor(90,1))
    attack_list_knife_thrower   = (AttackOrArmor(4,4), AttackOrArmor(38,3), AttackOrArmor(21,1), AttackOrArmor(90,3))
    attack_list_hatchet_thrower = (AttackOrArmor(4,5), AttackOrArmor(38,3), AttackOrArmor(21,2), AttackOrArmor(90,3))
    attack_list_ninja           = (AttackOrArmor(4,4), AttackOrArmor(38,3), AttackOrArmor(21,1), AttackOrArmor(90,3), AttackOrArmor (19, 3)) # extra attack vs unique units

                                     # melee,               pierce,         infantry,     
    armor_list_dart_thrower    = (AttackOrArmor(4,0), AttackOrArmor(3,0), AttackOrArmor(1,0))
    armor_list_knife_thrower   = (AttackOrArmor(4,1), AttackOrArmor(3,0), AttackOrArmor(1,0))
    armor_list_hatchet_thrower = (AttackOrArmor(4,1), AttackOrArmor(3,1), AttackOrArmor(1,0))
    armor_list_ninja           = (AttackOrArmor(4,1), AttackOrArmor(3,0), AttackOrArmor(1,0))

    storage.throwerUnitIcons = icon_list = (704, 693, 140, 299) # Phalangite, Rhodian Slinger, Norse Warrior, Ninja
    
    # Graphics of (Yodit, Rhodian Slinger, Norse Warrior, Ninja)
    attack_graphic_list = (3900, 15654, storage.silentNorseWarriorID, storage.silentNinjaID)
    attack_graphic2_list = (-1, 15659, -1, -1)
    dead_unit_list = (1625, 2367, 362, 1147)
    standing_graphic_list= ([3902, -1], [15656, -1], [7628, -1], [1037, -1]) # Keep in mind, standing_graphic, despite being singular, requires two int (or rather a tuple)
    dying_graphic_list = (storage.yoditDeathScreamID, 15655, 7627, 1034)
    walking_graphic_list = (3905, 15658, 7630, 1041)

    storage.throwerStringID = string_start_thrower = 300633

    for idx in range(len(name_list)):
        thrower_variant = copy.deepcopy(base) # copy each thrower type from the base copy
        thrower_variant.id = len(df.civs[0].units) # add ID and loop
        storage.ThrowerIDs.append(thrower_variant.id)
        thrower_variant.name = name_list[idx] # now go through all these tuples and list and set the stats of each unit
        logging.info(f"Adding {name_list[idx]} at id {thrower_variant.id}")

        thrower_variant.hit_points = hp_list[idx]
        thrower_variant.speed = speed_list[idx]
        thrower_variant.type_50.frame_delay = frame_delay_list[idx]

        thrower_variant.type_50.max_range = range_list[idx]
        thrower_variant.type_50.displayed_range = displayed_range_list[idx]
        thrower_variant.type_50.accuracy_percent = accuracy_list[idx]

        thrower_variant.icon_id = icon_list [idx]
        thrower_variant.type_50.projectile_unit_id = storage.ThrowerProjectileIDs[idx]

        thrower_variant.type_50.displayed_attack = displayed_attack_list [idx]
        thrower_variant.type_50.displayed_melee_armour = displayed_m_armor_list [idx]
        thrower_variant.creatable.displayed_pierce_armour = displayed_p_armor_list [idx]

        if idx > 0:
            thrower_variant.creatable.train_locations[0].train_time = 25 # Knife and Hatchet thrower train time is shorter than dart thrower (30s -> 25s)

        for index in range(len(attack_list_dart_thrower)):
            if idx == 0:
                attack_dartthrower: AttackOrArmor = attack_list_dart_thrower [index] 
                thrower_variant.type_50.attacks.append (attack_dartthrower)
            elif idx == 1:
                attack_knifethrower: AttackOrArmor = attack_list_knife_thrower [index] 
                thrower_variant.type_50.attacks.append (attack_knifethrower)
            elif idx == 2:
                attack_hatchetthrower: AttackOrArmor = attack_list_hatchet_thrower [index] 
                thrower_variant.type_50.attacks.append (attack_hatchetthrower)
                thrower_variant.line_of_sight = 5
                thrower_variant.bird.search_radius = 5
            elif idx == 3:
                attack_ninja: AttackOrArmor = attack_list_ninja [index] 
                thrower_variant.type_50.attacks.append (attack_ninja)
                thrower_variant.line_of_sight = 6
                thrower_variant.bird.search_radius = 6
                if index+1 == len(attack_list_dart_thrower):
                    thrower_variant.type_50.attacks.append (attack_list_ninja [index+1]) # add the extra attack vs unique units
            else:
                logging.error("Error: Atleast one too much Thrower Variant")

        for index in range(len(armor_list_ninja)):
            if idx == 0:
                armor_dartthrower: AttackOrArmor = armor_list_dart_thrower [index]
                thrower_variant.type_50.armours.append (armor_dartthrower)
            elif idx == 1:
                armor_knifethrower: AttackOrArmor = armor_list_knife_thrower [index] 
                thrower_variant.type_50.armours.append (armor_knifethrower)
            elif idx == 2:
                armor_hatchetthrower: AttackOrArmor = armor_list_hatchet_thrower [index] 
                thrower_variant.type_50.armours.append (armor_hatchetthrower)
            elif idx == 3:
                armor_ninja: AttackOrArmor = armor_list_ninja [index] 
                thrower_variant.type_50.armours.append (armor_ninja)
            else:
                logging.error("Error: Atleast one too much Thrower Variant")

        thrower_variant.type_50.attack_graphic = attack_graphic_list [idx]
        thrower_variant.type_50.attack_graphic_2 = attack_graphic2_list [idx]
        thrower_variant.standing_graphic = standing_graphic_list [idx]
        thrower_variant.dying_graphic = dying_graphic_list [idx]
        thrower_variant.dead_fish.walking_graphic = walking_graphic_list [idx]

        thrower_variant.dead_unit_id = dead_unit_list [idx]

        thrower_variant.language_dll_name = string_start_thrower + idx
        thrower_variant.language_dll_creation = string_start_thrower + 1000 + idx
        thrower_variant.language_dll_help = string_start_thrower + 100000 + idx
    
        for civ in df.civs:
            logging.debug(f'adding {thrower_variant.name} for civ {civ.name}')
            civ.units.append(thrower_variant)


        logging.info(f"SUCCESS: {thrower_variant.name} added")


def add_FlameThrower(df: DatFile):
    # @Flamethrower
    flame_thrower = copy.deepcopy(df.civs[0].units[188]) # copy flamethrower

    flame_thrower.name = "Flamethrower"
    storage.flamethrowerName = flame_thrower.name
    flame_thrower.id = len(df.civs[0].units)  # assign new ID
    storage.FlameThrowerID = flame_thrower.id
    flame_thrower.enabled = 0

    flame_thrower.hit_points = 85
    flame_thrower.speed = 0.85

    flame_thrower.line_of_sight = 7
    flame_thrower.bird.search_radius = 7

    flame_thrower.type_50.max_range = 6
    flame_thrower.type_50.displayed_range = 6

    flame_thrower.type_50.min_range = 2

    flame_thrower.type_50.reload_time = 0.25
    flame_thrower.type_50.displayed_reload_time = 0.25

    flame_thrower.type_50.blast_width = 0.2
    flame_thrower.type_50.blast_attack_level = 1 # so they can only destroy trees and no gold
    
    flame_thrower.creatable.idle_attack_graphic = -1

    flame_thrower.bird.attack_sound = 476
    flame_thrower.bird.wwise_attack_sound_id = -311600688 # reverse engineered using # print(json.dumps(dataclasses.asdict(dfBase.civs[0].units[280]), indent=2)) in create_mod.py

    flame_thrower.type_50.attacks.clear() #delete all info from flamethrower to future proof
    flame_thrower.type_50.armours.clear()

    flame_thrower.type_50.displayed_attack = 5
                                        #melee,             building class,      standardbuilding,    stone defenses,           gunpowder,          So that flamethrowers only deal 5 damage to trees
    flame_thrower.type_50.attacks = [AttackOrArmor(4,5) , AttackOrArmor(11,5), AttackOrArmor(21,3), AttackOrArmor(13,-5), AttackOrArmor(23,2), AttackOrArmor(93, -5)] 
                                        #melee,                 pierce,             rams,                   siege                                          
    flame_thrower.type_50.armours = [AttackOrArmor(4,-3), AttackOrArmor(3,12), AttackOrArmor(17,0), AttackOrArmor(20,0), AttackOrArmor(31,0)] # Leitis Armor
    # Flamethrower damage vs buildings per minute (with masonry, and architecture) 2400 (1440, 720)
    
    flame_thrower.type_50.displayed_melee_armour = -3
    flame_thrower.creatable.displayed_pierce_armour = 12

    storage.flamethrowerUnitIcon = flame_thrower.icon_id = 144 # not really needed cause the base flame thrower already has it


    flame_thrower.creatable.train_locations.clear()
    
    train_location_final: TrainLocation = TrainLocation(65, 49, 13, 416012) # train time, Siege Workshop (49), button 13, hotkey ID (Leviathan)
    flame_thrower.creatable.train_locations.append(train_location_final)

    # thrower.resource_storages - not needed, copy has correct values.... for now
    woodcost: ResourceCost = ResourceCost (1, 80, 1) # 1 wood storage, 80 cost, 1 deduct yes
    goldcost: ResourceCost = ResourceCost (3, 110, 1) # 3 gold storage, 110 cost, 1 deduct yes
    headroom: ResourceCost = ResourceCost (4, 1, 0) #  4 population headroom, 1 cost, 0 deduct no
    flame_thrower.creatable.resource_costs = (woodcost, goldcost, headroom)

    storage.flamethrowerStringID = string_start_flamer = 300639
    
    flame_thrower.language_dll_name = string_start_flamer
    flame_thrower.language_dll_creation = string_start_flamer + 1000
    flame_thrower.language_dll_help = string_start_flamer + 100000

    for civ in df.civs:
        logging.debug(f'adding {flame_thrower.name} for civ {civ.name}')
        civ.units.append(flame_thrower)
    logging.info(f"SUCCESS: {flame_thrower.name} added")