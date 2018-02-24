from os import system
from class_definitions import create_table
from local_modules.keyboard_master import keyboard # event listeners for keyboard
from time import sleep
from pprint import pprint

# inventory system
def speed_potion_effect():
    global speed_potion
    global speed
    readout_text = "You used a speed potion!"
    speed += 1
    moves_until_effect_expires["speed"] += speed_potion["duration"]
    print(readout_text)

speed_potion = {
    "name": "speed potion",
    "duration": 12, # might have to be tweaked a bit
    "item_id": "100",
    "quantity": 1,
    "effect": speed_potion_effect


}

# global-scope variables
game_break = False # creating end condition for game screen loop
player_inventory = [speed_potion] # hard-coding a speed potion into the inventory for now
speed = 1 # for speed potion; DO NOT SET TO ZERO FOR ANY REASON
number_of_player_moves = 0 # count of player moves for effect duration
moves_until_effect_expires = {
    "speed": 0
}


dim = int(input("Tile dimension?\n")) # getting world dimensions from user
world = create_table(dim,"world") # creating "world" object in "table" class with user input
world.mod_col(1, "#")   #
world.mod_col(dim, "#") # defining map boundaries
world.mod_row(dim,"#")  #
system("cls") # clearing screen to prepare for game


### FINDING PLAYER SPAWN POINT ###
player_pos = [1,1] # creating player coordinate storage
x = 0 # easy access to player position indices
y = 1
spawn_row = world.row(1)
i = 1
for item in spawn_row: # finding empty space in first row for player to spawn
    if item == " ":
        player_pos[x] = i
        break
    i += 1
world.mod_char(player_pos[x],y,"+") # marking origin on map
world.print_tile() # printing the world for the first time

"""
functions for motion
"""
stored_tile = ["O"] # stores the tile the player is currently on (initial value will mark origin

def reset_pos(): # resets after motion the tile that the player was on
    world.mod_char(player_pos[x],player_pos[y],stored_tile[0])

def detect_collision(coordinate,direction):
    collision_output = []
    if coordinate == "x":
        for dict_element in world.tile_elements:
            if world.char(player_pos[x]+direction,player_pos[y]) == dict_element["character"] and dict_element["is_viable"] == False:
                collision_output.append(True)
                collision_output.append(dict_element["name"])
                return collision_output
                #return True

        collision_output.append(False)
        return collision_output
                #return False
    elif coordinate == "y":
        for dict_element in world.tile_elements:
            if world.char(player_pos[x],player_pos[y]+direction) == dict_element["character"] and dict_element["is_viable"] == False:
                collision_output.append(True)
                collision_output.append(dict_element["name"])
                return collision_output
                #return True

        collision_output.append(False)
        return collision_output
                #return False


accepted_motions = [["w","a","s","d"],["2w","2a","2s","2d"]]
def player_move(motion):
    global speed
    global number_of_player_moves
    global moves_until_effect_expires
    number_of_player_moves += 1 # upping the count of player moves by one

    # making speed timer count down
    if speed > 1:
        if moves_until_effect_expires["speed"] == 0:
            speed -= 1
        else:
            moves_until_effect_expires["speed"] -= 1
    if motion == "w":
        for i in range(0, speed):
            if player_pos[y]+1 > dim-1 or player_pos[y]+1 < 1:
                print("You cannot leave the map!")
                sleep(0.5)
            elif detect_collision("y",1)[0] == True:
                print("Collision detected:")
                print("You cannot traverse a {}".format(detect_collision("y",1)[1]))
                sleep(0.5)
            else:
                reset_pos() # clears character position and replaces with previous tile
                del stored_tile[0]
                player_pos[y] += 1 # moves character location on virtual map
                stored_tile.append(world.char(player_pos[x], player_pos[y]))  # stores tile that is about to be moved onto
    elif motion == "s":
        for i in range(0, speed):
            if player_pos[y]-1 > dim-1 or player_pos[y]-1 < 1:
                print("You cannot leave the map!")
                sleep(0.5)
            elif detect_collision("y",-1)[0] == True:
                print("Collision detected:")
                print("You cannot traverse a {}".format(detect_collision("y",-1)[1]))
                sleep(0.5)
            else:
                reset_pos()
                del stored_tile[0]
                player_pos[y] -= 1
                stored_tile.append(world.char(player_pos[x], player_pos[y]))
    elif motion == "a":
        for i in range(0, speed):
            if player_pos[x]-1 > dim-1 or player_pos[x]-1 < 2:
                print("You cannot leave the map!")
                sleep(0.5)
            elif detect_collision("x",-1)[0] == True:
                print("Collision detected:")
                print("You cannot traverse a {}".format(detect_collision("x",-1)[1]))
                sleep(0.5)
            else:
                reset_pos()
                del stored_tile[0]
                player_pos[x] -= 1
                stored_tile.append(world.char(player_pos[x], player_pos[y]))
    elif motion == "d":
        for i in range(0, speed):
            if player_pos[x]+1 > dim-1 or player_pos[x]+1 < 2:
                print("You cannot leave the map!")
                sleep(0.5)
            elif detect_collision("x",1)[0] == True:
                print("Collision detected:")
                print("You cannot traverse a {}".format(detect_collision("x",1)[1]))
                sleep(0.5)
            else:
                reset_pos()
                del stored_tile[0]
                player_pos[x] += 1
                stored_tile.append(world.char(player_pos[x], player_pos[y]))
while True:
    sleep(0.1)
    player_input = keyboard.read_key()

    if player_input in accepted_motions[0]: # get player input to move on virtual map
        player_move(player_input)
    elif player_input == "z":
        break # loop kill switch
    elif player_input == "e":
        system("cls")
        print(f"Inventory: \n")
        pprint(player_inventory) # display inventory
        while True: # inventory system
            e_input = input("Enter inventory command: \n")
            if e_input == "e":
                break
            elif any (item["name"] == e_input for item in player_inventory): # if there is an item object in player inventory with name input by user
                for item in player_inventory: # iterate through and find it
                    if e_input == item["name"]:
                        if item["quantity"] == 0: # if no more of this item in inventory
                            print("You are out of this item. ")
                            break
                        else:
                            item["quantity"] -=1 # remove one of the item from inventory
                            item["effect"]() # and use its effect
            else:
                print("Unrecognized command")
        system("cls")
    else:
        print("Invalid key input!")
    world.mod_char(player_pos[x], player_pos[y],"+") # stores character location to virtual map

    system("cls") # clears existing map
    world.print_tile() #prints world (and new character location)
    print("Coordinates:")
    print(player_pos)

########################################################################################################################