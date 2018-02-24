from os import system
from random import randint
from math import sqrt, ceil
from class_definitions import create_table
from local_modules.keyboard_master import keyboard # event listeners for keyboard
from time import sleep

game_break = False # creating end condition for game screen loop
player_inventory = {}

dim = int(input("Tile dimension?\n")) # getting world dimensions from user
world = create_table(dim) # creating "world" object in "table" class with user input
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
world.mod_char(player_pos[x],y,"@") # marking origin on map
world.print_tile() # printing the world for the first time

"""
functions for motion
"""
stored_tile = ["O"] # stores the tile the player is currently on (initial value will mark origin

def reset_pos(): # resets after motion the tile that the player was on
    world.mod_char(player_pos[x],player_pos[y],stored_tile[0])

accepted_motions = ["w","a","s","d","2w","2a","2s","2d"]
def player_move(motion):
    if motion == "w":
        if player_pos[y]+1 > dim or player_pos[y]+1 < 0:
            print("You cannot leave the map!")
        else:
            reset_pos() # clears character position and replaces with previous tile
            del stored_tile[0]
            player_pos[y] += 1 # moves character location on virtual map
            stored_tile.append(world.char(player_pos[x], player_pos[y]))  # stores tile that is about to be moved onto

while True:
    sleep(0.1)
    player_input = keyboard.read_key()

    if player_input in accepted_motions: # get player input to move on virtual map
        player_move(player_input)
    elif player_input == "z":
        print(stored_tile)
        break # loop kill switch
    elif player_input == "e":
        system("cls")
        print(f"Inventory: {player_inventory}")
        while True:
            e_input = input("Enter inventory command: \n")
            if e_input == "e":
                break
            elif e_input in player_inventory:
                player_inventory[e_input] = not player_inventory[e_input]
                if player_inventory[e_input] == True:
                    item_state = "active"
                else:
                    item_state = "inactive"
                print("{} is now {}!\n".format(e_input, item_state))
            else:
                print("Unrecognized command")
        system("cls")
    else:
        print("Invalid key input!")
    world.mod_char(player_pos[x], player_pos[y],"@") # stores character location to virtual map

    system("cls") # clears existing map
    world.print_tile() #prints world (and new character location)
    print("Coordinates:")
    print(player_pos)

########################################################################################################################
"""
# resets player position
def reset_pos():
    world[player_pos[1]][player_pos[0]] = "."

# gets input to move player via editing player_pos and updating that location with reset_pos
def player_move(motion):
    system("clear")
    if motion == "w":
        if (player_pos[y]-1) > (world_dim-1) or (player_pos[y]-1) < 0:
            print("You cannot leave the world boundaries!")
        else:
            print(" ")
            reset_pos()
            player_pos[y] -= 1
    elif motion == "s":
        if (player_pos[y]+1) > (world_dim-1) or (player_pos[y]+1) < 0:
            print("You cannot leave the world boundaries!")
        else:
            print(" ")
            reset_pos()
            player_pos[y] += 1
    elif motion == "a":
        if (player_pos[x]-1) > (world_dim-1) or (player_pos[x]-1) < 0:
            print("You cannot leave the world boundaries!")
        else:
            print(" ")
            reset_pos()
            player_pos[x] -= 1
    elif motion == "d":
        if (player_pos[x]+1) > (world_dim-1) or (player_pos[x]+1) < 0:
            print("You cannot leave the world boundaries!")
        else:
            print(" ")
            reset_pos()
            player_pos[x] += 1
    else:
        print("Invalid key entry.")



# actually running the game here
# constantly getting user input
while True:
    # defining player on world map as "X" based on player cords
    world[player_pos[1]][player_pos[0]] = "X"
    # printing game board with player on it
    print_board(world)
    # moving player
    p_input = input()
    if p_input == "z":
        break
    elif p_input == "e":
        system("clear")
        print("Inventory: {}".format(inventory.keys()))
        while True:
            e_input = input("Enter inventory command: \n")
            if e_input == "e":
                break
            elif e_input in inventory:
                inventory[e_input] = not inventory[e_input]
                if inventory[e_input] == True:
                    item_state = "active"
                else:
                    item_state = "inactive"
                print("{} is now {}!\n".format(e_input,item_state))
            else:
                print("Unrecognized command")
        system("clear")
    else:
        player_move(p_input)
    # print indices of player location
    print("abs position")
    print(player_pos)
    # print coordinates
    print("coordinates")
    print("({},{})".format(player_pos[x]+1,player_pos[y]+1))
"""