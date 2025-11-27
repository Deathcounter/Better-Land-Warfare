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
    burgundian_change (df)
    burmese_change (df)
    dravidian_change (df)
    french_change (df)
    jurchens_change (df)
    malian_change (df)
    slavs_change (df)
    spanish_change (df)
    poles_change (df)
    vietnamese_change (df)
    vikings_change (df)
    logging.info("Successfully changed Civilizations")


def armenians_change (df: DatFile):
    # Since the change of the barrack techs being avail one age earlier is already done, only Fereters is left. 
    # @UniqueTech Fereters
    df.effects[933].effect_commands.clear()
    affected_vanilla_unit_list = [74, 75, 77, 473, 567, 1793, 882, 93, 358, 359] #militia-line, condos, spearmen
    for vanilla_unit in affected_vanilla_unit_list:
                                                            # Attr. Modifier +-(4), vanilla unit, Class -1, Armor (8), Amount (+20), Armorclass Infantry (1)
        df.effects[933].effect_commands.append (EffectCommand (4, vanilla_unit, -1, 8, helpers.amount_type_to_d(20, 1)))
        if vanilla_unit in [93, 358, 359]:
            df.effects[933].effect_commands.append (EffectCommand (4, vanilla_unit, -1, 8, helpers.amount_type_to_d(20, 27))) # give Spearman +20 Spearman armor
        if vanilla_unit == 882:
            df.effects[933].effect_commands.append (EffectCommand (4, vanilla_unit, -1, 8, helpers.amount_type_to_d(20, 19))) # give Condos +20 Unique Unit armor

    for billman in storage.BillmanIDs:
        df.effects[933].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(20, 1)))
        df.effects[933].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(20, 29))) # give Billman +20 Shock Infantry Armor


    warrior_monk_units = [1811, 1826, 1827]
    for warrior_monk in warrior_monk_units:
                                        # Attr. Modifier Mult(5), warrior monk, Class -1, Work Rate (13), Amount (x2)
        df.effects[933].effect_commands.append (EffectCommand (5, warrior_monk, -1, 13, 2))
                                        # Attr. Modifier +-(4), warrior monk, Class -1, Armor (8), Amount (+5), Armorclass Monk (25)
        df.effects[933].effect_commands.append (EffectCommand (4, warrior_monk, -1, 8, helpers.amount_type_to_d(5, 25)))
    logging.debug ("Successfully changed Armenians")

def burgundian_change (df: DatFile):
    # @CivBonus Burgundian
    # Minor Change - Minor Changes are changes that must be made as the result of me adding these units, while keeping the bonus the same
    # All Stable technologies cost -50% (must include Heavy Lancer tech)

    # first, loop through the Burgundian (-> Civ 36, and it's tech tree ID) Tech tree
    tech_tree_id = df.civs[36].tech_tree_id
                        # Tech Cost Modifier (Set/+/-) (101), Technology (Heavy Lancer), Food Storage (0), Mode +-(1), Amount (1075 / 2)
    df.effects[tech_tree_id].effect_commands.append(EffectCommand (101, storage.lancerUpgradeTech, 0, 1, -538)) # implement helpers.discount_tech here on next change
    df.effects[tech_tree_id].effect_commands.append(EffectCommand (101, storage.lancerUpgradeTech, 3, 1, -225)) # same with gold
    logging.debug ("Successfully changed Burgundians")    

