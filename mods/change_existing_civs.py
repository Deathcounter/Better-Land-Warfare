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
NAME = "change_existing_civs"

#As to why I change these civs, refer to the Game Design document of the mod
def run_change_existing_civs (df: DatFile):
    armenians_change (df)
    burmese_change (df)
    french_change (df)
    jurchens_change (df)
    poles_change (df)
    logging.info("Successfully changed Civilizations")


def armenians_change (df: DatFile):
    # Since the change of the barrack techs being avail one age earlier is already done, only Fereters is left. 
    # @Fereters
    df.effects[933].effect_commands.clear()
    affected_vanilla_unit_list = [74, 75, 77, 473, 567, 1793, 882, 93, 358, 359] #militia-line, condos, spearmen
    for vanilla_unit in affected_vanilla_unit_list:
                                                            # Attr. Modifier +-(4), vanilla unit, Class -1, Armor (8), Amount (+10), Armorclass Infantry (1)
        df.effects[933].effect_commands.append (EffectCommand (4, vanilla_unit, -1, 8, helpers.amount_type_to_d(10, 1)))


    for billman in storage.BillmanIDs:
        df.effects[933].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(10, 1)))


    warrior_monk_units = [1811, 1826, 1827]
    for warrior_monk in warrior_monk_units:
                                        # Attr. Modifier Mult(5), warrior monk, Class -1, Work Rate (13), Amount (x2)
        df.effects[933].effect_commands.append (EffectCommand (5, warrior_monk, -1, 13, 2))
                                        # Attr. Modifier +-(4), warrior monk, Class -1, Armor (8), Amount (+5), Armorclass Monk (25)
        df.effects[933].effect_commands.append (EffectCommand (4, warrior_monk, -1, 8, helpers.amount_type_to_d(5, 25)))
    logging.debug ("Successfully changed Armenians")
    
def burmese_change (df: DatFile):
    # @Civbonus Burmese
    affected_effects = [686, 687, 688] # Civ Bonuses, give +1 attack per age
    affected_vanilla_unit_list = [74, 75, 77, 473, 567, 1793, 882, 93, 358, 359] #militia-line, condos, spearmen

    for effect in affected_effects:
        df.effects[effect].effect_commands.clear()
        for vanilla_unit in affected_vanilla_unit_list:
                                                            # Attr. Modifier +-(4), vanilla unit, Class -1, Attack (9), Amount (+1), Armorclass Infantry (1)
            df.effects[effect].effect_commands.append (EffectCommand (4, vanilla_unit , -1, 9, helpers.amount_type_to_d(1, 4)))


        for billman in storage.BillmanIDs:         # Attr. Modifier +-(4), billman, Class -1, Attack (9), Amount (1), Armorclass Melee (4)
            df.effects[effect].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(1, 4)))
    logging.debug ("Successfully changed Burmese")


def french_change (df: DatFile):
    # @Civbonus French/Franks
    # Knights and Lancers +20% HP
    affected_vanilla_unit_list = [38, 283, 569] #knight-line
    df.effects[285].effect_commands.clear() # Current Franks bonus is at ID 285
    for vanilla_unit in affected_vanilla_unit_list:
        df.effects[285].effect_commands.append (EffectCommand (5, vanilla_unit, -1, 0, 1.2)) # Attr. Modifier Multiply(5), vanilla unit, Class -1, Hitpoints (0), Amount (x1.2)
    for lancer in storage.LancerIDs:
        df.effects[285].effect_commands.append (EffectCommand (5, lancer, -1, 0, 1.2)) # Attr. Modifier Multiply(5), lancer, Class -1, Hitpoints (0), Amount (x1.2)

    # Forager are 20% faster
    df.effects[523].effect_commands[0].d = 1.20
    df.effects[523].effect_commands[1].d = 1.20
    logging.debug ("Successfully changed Franks")
    

def jurchens_change (df: DatFile):
    # @Civbonus Jurchens
    # All Lancer Units (Steppe-, Fire- and regular Lancer) attack +25% faster
    affected_vanilla_unit_list = [1370, 1372, 1901, 1903] # Steppe- and Firelancers
    df.effects[994].effect_commands.clear() # Current Jurchen bonus is at ID 994
    for vanilla_unit in affected_vanilla_unit_list:
        df.effects[994].effect_commands.append (EffectCommand (5, vanilla_unit, -1, 10, 0.8)) # Attr. Modifier Multiply(4), vanilla unit, Class -1, Reload Time (10), Amount (x0.8)
    for lancer in storage.LancerIDs:
        df.effects[994].effect_commands.append (EffectCommand (5, lancer, -1, 10, 0.8)) # Attr. Modifier Multiply(5), lancer, Class -1, Reload Time (10), Amount (x0.8)
    logging.debug ("Successfully changed Jurchens")


def poles_change (df: DatFile):
    # @Civbonus Poles
    # All Stable technologies cost -75% less gold

    # first, loop through the polish (-> Civ 38, and it's tech tree ID) Tech tree
    tech_tree_id = df.civs[38].tech_tree_id
    for idx, command in enumerate(df.effects[tech_tree_id].effect_commands):
        # if the effect command is 101 Tech Cost Modifier, delete it
        if command.type == 101:
            df.effects[df.civs[38].tech_tree_id].effect_commands.pop(idx)

    # afterwards add my reduction (Husbandry costs no gold)
    stable_discounts = [[435, -75], [254, -38], [786, -600], [175, -225], [storage.lancerUpgradeTech, -338]]

    for discount in stable_discounts:
                     # Tech Cost Modifier (Set/+/-) (101), Technology (discount[0]), Gold Storage (3), Mode +-(1), Amount (discount[1])
        discount_ec: EffectCommand = EffectCommand (101, discount[0], 3, 1, discount[1])
        df.effects[tech_tree_id].effect_commands.append(discount_ec)
    logging.debug ("Successfully changed Poles")