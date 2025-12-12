from genieutils.datfile import DatFile
from genieutils.task import Task
from genieutils.civ import Civ
from genieutils.effect import Effect, EffectCommand
from genieutils.tech import ResearchResourceCost, Tech
from genieutils.unit import *
import logging

from mods import helpers
from mods import storage


logging.getLogger(__name__)

NAME = "change_existing_techs"


def run_change_existing_techs(df: DatFile):
    change_armenian_early_barracks_techs (df)
    move_elite_genitour_to_castle (df)
    change_gambesons_to_give_HP (df)
    blacksmith_infantry_attack_upgrades (df)
    japanese_staggering_attackspeed (df)


def change_armenian_early_barracks_techs (df: DatFile):
    #here I change the immutable tuple into a list, in case the original tech gets an additional required tech, then back again.

    temp = list(df.techs[950].required_techs) 
    temp[0] = 101 #set the "C-Bonus, Early Barracks techs" = 950, in Slot 1 from Dark to Feudal Age = 101, because starting in Feudal
    df.techs[950].required_techs = tuple(temp)

    temp = list(df.techs[87].required_techs) 
    temp[1] = -1 #remove 950 from spearman avail tech [87] which was in Slot 2
    df.techs[87].required_techs = tuple(temp) 

    temp = list(df.techs[215].required_techs) 
    temp[1] = 950 #add 950 to Squires [215] in Slot 2 so its available in Feudal Age
    df.techs[215].required_techs = tuple(temp) 

    temp = list(df.techs[875].required_techs) 
    temp[1] = 950 #add 950 to Gambesons [875] in Slot 2 so its available in Feudal Age
    df.techs[875].required_techs = tuple(temp) 



def move_elite_genitour_to_castle (df: DatFile):
    #moving Elite Genitour Upgrade to Castle in order to make space for thrower line and upgrade
    df.effects[38].effect_commands[2].d = 9 #changes the Berber Teambonus [38] to move the research location to button 9 instead of 14
    df.techs[599].research_locations[0].location_id = 82 #changes the research location of Elite Genitour [599] from Archery Range to Castle (82)


# technically should be in change_existing_effect.py but don't tell Police pls
def change_gambesons_to_give_HP (df: DatFile):
    #Change Gambesons to give +10 HP to Billman
    for idx in storage.BillmanIDs:
        add_10_HP_to_Billmen: EffectCommand = EffectCommand(4, idx, -1, 0, 10) # Attr. Modifier +-(4), BillmanID (idx), Class -1, Hitpoints (0), Amount (+10)
        df.effects[886].effect_commands.append(add_10_HP_to_Billmen)

def blacksmith_infantry_attack_upgrades (df: DatFile):
    #Change Infantry Attack Upgrades to not affect Thrower-line
    infantry_attack_upgrade_IDs = [67, 68, 75]
    for infantry_attack_upgrade in infantry_attack_upgrade_IDs:
        for thrower in storage.ThrowerIDs:
                                                # Attr. Modifier +-(4), ThrowerId, Class -1, Attack(9), Amount (-1), Melee Attackclass (4)
            if (infantry_attack_upgrade == 75):
                value = -1026 #turns into negative -1 for melee Attack class
            else:
                value = -1025 #turns into negative -2 for melee Attack class (Blast Furnace)
                
            remove_Thrower_attack: EffectCommand = EffectCommand(4, thrower, -1, 9, value)     
            df.effects[infantry_attack_upgrade].effect_commands.append(remove_Thrower_attack)

def japanese_staggering_attackspeed (df: DatFile):
    agetechs = [104, 101, 102, 103]
    technames = [10, 15, 20, 25]
    for idx, jap_effect in enumerate(storage.japaneseStaggeredAS_IDs):
        japanese_staggering_as_tech = helpers.create_empty_tech()
        japanese_staggering_as_tech.required_techs = (agetechs[idx], -1, -1, -1, -1, -1)
        japanese_staggering_as_tech.effect_id = jap_effect
        japanese_staggering_as_tech.civ = 5 # Japanese
        japanese_staggering_as_tech.repeatable = 1
        japanese_staggering_as_tech.required_tech_count = 1
        japanese_staggering_as_tech.name = f"C-Bonus, {technames [idx]} Inf Attack Spd"
        df.techs.append(japanese_staggering_as_tech)

def vikings_staggering_HP (df: DatFile):
    agetechs = [104, 101, 102, 103]
    technames = [10, 15, 20, 25]
    for idx, vik_effect in enumerate(storage.vikingStaggeredHP_IDs):
        viking_staggering_HP_tech = helpers.create_empty_tech()
        viking_staggering_HP_tech.required_techs = (agetechs[idx], -1, -1, -1, -1, -1)
        viking_staggering_HP_tech.effect_id = vik_effect
        viking_staggering_HP_tech.civ = 11 # Vikings
        viking_staggering_HP_tech.repeatable = 1
        viking_staggering_HP_tech.required_tech_count = 1
        viking_staggering_HP_tech.name = f"C-Bonus, +{technames [idx]}% HP"
        df.techs.append(viking_staggering_HP_tech)