def burmese_change (df: DatFile):
    # @CivBonus Burmese
    # Barrack Units +1 attack per Age (instead of all of infantry)
    affected_effects = [686, 687, 688] # Civ Bonuses, give +1 attack per age
    affected_vanilla_unit_list = [74, 75, 77, 473, 567, 1793, 882, 93, 358, 359] # militia-line, condos, spearmen

    for effect in affected_effects:
        df.effects[effect].effect_commands.clear()
        for vanilla_unit in affected_vanilla_unit_list:
                                                            # Attr. Modifier +-(4), vanilla unit, Class -1, Attack (9), Amount (+1), AttackClass Melee (4)
            df.effects[effect].effect_commands.append (EffectCommand (4, vanilla_unit , -1, 9, helpers.amount_type_to_d(1, 4)))


        for billman in storage.BillmanIDs:         # Attr. Modifier +-(4), billman, Class -1, Attack (9), Amount (1), AttackClass Melee (4)
            df.effects[effect].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(1, 4)))
    logging.debug ("Successfully changed Burmese")

def dravidian_change (df: DatFile):
    # @CivBonus Dravidians
    # Minor Change
    # Barrack technologies cost -50% (must include Billman Upgrade techs and Shield Boss)

    # Similar to the Burgundian Change 
    tech_tree_id = df.civs[40].tech_tree_id
                       
    discount_techs = [storage.billmanUpgradeTechs[0], storage.billmanUpgradeTechs[1], storage.shieldBossTechId, storage.shieldBossTechId2]
    effect_command_list = []

    for tech_id in discount_techs:
        effect_command_list.extend(helpers.discount_tech(df, tech_id, 50)) # returns an EffectCommand list with: Tech Cost Modifier (Set/+/-) (101), Technology (tech_id int) , Amount (-50%), All resource Storages (because no specified resource)
    for effect_command in effect_command_list:
        df.effects[tech_tree_id].effect_commands.append(effect_command)
    logging.debug ("Successfully changed Dravidians")    


def french_change (df: DatFile):
    # @CivBonus French/Franks
    # Knights and Lancers +20% HP
    affected_vanilla_unit_list = [38, 283, 569] # knight-line
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
    # @CivBonus Jurchens
    # All Lancer Units (Steppe-, Fire- and regular Lancer) attack +25% faster (20% in coding terms)
    affected_vanilla_unit_list = [1370, 1372, 1901, 1903] # Steppe- and Firelancers
    df.effects[994].effect_commands.clear() # Current Jurchen bonus is at ID 994
    for vanilla_unit in affected_vanilla_unit_list:
        df.effects[994].effect_commands.append (EffectCommand (5, vanilla_unit, -1, 10, 0.8)) # Attr. Modifier Multiply(4), vanilla unit, Class -1, Reload Time (10), Amount (x0.8)
    for lancer in storage.LancerIDs:
        df.effects[994].effect_commands.append (EffectCommand (5, lancer, -1, 10, 0.8)) # Attr. Modifier Multiply(5), lancer, Class -1, Reload Time (10), Amount (x0.8)
    logging.debug ("Successfully changed Jurchens")

def malian_change (df: DatFile):
    # @CivBonus Malians
    # Minor Change
    # Barrack units +1 Pierce Armor per Age (add Billman)

    affected_effects = [618, 619, 620] # C-Bonus, inf +1 armor feudal (castle/imp)

    for effect in affected_effects:
        for billman in storage.BillmanIDs:     # Attr. Modifier +-(4), billman, Class -1, Attack (9), Amount (1), Armorclass Pierce (3)
            df.effects[effect].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(1, 3)))
    logging.debug ("Successfully changed Malians")

def poles_change (df: DatFile):
    # @CivBonus Poles
    # All Stable technologies cost -75% less gold

    # first, loop through the polish (-> Civ 38, and it's tech tree ID) Tech tree
    tech_tree_id = df.civs[38].tech_tree_id
    new_ec_list: list[EffectCommand] = []
    for command in df.effects[tech_tree_id].effect_commands:
        # if the effect command is not 101 Tech Cost Modifier, add it to the new list
        if command.type != 101:
            new_ec_list.append(command)

    # afterwards add my reduction (Husbandry costs no gold)
    stable_discounts = [[435, -75], [254, -38], [786, -600], [209, -225], [storage.lancerUpgradeTech, -338]] # implement helpers.discount_tech here on next change

    for discount in stable_discounts:
                     # Tech Cost Modifier (Set/+/-) (101), Technology (discount[0]), Gold Storage (3), Mode +-(1), Amount (discount[1])
        discount_ec: EffectCommand = EffectCommand (101, discount[0], 3, 1, discount[1])
        new_ec_list.append(discount_ec)

    df.effects[tech_tree_id].effect_commands.clear()
    df.effects[tech_tree_id].effect_commands = new_ec_list
    logging.debug ("Successfully changed Poles")

