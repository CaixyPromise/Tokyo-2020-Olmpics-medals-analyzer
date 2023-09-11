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

def rename_files(race_id, race_name, old_player, new_player,  destination_folder = 'static/reward'):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    old_file_path = f"{race_id}_{race_name}_{old_player}"
    old_file_path = os.path.join(destination_folder, old_file_path)
    if (old_file_path and os.path.exists(old_file_path)):
        return

    new_file_name = f"{race_id}_{race_name}_{new_player}"
    new_file_path = os.path.join(destination_folder, new_file_name)
    os.rename(old_file_path, new_file_path)

def delete_files(race_id, race_name, player,  destination_folder = 'static/reward'):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    old_file_path = f"{race_id}_{race_name}_{player}"
    old_file_path = os.path.join(destination_folder, old_file_path)
    if (old_file_path and os.path.exists(old_file_path)):
        os.remove(old_file_path)