#These are all the IDs added through various modules in this script. This file allows cross-module access to these IDs
#For example, when I add a new unit, I need to access to it's ID to make the (make avail) effect. Then I need the ID of that effect to add the corresponding technology of it
from pathlib import Path 

lightmode = False #if True basically disables function who might take a longer time and shouldn't be resolved every test run

# constants
techStrings =   ["Scytheman", "FlailWarrior", "HeavyLancer", "KnifeThrower", "HatchetThrower", "Ninja", 
                "ThrowingTechniques", "WoodenGrip", "Holster", "BalancedWeaponry", "ShieldBoss"]


#sounds
dartSoundID: int

#graphics
dartProjectileGraphicID: int # with custom sound
silentNorseWarriorID: int # removes the melee audio of Norse Warrior 
silentNinjaID: int # and Ninja
yoditDeathScreamID: int

#units
deadLancerUnitID: int

ThrowerProjectileIDs = []

BillmanIDs = []
LancerIDs = []
ThrowerIDs = []
FlameThrowerID: int

#unit names
billmanNames = []
lancerNames = []
throwerNames = []
flamethrowerName = str

#effects
billmanAvailID: int
lancerAvailID: int
dartthrowerAvailID: int 
flamethrowerAvailID: int

billmanUpgradeIDs = []
lancerUpgradeID: int
throwerUpgradeIDs = []

throwingTechniquesID: int
throwerBlacksmithIDs = []

shieldBossId: int

billmanAutoUpgradeAge3: int

#technologies
billmanAvailTechID: int
lancerAvailTechID: int
dartthrowerAvailTechID: int 
flamethrowerAvailTechID: int

armenian_scyteman_req_ID: int
armenian_flailWarrior_req_ID: int
armenian_shieldBoss_req_ID: int

billmanUpgradeTechs = []
lancerUpgradeTech: int
throwerUpgradeTechs = []

throwingTechniquesTechID = int
throwerBlacksmithTechIDs = []

shieldBossTechId: int
shieldBossTechId2: int

billmanAutoUpgradeAge3: int

#tech icons
si: int = 312 # Starting Icon, the last vanilla aoe2 Icon
billmanIconIDs = [si+1, si+2]
lancerIconID = si+3
throwerIconIDs = [si+4, si+5, si+6]

throwingTechniquesIconID = si+7

throwerBlacksmithIconIDs = [si+8, si+9, si+10]

shieldBossIconID = si+11

#folder paths
datFolder: Path
soundFolder: Path
dataModFolder: Path
languageFolders = []

UIModFolder: Path
widgetUIFolder: Path
techIconFolder: Path

blwDatPath: Path
constantsPath: Path

# Json content
techIconList = []