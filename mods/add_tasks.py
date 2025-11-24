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

NAME = "add_tasks"

def run_add_tasks (df: DatFile):
    add_Billman_killreward (df)



# https://docs.google.com/document/d/1lrwcqVOS_PrXbOP8uedIw3KduWPF8xEo1rIEWvaDUQU/ refer to this document or Tiger Cavalry in A.G.E
# Billman-line get attack (+2/+3/+4) when killing units (up to two times)
def add_Billman_killreward (df: DatFile):
    affected_classes = [0, 6, 12, 13, 18, 20, 22, 23, 35, 36, 43, 44, 47, 51, 53, 54, 55, 59]
    billman_attack_gain = [2, 3, 4]
    base_task = helpers.create_empty_task()
    base_task.action_type = 154
    base_task.proceeding_graphic_id = 12263 # Level up
    base_task.carry_check = 2
    base_task.search_wait_time = 9 # gain attack
    base_task.combat_level_flag = 1 # I think, idk what unused flag is?
    base_task.target_diplomacy = 1
    base_task.work_flag_2 = 2 # up to two times
    

    for idx, billman in enumerate(storage.BillmanIDs):
            for unit_class in affected_classes:
                task = copy.deepcopy(base_task)
                task.id = len(df.civs[0].units[billman].bird.tasks)
                task.class_id = unit_class
                task.gather_type = billman_attack_gain[idx] # 2/3/4 attack
                df.civs[0].units[billman].bird.tasks.append(task)
                