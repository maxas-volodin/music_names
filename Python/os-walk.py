import os
import sys

import composer_legacy

tmp_target_dir = ""
tmp_all_legacies = []

if len (sys.argv) == 1:
    tmp_target_dir = 'c:/maxas/sound/symphony/Chopin'
elif len (sys.argv) == 2:
    tmp_target_dir = sys.argv [1]
else:
    print ("Too many arguments")
    exit ()

if composer_legacy.ComposerLegacy.is_composer_legacy (os.path.split (tmp_target_dir) [1]):
    print ("Folder", tmp_target_dir, "contains composer legacy!")
    new_legacy = composer_legacy.ComposerLegacy(os.path.join (tmp_target_dir), os.path.split (tmp_target_dir) [1])
    new_legacy.collect_legacy ()
    tmp_all_legacies.append (new_legacy)
else:
    for tmp_root, tmp_folders, tmp_files in os.walk (tmp_target_dir):
        for this_folder in tmp_folders:
            if composer_legacy.ComposerLegacy.is_composer_legacy (this_folder):
                print ("Folder", this_folder, "contains composer legacy!")
                new_legacy = composer_legacy.ComposerLegacy (os.path.join (tmp_root, this_folder), this_folder)
                new_legacy.collect_legacy ()
                tmp_all_legacies.append (new_legacy)

for next_composer in tmp_all_legacies:
    next_composer.print_legacy()
