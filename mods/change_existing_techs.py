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
    temp[1] = 950 #add 950 to Squires [215] in Slot 2 so its available in Feudal Age
    df.techs[875].required_techs = tuple(temp) 

def move_elite_genitour_to_castle (df: DatFile):
    #moving Elite Genitour Upgrade to Castle in order to make space for thrower line and upgrade
    df.effects[37].effect_commands[2].d = 9 #changes the Berber Teambonus [37] to move the research location to button 9 instead of 14
    df.techs[599].research_locations[0].location_id = 82 #changes the research location of Elite Genitour [599] from Archery Range to Castle (82)