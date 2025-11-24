from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.tech import ResearchLocation
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *
import logging

logging.getLogger(__name__)

NAME = "helpers"



# finds the (make avail)-able or upgrade effect (not tech) of a unit with the id
def find_unit_avail_or_upgrade (df: DatFile, unit_id: int) -> int:
    for effect in df.effects:
        for command in effect.effect_commands:
            if (command.type == 2 and command.b == 1 and command.a == unit_id) or (command.type == 3 and command.b == unit_id and command.c == -1): 
                # if (Command type = enable/disable unit, and Mode = 1 = enabled and unit = unit id) OR
                # (commandy type = Upgrade Unit and any Unit is upgraded to the searched unit with Mode -1 = all)
                unit_avail_effect = df.effects.index(effect)
                logging.debug(f"found unit avail of unit {unit_id} at id {unit_avail_effect}")
                return unit_avail_effect
    logging.debug("No Unit avail effect found for")
    return -1

# finds the tech that contains the (make avail)-able effect
def find_tech_of_unit_avail (df: DatFile, effect_id: int) -> int:
    if (effect_id != -1):
        for tech in df.techs:
            if tech.effect_id == effect_id:
                # if the tech that executes the effect make avail is equal to the searched effect
                tech_avail_of_effect = df.techs.index(tech)
                logging.debug(f"found tech avail of effect {effect_id} at id {tech_avail_of_effect}")
                return tech_avail_of_effect
        logging.debug("No Tech avail effect found")
    return -1

# Returns true or false based on whether civ has a certain unit by looking if the make avail tech is disabled or not
# Doesnt work with Winged Hussar due to different structure. Camel hardcoded because Camel scout is ruining the function
def does_civ_have_unit (df: DatFile, civilization: int, unit_id: int) -> bool:
    tech_tree_id = df.civs[civilization].tech_tree_id # storing tech tree ID 
    if unit_id == 329:
        unit_avail_tech = 235 #hardcoding CamelCase
    else:
        unit_avail_tech = find_tech_of_unit_avail(df, find_unit_avail_or_upgrade(df, unit_id))
    # finds the Tech that makes the unit available by using the other two helpers
    civ_has_unit = True
    if (df.civs[civilization].units[unit_id].enabled == 1):
        for train_location in df.civs[civilization].units[unit_id].creatable.train_locations:
            if (train_location.unit_id != -1):
                # Unit is available from Dark Age onwards and has a train location.
                return True
        # Unit is available from Dark Age onwards, but has no train locations
        return False
    
    if (unit_avail_tech == -1):
        # if there is no make avail tech
        return False
    
    if (df.techs[unit_avail_tech].civ == civilization):
        # checks if an tech available has one specific civilization, AKA Unique Units
        # e.g If Plumed Archer (make avail) tech is only available for (Mayans == Mayans) - then Mayans have Plumed Archer
        civ_has_unit = True

    elif (df.techs[unit_avail_tech].civ != -1):
        #Unit is Unique Unit, but not of the searched civ
        civ_has_unit = False

    elif (len(df.civs[civilization].units[unit_id].creatable.train_locations) == 0 or df.civs[civilization].units[unit_id].disabled == 1):
        # unit of that civ has no train locations or unit is disabled
        civ_has_unit = False

    else:
        for command in df.effects[tech_tree_id].effect_commands: # looping through all effect commands of the tech tree effect
            if (command.type == 102 and command.d == unit_avail_tech):
                    # if command.type == disable tech (102) and the tech == tech that makes the unit avail
                    # Unit is specifically disabled in tech tree
                    civ_has_unit = False
                    break    
                    
    if(civ_has_unit):
        logging.debug(f"{df.techs[unit_avail_tech].name} is available for {df.civs[civilization].name}")
        return civ_has_unit
    else:
        logging.debug(f"The upgrade or avail tech {unit_avail_tech} {df.techs[unit_avail_tech].name}, is disabled for {df.civs[civilization].name}")
        return civ_has_unit 
   
def does_civ_has_gambesons (df: DatFile, civilization: int) -> bool:
    # Yes, I could have added the logic to make "does_civ_has_tech"...could have
    tech_tree_id = df.civs[civilization].tech_tree_id # storing tech tree ID 
    
    for command in df.effects[tech_tree_id].effect_commands:
        if(command.type == 102 and command.d == 875):
            return False
    return True



# Function that finds the base unit of any unit, returns ID of the unit e.g Paladin returns Knight, Plumed Archer returns Plumed Archer, Imperial Camel returns Camel Scout
def find_base_unit (df: DatFile, unit_id: int) -> int:
    effect_id = find_unit_avail_or_upgrade (df, unit_id)
    if effect_id == -1:
      return unit_id
    for command in df.effects[effect_id].effect_commands:
      if (command.type == 3 and command.b == unit_id and command.c == -1):
        # if command type == upgrade unit, and the unit is upgraded to the searched unit
        return find_base_unit(df, command.a)    
    return unit_id


