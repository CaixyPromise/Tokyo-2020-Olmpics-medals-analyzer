import os
import shutil


def copy_and_rename_files(paths, race_id, race_name, players,  destination_folder = 'static/reward'):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    print(paths, race_id, race_name, players,)
    for path, player in zip(paths, players):

        print(race_id,race_name,player)
        new_file_name = f"{race_id}_{race_name}_{player}"
        new_file_path = os.path.join(destination_folder, new_file_name)
        shutil.copy(path, new_file_path)