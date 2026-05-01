How to use:

Fill folders with gamefiles:
blw dat folder content -
1. Fill the folder blw dat with the entire CivTechTrees folder (as a whole) from C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\\_common\dat\CivTechTrees
2. Fill the folder  blw dat with following files from the same game file folder as Step 1.: futuravailableunits.json , unitlines.json , unitcategories.json
3. Add to the blw dat folder following game files from C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\widgetui: icons.json , materials.json , techtreepreviewpanel.json
4. The folder "constants" with all the mod content should be there and filled as it is part of the repository (if not I probably outsourced it to some Google Drive if github limit is reached)

datfiles folder content -
5. Fill the folder "datfiles" with the game's .dat file empires2_x2_p1.dat located at the path of Step 1.

6. Rename it to "base_game.dat"

7. The code will generate a modded empires2_x2_p1.dat, therefore you have to do Step 6.

With the folders now filled (the code will tell you if there is something missing) it is time to run create_mod.py in a Python Virtual environment and the libraries of requirements.txt running

Once it's done, it will fill the finished mod folder structure in the folder "finished_mods", however with the empires2_x2_p1.dat still missing because:

8. Open the "empires2_x2_p1.dat" in A.G.E Advanced Genie Editor then save it again and close (idk what it does, but it adds a few bytes and makes custom sounds work)

9. Copy the said file into [...]\finished_mods\Better Land Warfare (Official Data Mod)\resources\\_common\dat (probably don't call it Official Data Mod, that name is taken)

10. Copy the content of finished_mods\Better Land Warfare (Official Data Mod) - (resources folder, readme.txt and thumbnail.png) as well as (widgetui folder, thumbnail.png of the UI mod) and paste it in a local mod to test (Games\Age of Empires 2 DE\\[Your SteamID]\mods\local\Better Land Warfare) extensively ingame. 

Add a info.json with "{"Author":"Unpublished","CacheStatus":0,"Description":"Continued by [Your Name]","Title":"Better Land Warfare (Local Data Mod)"}" and save to avoid confusion between the published and local mod.
Feel free to add a readme.txt with the mod too linking to the Game Design document 

11. Repeat with the UI mod

12. Test if all changes were ingame and test for bugs

13. If everything is fine, double check if the content of the local mod and the finished_mods folder are really the one and the same .dat file

Publishing Mod:
Go to https://www.ageofempires.com/mods and publish a new mod/edit your current one.

14. Go into finished_mods\Better Land Warfare (Official Data Mod) & the UI mod. Select the file as in Step 10 -> create a ZIP file and name it Better Land Warfare (Continued UI/Data Mod) - any info.json file does not need to be part of the zip. 

Note that the UI mod doesn't really need updates much often, compared to the Data Mod. So think whether you changed something about the files that the UI mod consists of.

15. Publish the files in the mod center on the website above