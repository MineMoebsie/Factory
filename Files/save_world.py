import json
import numpy as np

#seperate functions for each frame during autosave
def save_world_grid(world_folder, grid):
    f = open('Data/Saves/'+world_folder+'/grid.txt','w')
    np.savetxt(f,grid.astype(int), fmt="%i")
    f.close()

def save_world_grid_rotation(world_folder, grid_rotation):
    f = open('Data/Saves/'+world_folder+'/grid_rotation.txt','w')
    np.savetxt(f,grid_rotation.astype(int), fmt="%i")
    f.close()

def save_world_grid_data(world_folder, grid_data):
    json_obj = {"shape": grid_data.shape, "data": grid_data.flatten().tolist()}
    with open('Data/Saves/'+world_folder+'/grid_data.json', "w") as f:
        json.dump(json_obj, f)

def save_world_grid_cables(world_folder, grid_cables):
    f = open('Data/Saves/'+world_folder+'/grid_cables.txt','w')
    np.savetxt(f, grid_cables.reshape((1,-1)), fmt="%s")
    f.close()

def save_world_research_data(world_folder, research_progress):
    f = open('Data/Saves/'+world_folder+'/research_data.txt','w')
    f.write("{}".format(research_progress))
    f.close()

def save_world_keybinds_and_storage(world_folder, keybinds, storage):
    f = open('Data/Saves/'+world_folder+'/storage.txt','w')
    f.write("{}".format(storage))
    f.close()

    f = open('Data/Saves/'+world_folder+'/keybinds.txt','w')
    f.write("{}".format(keybinds))
    f.close()

def save_world_research_grid(world_folder, research_grid):
    f = open('Data/Saves/'+world_folder+'/research_grid.txt','w')
    f.write("{}".format(research_grid))
    f.close()

def save_world_recipes(world_folder, unlocked_recipes, creater_unlocked_recipes):
    with open('Data/Saves/'+world_folder+'/unlocked_recipes.txt','w') as f:
        f.write(str(unlocked_recipes))

    with open('Data/Saves/'+world_folder+'/creater_unlocked_recipes.json','w') as f:
        json.dump(creater_unlocked_recipes, f)

def save_world_delivery(world_folder, to_deliver_list):
   with open('Data/Saves/'+world_folder+'/deliver_list.txt','w') as f:
       f.write(str(to_deliver_list))

def autosave_part(selected_world,grid,grid_rotation,grid_data,grid_cables,research_progress,storage,keybinds,research_grid,unlocked_recipes,creater_unlocked_recipes,to_deliver_list,autosave_state):
    match autosave_state:
        case 2:
            save_world_grid(selected_world, grid)
        case 4:
            save_world_grid_rotation(selected_world, grid_rotation)
        case 6:
            save_world_grid_data(selected_world, grid_data)
        case 8:
            save_world_grid_cables(selected_world, grid_cables)
        case 10:
            save_world_research_data(selected_world, research_progress)
        case 12:
            save_world_keybinds_and_storage(selected_world, keybinds, storage)
        case 14:
            save_world_research_grid(selected_world, research_grid)
        case 16:
            save_world_recipes(selected_world, unlocked_recipes, creater_unlocked_recipes)
        case 18:
            save_world_delivery(selected_world, to_deliver_list)

