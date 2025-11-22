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

    

def add_BLL_tech_tree (df: DatFile):

    CIV_TECH_MATRIX = {
    "Armenians":    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Aztecs":       [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
    "Bengalis":     [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    "Berbers":      [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    "Bohemians":    [0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
    "British":      [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Bulgarians":   [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    "Burgundians":  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    "Burmese":      [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    "Byzantine":    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
    "Celts":        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Chinese":      [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    "Cumans":       [0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    "Dravidians":   [1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0],
    "Ethiopians":   [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    "French":       [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Georgians":    [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    "Goths":        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    "Gurjaras":     [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    "Hindustanis":  [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    "Huns":         [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    "Incas":        [0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    "Italians":     [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    "Japanese":     [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    "Jurchens":     [1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0],
    "Khitans":      [1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    "Khmer":        [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    "Koreans":      [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    "Lithuanians":  [1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    "Magyars":      [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0],
    "Malay":        [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1],
    "Malians":      [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    "Mayan":        [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    "Mongols":      [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
    "Persians":     [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    "Poles":        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    "Portuguese":   [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    "Romans":       [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
    "Saracens":     [1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    "Shu":          [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    "Sicilians":    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Slavs":        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Spanish":      [0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    "Tatars":       [1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    "Teutons":      [0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    "Turks":        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    "Vietnamese":   [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    "Vikings":      [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    "Wei":          [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1],
    "Wu":           [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    }

    # list of the 11 tech IDs that correspond to each boolean position
    TECH_IDS_BY_SLOT = [
    storage.shieldBossTechId,               # slot  0 -> Shield Boss
    storage.shieldBossTechId2,              # slot  1 -> Shield Boss without Gambesons req - inserted later, not yet part of Civ Tech Matrix***
    storage.throwingTechniquesTechID,       # slot  2 -> Throwing techniques
    storage.throwerBlacksmithTechIDs[0],    # slot  3 -> Wooden Grip
    storage.throwerBlacksmithTechIDs[1],    # slot  4 -> Holster
    storage.throwerBlacksmithTechIDs[2],    # slot  5 -> Balanced Weaponry
    storage.throwerUpgradeTechs[0],         # slot  6 -> Knife Thrower
    storage.throwerUpgradeTechs[1],         # slot  7 -> Hatchet Thrower
    storage.lancerAvailTechID,              # slot  8 -> Lancer (make avail)
    storage.lancerUpgradeTech,              # slot  9 -> Heavy Lancer
    storage.billmanUpgradeTechs[0],         # slot 10 -> Scytheman
    storage.billmanUpgradeTechs[1]          # slot 11 -> Flail Warrior
    ]

    missing_civ_amount = -7 # I am expected to not include the 6 chronical civs + Gaia. Needs to be updated for each new non-standard civ.

    
    # iterate every civ in the datfile
    for civ_idx, civ in enumerate(df.civs):
        cfg = CIV_TECH_MATRIX.get(civ.name, None)
        if cfg is None:
            # no custom maxtrix for this civ -> skip, +1 to the debug variable
            logging.debug(f"No Tech matrix found for civ {civ.name}")
            missing_civ_amount += 1
            continue
        else:
            if(helpers.does_civ_has_gambesons(df, civ_idx)):
                cfg.insert(1,0) # *** if a civ has gambesons, I use the regular Shield Boss
            elif(cfg[0] == 1):
                cfg.insert(1,1) # *** if civ does not have gambesons, but still Shield Boss, I enable Shield Boss without Gambeson requirement

        # get the effect object for this civ's tech tree
        tech_effect = df.effects[civ.tech_tree_id]

        # for each of the 11 boolean slots, if the config says False -> append a disable command
        for slot_idx, enabled in enumerate(cfg):
            if not enabled:
                tech_id_to_disable = TECH_IDS_BY_SLOT[slot_idx]
                # create an EffectCommand that disables the tech; adjust fields to your encoding
                disable_ec = EffectCommand(102, -1, -1, -1, tech_id_to_disable) # Disable Tech (102), tech_id_to_disable(), 
                tech_effect.effect_commands.append(disable_ec)
        logging.debug(f"Successfully disabled some new techs for {civ.name}")
    if missing_civ_amount!= 0:
        print(f"In File :changing_existing_tech_tree: in :add_BLL_tech_tree: couldn't find {missing_civ_amount} civ(s) and it's corresponding BLL techs")
    else:
        logging.info ("Succesfully shaped the tech tree of all regular AoE2 civs (exluding Chronicals and GAIA)")