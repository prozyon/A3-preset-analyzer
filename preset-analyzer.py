import os
import tempfile
import csv

from distutils.dir_util import copy_tree
from xml.dom import minidom

# Workshop-Path:
wspath = 'D:\\Games\\Steam\\steamapps\\workshop\\content\\107410'

# ArmA-Profile Presets:
presetpath = os.getenv('LOCALAPPDATA') + '\Arma 3 Launcher\Presets'
try:
    #Creating temporary folder
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir_name = temp_dir.name
    print('Created temporary directory', temp_dir_name)
    #Copying preset2-Files from preset folder to temporary folder
    copy_tree(presetpath, temp_dir_name);
    print('Copied presets to temporary directory', temp_dir_name)
    #Deleting defaultpreset2-file as its not needed
    os.remove(temp_dir_name + '\\arma3.defaultpreset2')
    # Listing the files of the folder
    files = os.listdir(temp_dir_name)
    print('Renaming files for analysis...')
    # rename each file one by one
    for file_name in files:
        # construct full file path
        old_name = os.path.join(temp_dir_name, file_name)
        # Changing the extension from preset2 to xml for easier parsing later
        new_name = old_name.replace('.preset2', '.xml')
        os.rename(old_name, new_name)

    print('Renaming successful!')
    print('Parsing Mod-Ids....')
    #Creating list for storage of mod ids
    mod_ids_preset = []
    renamed_files = os.listdir(temp_dir_name)
    #parsing each xml file one by one
    for xmlfile in renamed_files:
        #Parsing an xml file by name
        full_path = os.path.join(temp_dir_name, xmlfile)
        file = minidom.parse(full_path)
        #use getElementsByTagName() to get tag
        ids = file.getElementsByTagName('id')
        #getting data from each entry in the file with the matching tag
        for elem in ids:
                mod_ids_preset.append(elem.firstChild.data)

    #deleting duplicate ids in the list
    unique_ids_preset = list(set(mod_ids_preset))
    number_of_unique_ids = len(unique_ids_preset)
    print('Found ' +  str(number_of_unique_ids)  + ' unique Mod-Ids in your presets.')
    print('Comparing Ids in presets with ids in Steam Workshop folder....')
    #getting all ids of installed mods from the workshop folder
    workshop = os.listdir(wspath)
    #removing !Workshop entry
    workshop.pop(0)
    #adding steam: modifier to ease comparison
    workshop_id = []
    for entry in workshop:
        workshop_id.append('steam:' + entry)

    #Comparing boths lists and saving mod ids not used in preset
    unused_mods_ids = list(set(workshop_id).difference(unique_ids_preset))
    #path to output file on the desktop of the user
    desktop_path = os.getenv('USERPROFILE') + '\\Desktop\\unused-mods.csv'
    # open csv file in write mode
    with open(desktop_path, 'w') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(unused_mods_ids)

    print('Presets have been analyzed and the results have been saved in a CSV-file on your Desktop!')

except Exception as e:
    print(e)
