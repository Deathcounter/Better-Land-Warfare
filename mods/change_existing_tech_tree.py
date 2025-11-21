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
NAME = "change_existing_civs"

#As to why I change these civs, refer to the Game Design document of the mod
def run_change_tech_tree (df: DatFile):
    add_BLL_tech_tree (df)
    logging.info("Successfully shaped the Tech Trees")


def add_BLL_tech_tree (df):
    Armenians:      list [bool] = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    Aztecs:         list [bool] = [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]
    Bengalis:       list [bool] = [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1]
    Berbers:        list [bool] = [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0]
    Berbers:        list [bool] = [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0]