def slavs_change (df: DatFile):
    # @CivTech Slavs
    # Druzhina: Melee Infantry deals trample damage (exluding Thrower-line)
    for thrower in storage.ThrowerIDs: # remove the blast width of thrower again
        df.effects[569].effect_commands.append (EffectCommand (4, thrower, -1, 22, -0.5)) # Attr. Modifier Multiply(4), thrower, Class -1, blast_width (22), Amount (-0.5)

def spanish_change (df: DatFile):
    # @CivBonus Spanish
    # Minor Change
    # Blacksmith Upgrades cost no gold (include Blacksmith Thrower Upgrades)

    # Similar to the Burgundian Change 
    tech_tree_id = df.civs[14].tech_tree_id
                       
    effect_command_list = []

    for tech_id in storage.throwerBlacksmithTechIDs:
        effect_command_list.extend(helpers.discount_tech(df, tech_id, 100, 3)) # returns an EffectCommand list with: Tech Cost Modifier (Set/+/-) (101), Technology (tech_id int) , Amount (-50%), All resource Storages (because no specified resource)
    for effect_command in effect_command_list:
        df.effects[tech_tree_id].effect_commands.append(effect_command)
    logging.debug ("Successfully changed Spanish")    

def teutons_change (df: DatFile):
    # @CivBonus Teutons
    # Minor Change
    # Barrack and Stable units +1 Melee Armor per Age (add Billman, Lancer)

    affected_effects = [333, 334] # C-Bonus, Inf Cav +1 armor Age3 (Age4)

    for effect in affected_effects:
        for billman in storage.BillmanIDs:      # Attr. Modifier +-(4), billman, Class -1, Attack (9), Amount (1), Armorclass Melee (4)
            df.effects[effect].effect_commands.append (EffectCommand (4, billman, -1, 8, helpers.amount_type_to_d(1, 4)))
        for lancer in storage.LancerIDs:        # Attr. Modifier +-(4), lancer, Class -1, Attack (9), Amount (1), Armorclass Melee (4)
            df.effects[effect].effect_commands.append (EffectCommand (4, lancer, -1, 8, helpers.amount_type_to_d(1, 4)))
    logging.debug ("Successfully changed Teutons")    


def vietnamese_change (df: DatFile):
    # @Civ bonus Vietnamese
    # Foot Archers and Fire Lancers +25% HP
    affected_vanilla_unit_list = [4, 24, 492, 7, 6, 1129, 1131, 1155, 1901, 1903] # Archer-line, Skirmisher-line, Rattan Archers, Fire Lancers
    df.effects[672].effect_commands.clear() # Current Vietnamese bonus is at ID 672
    for vanilla_unit in affected_vanilla_unit_list:
        df.effects[672].effect_commands.append (EffectCommand (5, vanilla_unit, -1, 0, 1.25)) # Attr. Modifier Multiply(5), vanilla unit, Class -1, Hitpoints (0), Amount (x1.25)

    #Rattan Archers -5 HP in change_existing_units
    logging.debug ("Successfully changed Vietnamese")


def vikings_change (df: DatFile):
    # @Civ bonus Vikings
    # Feudal Age Warcost Discount -10% HP cost
    for command in df.effects[394].effect_commands:
        command.d = 0.9 #changed the d of all C-Bonus, Warship cost age2 to x0.9 for an only 10% discount.
        logging.debug ("Successfully changed Vikings")