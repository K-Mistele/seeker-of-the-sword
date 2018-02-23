# initial version

# creating empty world and loop end
world = []
game_break = False

#change to increase square dimensions (edge lengths) of the world
# world 0-indexed, so world_dim is length but max dim is world_dim-1
world_dim = 5

# tracking player position
# player_pos[0] = horizontal coordinate = x
# player_pos[1] = vertical coordinate = y
player_pos = [int(world_dim/2),int(world_dim/2)]
x = 0
y = 1

# creating the world
for i in range(world_dim):
    world.append(["."]*world_dim)
world[world_dim-1][world_dim-1] = "O"

# call function to print current tile
def print_board(tile):
  for row in tile:
    print(" ".join(row))

# resets player position
def reset_pos():
    world[player_pos[1]][player_pos[0]] = "."

# gets input to move player via editing player_pos and updating that location with reset_pos
def player_move(motion):
    if motion == "w":
        reset_pos()
        player_pos[y] -= 1
    elif motion == "s":
        reset_pos()
        player_pos[y] += 1
    elif motion == "a":
        reset_pos()
        player_pos[x] -= 1
    elif motion == "d":
        reset_pos()
        player_pos[x] += 1

# actually running the game here
# constantly getting user input
while True:
    # defining player on world map as "X" based on player cords
    world[player_pos[1]][player_pos[0]] = "X"
    # printing game board with player on it
    print_board(world)
    # moving player
    motion = input()
    if motion == "z":
        break
    else:
        player_move(motion)
    # print indices of player location
    print("abs position")
    print(player_pos)
    # print coordinates
    print("coordinates")
    print("({},{})".format(player_pos[x]+1,player_pos[y]+1))
    print("\n")