def find_units_with_3_combined_armor (df: DatFile) -> list[Unit]:
    units_with_3_combined_armor: list[Unit] = []
    for unit in df.civs[0].units:
        if (unit and unit.type == 70 and unit.class_ in (0, 4, 6, 12, 18, 23, 24, 25, 26, 35, 43, 44)): 
            # if Unit is not None and is Combatant (70) or in one of the soldier classes (excludes siege, ships)
            unit_armor = 0
            base_unit_id = find_base_unit(df, unit.id) # does the !!BASE!! unit have 3 combined armor?
            for armor in df.civs[0].units[base_unit_id].type_50.armours:
                if (armor.class_== 4 or armor.class_ == 3): # if armor class is pierce or melee
                    unit_armor += armor.amount
            if (unit_armor >= 3):
                units_with_3_combined_armor.append(unit) # Append to unit list
    return units_with_3_combined_armor   

def discount_tech (df: DatFile, tech: int, percentage: int, costtype = None) -> list [EffectCommand]:
    if (df.techs[tech]):
        ec_list: list[EffectCommand] = []
        # Both Costs must be in the first two ResearchResourceCost
        types: list[int] = [df.techs[tech].resource_costs[0].type, df.techs[tech].resource_costs[1].type]
        amounts: list[int] = [df.techs[tech].resource_costs[0].amount, df.techs[tech].resource_costs[1].amount]
        mode = 1 # Mode 1 = +-, Mode 0 = Set
        if (percentage == 100):
            mode = 0 # if the percentage is 100, then I set the cost to 0 instead. The discount gets set to 0 (by multiplying with 0) and the mode gets adjusted

        discount = lambda amt: int(-abs(amt * percentage / 100) * mode) # calculating discount, making it negative with -abs and rounding by converting it to int()

        if (costtype is None):
            for idx in range(len(types)):
                        # Tech Cost Modifier (Set/+/-) (101), Technology (Tech), type (idx), Mode +- (1) or Set (0), Amount (discount)
                ec_list.append(EffectCommand (101, df.techs.index(df.techs[tech]), types[idx], mode, discount(amounts[idx])))
        else:   
            # if a specific costtype is declared, it only discounts e.g the gold cost of a tech
            for idx, resources in enumerate(df.techs[tech].resource_costs):
                if (resources.type == costtype): # determining where the type of the tech equals the specified type
                    ec_list.append(EffectCommand (101, df.techs.index(df.techs[tech]), types[idx], mode, discount(df.techs[tech].resource_costs[idx].amount)))
        
        return ec_list            
    else:           
        print("Something wrong in helpers.discount_tech")
        return None

def create_empty_task() -> Task:
    return Task(
        task_type=1, 
        id=-1,
        is_default=0,
        action_type=0,
        class_id=-1,
        unit_id=-1,
        terrain_id=-1,
        resource_in=-1,
        resource_multiplier=-1,
        resource_out=-1,
        unused_resource=-1,
        work_value_1=0,
        work_value_2=0,
        work_range=0,
        auto_search_targets=0,
        search_wait_time=0,
        enable_targeting=0,
        combat_level_flag=0,
        gather_type=0,
        work_flag_2=0,
        target_diplomacy=0,
        carry_check=0,
        pick_for_construction=0,
        moving_graphic_id=-1,
        proceeding_graphic_id=-1,
        working_graphic_id=-1,
        carrying_graphic_id=-1,
        resource_gathering_sound_id=-1,
        resource_deposit_sound_id=-1,
        wwise_resource_gathering_sound_id=0,
        wwise_resource_deposit_sound_id=0,
        enabled=-1,
    )


def pack_amount_and_type(amount: int, typ: int) -> int:
    """Pack signed 8-bit amount and unsigned 8-bit type into an int (type in high byte, amount in low byte)."""
    amt_byte = amount & 0xFF    # two's complement 8-bit
    typ_byte = typ & 0xFF
    return (typ_byte << 8) | amt_byte


def amount_type_to_d_test(amount: int, typ: int) -> float:
    return float(pack_amount_and_type(amount, typ))

# Hello, Deathcounter here, I used all functions after this msg from helper.py from genieutils-examples https://github.com/Krakenmeister/genieutils-examples 
# - Credits to him, thank you <3


# EffectCommands D value is always a float, meaning it can only hold one value
# However, for EffectCommands that alter armors or attacks, one float must hold both the AttackOrArmor's class and amount
# This helper function will convert an amount and attack/armor type into a float that can be used for a D value in an EffectCommand
def amount_type_to_d(value: int, type: int) -> float:
    # Ensure the input is within the range of an 8-bit signed integer
    value = value & 0xFF  # Mask to 8 bits
    if value & 0x80:  # Handle sign extension for negative numbers
        value -= 0x100

    # Ensure the type is within the range of an 8-bit unsigned integer
    type = type & 0xFF

    # Combine value and type into a 32-bit integer
    NewD = (type << 8) | (value & 0xFF)

    # Convert to float and return
    return float(NewD)

# Create a technology with default values -- no requirements, time to research, etc.
def create_empty_tech() -> Tech:
    empty_cost: ResearchResourceCost = ResearchResourceCost(-1, 0, 0)
    return Tech(
        required_techs=(-1, -1, -1, -1, -1, -1),
        resource_costs=(empty_cost, empty_cost, empty_cost),
        required_tech_count=0,
        civ=-1,
        full_tech_mode=0,
        language_dll_name=7000,
        language_dll_description=8000,
        effect_id=-1,
        type=0,
        icon_id=-1,
        language_dll_help=107000,
        language_dll_tech_tree=150000,
        name="",
        repeatable=0,
        research_locations=[ResearchLocation(-1,0,0,-1)],
    )
