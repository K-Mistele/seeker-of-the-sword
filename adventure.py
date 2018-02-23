from os import system

# creating empty world and loop end
world = []
inventory = {"speed potion": False, "sword":True}
game_break = False

# change to increase square dimensions (edge lengths) of the world
# world 0-indexed, so world_dim is length but max dim is world_dim-1
world_dim = int(input("World dimension?"))

# setting up initial board print so that location does'nt shift as commands are input

system("clear")
print("\n")
print("\n")
print(" ")
# tracking player position
# player_pos[0] = horizontal coordinate = x
# player_pos[1] = vertical coordinate = y
player_pos = [int(world_dim/2),int(world_dim/2)]
x = 0
y = 1

# creating the world
for i in range(world_dim):
    world.append(["."]*world_dim)

# marking the ORIGIN
world[0][0] = "O"

# call function to print current tile
def print_board(tile):
  for row in tile:
    print(" ".join(row))

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