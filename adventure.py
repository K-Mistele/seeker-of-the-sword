from os import system, listdir
from tile_classes import world_tile
# from local_resources.keyboard_master import keyboard # event listeners for keyboard
from local_resources.colorama_master import colorama  # color library
from time import sleep
from random import randint
from math import ceil, floor
from entity_classes import character, wraith, wyvern, goblin, cyclops, wizard, necromancer, cursed_shadow, chest
from inventory_classes import potion, melee_weapon, consumable
from local_resources import ascii_resources  # ascii art resources
from local_resources.ascii_credits import run_color_credits, run_plain_credits
import platform
from check_high_scores import check_high_scores, print_high_scores # csv high scores system

if platform.system() == "Darwin":  # determining whether system is a mac for compatible modules
    is_mac = True
    print("We have detected you are using a Mac terminal. You may wish to change your background color to black"
          "for a better experience if you enable color mode.")
else:
    is_mac = False
    from local_resources.keyboard_master import keyboard

if platform.system() != "Windows":  # determining whether to use system("cls") or system("clear") to clear screen
    clear_command = "clear"
else:
    clear_command = "cls"


while True:
    with_colors = input("Initiate with colors?\n")
    if "y" in with_colors.lower():
        with_colors = True
        break
    elif "n" in with_colors.lower():
        with_colors = False
        break
    else:
        print("Invalid input!")
        continue
if with_colors:
    colorama.init()

player_character = colorama.Fore.WHITE + "+" if with_colors else "+" # defining player character

play_again = True
game_iteration = 0
while play_again: # game replay loop
    system(clear_command)
    # display splash screen in color or plain
    if with_colors == True:
        #colorama.init()
        print(colorama.Fore.MAGENTA + ascii_resources.color_splash_screen[0] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[1] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[2] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[3] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[4] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[5] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[6] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[7] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[8] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[9] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[10] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[11] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[12] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[13] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[14] +
              colorama.Fore.BLUE + ascii_resources.color_splash_screen[15] +
              colorama.Fore.RED + ascii_resources.color_splash_screen[16] +
              colorama.Fore.GREEN + ascii_resources.color_splash_screen[17] +
              colorama.Fore.WHITE)
        #colorama.deinit()
        sleep(3)
        if game_iteration == 0:
            run_color_credits()
    else:
        print(ascii_resources.plain_splash_screen)
        sleep(3)
        if game_iteration == 0:
            run_plain_credits()

    if with_colors:
        name = input(colorama.Fore.WHITE+"Please enter your name:\n")
        if name.lower() == "hot dog":
            print(colorama.Fore.GREEN + "\nWelcome, [ADMIN]\n")
    else:
        name = input("Please enter your name:\n")
        if "[admin]" in name.lower():
            print("\nWelcome, [ADMIN]\n")

    """Difficulty"""
    difficulty = ""
    while True:
        if with_colors:
            select_difficulty = input(colorama.Fore.WHITE+"Please select difficulty: Normal, Heroic, or True Seeker:\n").lower()
        else:
            select_difficulty = input("Please select difficulty: Normal, Heroic, or True Seeker:\n").lower()
        if select_difficulty in "normal":
            difficulty = "normal"
            player = character(name, 20, 2, 2, 1, 3)  # basic difficulty
            break
        elif select_difficulty in "heroic":
            difficulty = "heroic"
            player = character(name, 20, 2, 2, 1, 2)  # more mobs will spawn
            break
        elif select_difficulty in "true seeker":
            difficulty = "seeker"
            player = character(name, 15, 4, 4, 1, 1)  # lower health, higher damage; more mobs will spawn
            break
        else:
            continue

    while True:  # sanitized getting user input about custom maps
        if with_colors:
            with_custom = input(colorama.Fore.WHITE+"Generate map or use custom?\n").lower()
        else:
            with_custom = input("Generate map or use custom?\n").lower()  # asking user to either generate or use custom map
        if with_custom in "generate" or "generate" in with_custom:
            while True:  # sanitized getting dim
                if with_colors:
                    dim = input(colorama.Fore.WHITE+"Tile dimension?(minimum 16)\n")
                else:
                    dim = input("Tile dimension?(minimum 16)\n")  # getting world dimensions from user
                try:
                    dim = int(dim)
                    if dim < 16:
                        if with_colors:
                            print(colorama.Fore.WHITE+"Tile size too small.")
                        else:
                            print("Tile size too small.")
                        continue
                    break
                except:
                    if with_colors:
                        print(colorama.Fore.WHITE+"Invalid input!")
                    else:
                        print("Invalid input!")
                    continue
            world = world_tile(dim, "world", with_colors, False,"")  # creating "world" object in "table" class with user input
            system(clear_command)  # clearing screen to prepare for game
            break
        elif with_custom in "custom" or "custom" in with_custom:
            dim = 5
            available_files = listdir("custom_maps")  # getting all files in directory that stores maps
            available_maps = []
            for file in available_files:  # only preparing files to display to user that are text files
                if ".txt" in file:
                    available_maps.append(file[:-4])
            if with_colors:
                print(colorama.Fore.WHITE+"\nAvailable maps:")
            else:
                print("\nAvailable maps:")
            for map in available_maps:  # printing maps that the user can choose from
                if with_colors:
                    print(colorama.Fore.WHITE+map)
                else:
                    print(map)
            while True:
                if with_colors:
                    filename = input(colorama.Fore.WHITE+"\nInput name of file to be imported:\n")
                else:
                    filename = input("\nInput name of file to be imported:\n")
                if filename in available_maps:
                    world = world_tile(dim, "world", with_colors, True, filename+".txt")
                    system(clear_command)
                    break
                else:
                    if with_colors:
                        print(colorama.Fore.WHITE+"Invalid file name!")
                    else:
                        print("Invalid file name!")
                    continue
            break
        else:
            if with_colors:
                print(colorama.Fore.WHITE+"Invalid Input!")
            else:
                print("Invalid input!")
            continue
    dim = world.tile_dim

    """Creating effect functions for inventory items"""
    # inventory system
    def speed_potion_effect():
        global with_colors
        player.speed += 1
        moves_until_effect_expires["speed"] += speed_potion.duration
        if with_colors:
            print(colorama.Fore.WHITE+"Invalid Input!")
        else:
            print("You used a speed potion!")


    def lesser_health_effect():
        global with_colors
        if player.health < 20:
            i = 0
            while i < 5:
                if player.health < 20:
                    player.health += 1
                    i += 1
        if with_colors:
            print(colorama.Fore.WHITE+"You used a lesser health potion! \n Health restored to {}!".format(player.health))
        else:
            print("You used a lesser health potion! \n Health restored to {}!".format(player.health))


    def greater_health_effect():
        global with_colors
        if player.health < 20:
            i = 0
            while i < 10:
                if player.health < 20:
                    player.health += 1
                    i += 1
        if with_colors:
            print(colorama.Fore.WHITE+"You used a greater health potion! \n Health restored to {}!".format(player.health))
        else:
            print("You used a greater health potion! \n Health restored to {}!".format(player.health))


    def invisibility_effect():
        global with_colors
        global invisible
        global invisibility_turns
        player.invisible = True
        moves_until_effect_expires["invisibility"] += invisibility_potion.duration
        if with_colors:
            print(colorama.Fore.WHITE+"You used an invisibility potion!")
        else:
            print("You used an invisibility potion!")

    def strength_effect():
        player.damage = player.base_damage * 2
        moves_until_effect_expires["strength"] += strength_potion.duration
        if with_colors:
            print(colorama.Fore.WHITE+"You used a strength potion!")
        else:
            print("You used a strength potion!")

    def tnt_effect():

        if (1 < player_pos[x]+1 < world.tile_dim and 1 < player_pos[y] < world.tile_dim
            and world.char(player_pos[x]+1, player_pos[y]) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]+1, player_pos[y]) in world.tile_elements):
            world.mod_char(player_pos[x]+1, player_pos[y], " ")
        if (1 < player_pos[x]+1 < world.tile_dim and 1 < player_pos[y]+1 < world.tile_dim
            and world.char(player_pos[x] + 1, player_pos[y]+1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]+1, player_pos[y]+1) in world.tile_elements):
            world.mod_char(player_pos[x]+1, player_pos[y]+1, " ")
        if (1 < player_pos[x]+1 < world.tile_dim and 1 < player_pos[y]-1 < world.tile_dim
            and world.char(player_pos[x] + 1, player_pos[y]-1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]+1, player_pos[y]-1) in world.tile_elements):
            world.mod_char(player_pos[x]+1, player_pos[y]-1, " ")
        if (1 < player_pos[x]-1 < world.tile_dim and 1 < player_pos[y] < world.tile_dim
            and world.char(player_pos[x]-1, player_pos[y]) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]-1, player_pos[y]) in world.tile_elements):
            world.mod_char(player_pos[x]-1, player_pos[y], " ")
        if (1 < player_pos[x]-1 < world.tile_dim and 1 < player_pos[y]+1 < world.tile_dim
            and world.char(player_pos[x] - 1, player_pos[y]+1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]-1, player_pos[y]+1) in world.tile_elements):
            world.mod_char(player_pos[x]-1, player_pos[y]+1, " ")
        if (1 < player_pos[x]-1 < world.tile_dim and 1 < player_pos[y]-1 < world.tile_dim
            and world.char(player_pos[x]-1, player_pos[y]-1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x]-1, player_pos[y]-1) in world.tile_elements):
            world.mod_char(player_pos[x]-1, player_pos[y]-1, " ")
        if (1 < player_pos[x] < world.tile_dim and 1 < player_pos[y]+1 < world.tile_dim
            and world.char(player_pos[x], player_pos[y]+1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x], player_pos[y]+1) in world.tile_elements):
            world.mod_char(player_pos[x], player_pos[y]+1, " ")
        if (1 < player_pos[x] < world.tile_dim and 1 < player_pos[y]-1 < world.tile_dim
            and world.char(player_pos[x], player_pos[y]-1) != (colorama.Fore.CYAN + "H" if with_colors else "H")):
            #    and world.char(player_pos[x], player_pos[y]-1) in world.tile_elements):
            world.mod_char(player_pos[x], player_pos[y]-1, " ")
        if with_colors:
            print(colorama.Fore.WHITE+"BOOM!")
        else:
            print("BOOM!")

    def cataclysm_effect():
        for mob in world.monsters:
            world.mod_char(mob.x_index, mob.y_index, mob.stored_char) # remove mosnter symbol from board and restore char
        del world.monsters[:] # kill all monsters in world
        player.health = 0
        if with_colors:
            print(colorama.Fore.WHITE+"Cataclysm activated.")
        else:
            print("Cataclysm activated.")

    """Creating Inventory Items"""

    speed_potion = potion("Speed Potion", int(ceil(dim / 2)), "100", speed_potion_effect, "Speed x2")
    lesser_health_potion = potion("Lesser Health Potion", "instant", "101", lesser_health_effect, "Restores 5 health")
    greater_health_potion = potion("Greater Health Potion", "instant", "102", greater_health_effect, "Restores 10 health")
    invisibility_potion = potion("Invisibility Potion", 10, "103", invisibility_effect, "Become invisible for a short time")
    strength_potion = potion("Strength Potion", int(ceil(dim/3)), "104", strength_effect, "Double your strength for a short time!")
    tnt = consumable("TNT", "201", tnt_effect, "Clears a small area around you. Boom!")
    cataclysm = consumable("The Cataclysm", "202", cataclysm_effect, "WARNING: Kills all life in this world tile. ")
    # global-scope variables
    game_break = False  # creating end condition for game screen loop

    player_inventory = [[speed_potion, 1],
                        [lesser_health_potion, 1],
                        [greater_health_potion, 1],
                        [invisibility_potion, 1],
                        [strength_potion, 1],
                        [tnt, 2]]  # hard-coding a speed potion into the inventory for now
    if "[admin]" in player.name:
        player_inventory.append([cataclysm, 1])
    # speed = 1 # for speed potion; DO NOT SET TO ZERO FOR ANY REASON
    number_of_player_moves = 0  # count of player moves for effect duration
    moves_until_effect_expires = {
        "speed": 0,
        "invisibility": 0,
        "strength": 0
    }

    """Possible items for chest inventories"""
    possible_items = [greater_health_potion, lesser_health_potion, invisibility_potion, strength_potion, tnt]
    # TODO: add chest to world
    world.chests.append(chest(world, possible_items,  False, inventory_size=5)) # larger inventory
    """Generate World, Monsters based on difficulty"""
    def spawn_mobs(difficulty):
        #world = world_tile(dim, "world", with_colors)  # creating "world" object in "table" class with user input
        if difficulty == "normal":
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))):  world.monsters.append(goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 6))):  world.monsters.append(wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 10))): world.monsters.append(cyclops(world, dim, with_colors))
        elif difficulty == "heroic":
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 4))): world.monsters.append(goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))): world.monsters.append(wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 8))): world.monsters.append(cyclops(world, dim, with_colors))
        elif difficulty == "seeker":
            world.monsters.append(wraith(world, dim, with_colors))
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 4))): world.monsters.append(goblin(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 4))): world.monsters.append(wyvern(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 5))): world.monsters.append(cyclops(world, dim, with_colors))
        else:
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))):  world.monsters.append(goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 6))):  world.monsters.append(wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 10))): world.monsters.append(cyclops(world, dim, with_colors))
        if name == "mob test":
            world.monsters.append(wizard(world, dim, with_colors))
            world.monsters.append(necromancer(world, dim, with_colors))
        if world.is_custom == True: # if world is generated --> a dungeon
            for i in range(0, int(ceil(world.tile_dim/16))): # scale number of necromancers and wizards spawned to world
                world.monsters.append(necromancer(world, dim, with_colors))
                world.monsters.append(wizard(world, dim, with_colors))

    spawn_mobs(difficulty)
    system(clear_command)  # clearing screen to prepare for game

    def new_round(difficulty):
        system(clear_command)
        print(colorama.Fore.BLUE + ascii_resources.new_round if with_colors else ascii_resources.new_round)
        sleep(0.2)
        print(colorama.Fore.MAGENTA + ascii_resources.plus_200_points if with_colors else ascii_resources.plus_200_points)
        sleep(1.2)
        spawn_mobs(difficulty)
        return_player_to_origin()
        system(clear_command)



    ### FINDING PLAYER SPAWN POINT ###
    player_pos = [1, 2]  # creating player coordinate storage
    x = 0  # easy access to player position indices
    y = 1

    iter_row = 2
    found = False
    while iter_row <= dim - 1:
        spawn_row = world.row(iter_row)
        iter_character = int(ceil(dim / 3))
        index_counter = iter_character - 1
        for item in spawn_row:
            if iter_character - index_counter < int(ceil(dim / 3)):
                iter_character += 1
                continue
            elif item == " ":
                player_pos[x] = iter_character - index_counter
                found = True
                break
            elif index_counter < dim - 1:
                iter_character += 1
            else:
                break
        if found == True:
            break
        iter_row += 1
        player_pos[y] = iter_row

    world.mod_char(player_pos[x], iter_row, player_character)  # marking origin on map
    origin_point = [player_pos[x], iter_row]
    world.print_tile()  # printing the world for the first time

    """
    functions for motion
    """
    stored_tile = [colorama.Fore.WHITE + "O" if with_colors else "O"]  # stores the tile the player is currently on
    # initial value marks origin

    def reset_pos():  # resets after motion the tile that the player was on
        world.mod_char(player_pos[x], player_pos[y], stored_tile[0])

    def detect_collision(coordinate, direction):
        collision_output = []
        if coordinate == "x":
            for dict_element in world.all_elements:
                if world.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
                    "is_viable"] == False:  # collision
                    collision_output.append(True)
                    collision_output.append(dict_element["name"])
                    collision_output.append(20)
                    return collision_output
                elif world.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
                    "directional"] == True:  # ridges
                    if direction == -1 and dict_element["direction"] == "right":
                        collision_output.append(True)
                        collision_output.append(dict_element["name"])
                        collision_output.append(20)
                        return collision_output
                    elif direction == 1 and dict_element["direction"] == "left":
                        collision_output.append(True)
                        collision_output.append(dict_element["name"])
                        collision_output.append(20)
                        return collision_output
                elif world.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
                    "is_gateway"] == True:  # teleporters
                    collision_output.append(False)
                    collision_output.append(dict_element["name"])
                    collision_output.append(dict_element["gate_id"])
                    return collision_output

            collision_output.append(False)  # no collision
            collision_output.append(None)
            collision_output.append(None)
            return collision_output
            # return False
        elif coordinate == "y":
            for dict_element in world.all_elements:
                if world.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
                    "is_viable"] == False:  # collision
                    collision_output.append(True)
                    collision_output.append(dict_element["name"])
                    collision_output.append(20)
                    return collision_output
                elif world.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
                    "directional"] == True:  # ridges
                    if direction == -1 and dict_element["direction"] == "up":
                        collision_output.append(True)
                        collision_output.append(dict_element["name"])
                        collision_output.append(20)
                        return collision_output
                    elif direction == 1 and dict_element["direction"] == "down":
                        collision_output.append(True)
                        collision_output.append(dict_element["name"])
                        collision_output.append(20)
                        return collision_output
                elif world.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
                    "is_gateway"] == True:  # teleporters
                    collision_output.append(False)
                    collision_output.append(dict_element["name"])
                    collision_output.append(dict_element["gate_id"])
                    return collision_output

            collision_output.append(False)  # no collision
            collision_output.append(None)
            collision_output.append(None)
            return collision_output

    def detect_mob_collision(coordinate, direction):
        mob_collision_output = []
        if coordinate == "x":
            for mob in list(world.monsters):  # iterate over a copy of monsters list
                # if world.char(player_pos[x]+direction,player_pos[y]) == mob.symbol:
                if (mob.x_index == player_pos[x] + direction and
                        mob.y_index == player_pos[y]):

                    mob_collision_output.append(True)
                    name = mob.name
                    mob_collision_output.append(name)
                    mob.health -= player.damage
                    health = mob.health
                    mob_collision_output.append(health)
                    player.score += mob.points
                    if mob.health <= 0:
                        world.mod_char(mob.x_index, mob.y_index, mob.stored_char)  # reset where mob was
                        world.monsters.remove(mob)  # remove mob from original list
                    return mob_collision_output
                    # return True

            mob_collision_output.append(False)
            return mob_collision_output
            # return False
        elif coordinate == "y":
            for mob in list(world.monsters):  # iterate over a copy of monsters list
                # if world.char(player_pos[x],player_pos[y]+direction) == mob.symbol:
                if (mob.x_index == player_pos[x] and  # check based on mob locations not character at that location
                        mob.y_index == player_pos[y] + direction):

                    mob_collision_output.append(True)
                    name = mob.name
                    mob_collision_output.append(name)
                    mob.health -= player.damage
                    health = mob.health
                    mob_collision_output.append(health)
                    player.score += mob.points
                    if mob.health <= 0:
                        world.mod_char(mob.x_index, mob.y_index, mob.stored_char)  # reset where mob was
                        world.monsters.remove(mob)  # remove mob from original list
                    return mob_collision_output
                    # return True

            mob_collision_output.append(False)
            return mob_collision_output

    action_string = ""
    accepted_motions = ["w", "a", "s", "d"]
    def player_move(motion):
        global number_of_player_moves
        global moves_until_effect_expires
        global action_string
        action_string = ""
        number_of_player_moves += 1  # upping the count of player moves by one

        # making speed timer count down
        if player.speed > 1:
            if moves_until_effect_expires["speed"] == 0:
                player.speed -= 1
                action_string += "Speed potion wore off!\n"
            else:
                moves_until_effect_expires["speed"] -= 1
        if player.invisible == True:
            if moves_until_effect_expires["invisibility"] == 0:
                player.invisible = False
                action_string += "Invisibility Potion wore off!\n"
            else:
                moves_until_effect_expires["invisibility"] -= 1
        if player.damage != player.base_damage:
            if moves_until_effect_expires["strength"] == 0:
                player.damage = player.base_damage
                action_string += "Strength Potion wore off!\n"
            else:
                moves_until_effect_expires["strength"] -= 1
        if motion == "w":
            collision_output = detect_collision("y", 1)
            mob_collision_w = detect_mob_collision("y", 1)
            for i in range(0, player.speed):
                if player_pos[y] + 1 > dim - 1 or player_pos[y] + 1 < 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot leave the map!")
                    else:
                        print("You cannot leave the map!")
                    sleep(0.5)
                elif (collision_output[0] == False) and (collision_output[2] in range(0, 10)):
                    cord_1 = 0
                    cord_2 = 1
                    # cord_iter = 0
                    for pair_of_cords in world.gateway_cords[
                        collision_output[2]]:  # checking whether player is moving onto a gateway and then moves them
                        # print(pair_of_cords)
                        # test_var = pair_of_cords
                        if [player_pos[x], player_pos[y] + 1] == world.gateway_cords[collision_output[2]][
                            cord_1]:  # if the location the player is moving onto is the first cord pair
                            # then move the player to the second cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                        elif [player_pos[x], player_pos[y] + 1] == world.gateway_cords[collision_output[2]][
                            cord_2]:  # if the location the player is moving onto is the second cord pair
                            # then move the player to the first cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                elif collision_output[0] == True:
                    # print("Collision detected:")
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                    else:
                        print("You cannot traverse a {}.".format(collision_output[1]))
                    sleep(0.5)
                elif mob_collision_w[0] and len(mob_collision_w) >= 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_w[1], mob_collision_w[2]))
                    else:
                        print("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_w[1], mob_collision_w[2]))
                    sleep(0.5)
                else:
                    reset_pos()  # clears character position and replaces with previous tile
                    del stored_tile[0]
                    player_pos[y] += 1  # moves character location on virtual map
                    stored_tile.append(
                        world.char(player_pos[x], player_pos[y]))  # stores tile that is about to be moved onto
        elif motion == "s":
            collision_output = detect_collision("y", -1)
            mob_collision_s = detect_mob_collision("y", -1)
            for i in range(0, player.speed):
                if player_pos[y] - 1 > dim - 1 or player_pos[y] - 1 < 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot leave the map!")
                    else:
                        print("You cannot leave the map!")
                    sleep(0.5)
                elif (collision_output[0] == False) and (collision_output[2] in range(0, 10)):
                    cord_1 = 0
                    cord_2 = 1
                    # cord_iter = 0
                    for pair_of_cords in world.gateway_cords[
                        collision_output[2]]:  # checking whether player is moving onto a gateway and then moves them
                        # print(pair_of_cords)
                        # test_var = pair_of_cords
                        if [player_pos[x], player_pos[y] - 1] == world.gateway_cords[collision_output[2]][
                            cord_1]:  # if the location the player is moving onto is the first cord pair
                            # then move the player to the second cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                        elif [player_pos[x], player_pos[y] - 1] == world.gateway_cords[collision_output[2]][
                            cord_2]:  # if the location the player is moving onto is the second cord pair
                            # then move the player to the first cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                elif collision_output[0] == True:
                    # print("Collision detected:")
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                    else:
                        print("You cannot traverse a {}.".format(collision_output[1]))
                    sleep(0.5)
                elif mob_collision_s[0] and len(mob_collision_s) >= 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_s[1], mob_collision_s[2]))
                    else:
                        print("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_s[1], mob_collision_s[2]))
                    sleep(0.5)
                else:
                    reset_pos()
                    del stored_tile[0]
                    player_pos[y] -= 1
                    stored_tile.append(world.char(player_pos[x], player_pos[y]))
        elif motion == "a":
            collision_output = detect_collision("x", -1)
            mob_collision_a = detect_mob_collision("x", -1)
            for i in range(0, player.speed):
                if player_pos[x] - 1 > dim - 1 or player_pos[x] - 1 < 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot leave the map!")
                    else:
                        print("You cannot leave the map!")
                    sleep(0.5)
                elif (collision_output[0] == False) and (collision_output[2] in range(0, 10)):
                    cord_1 = 0
                    cord_2 = 1
                    # cord_iter = 0
                    for pair_of_cords in world.gateway_cords[
                        collision_output[2]]:  # checking whether player is moving onto a gateway and then moves them
                        # print(pair_of_cords)
                        # test_var = pair_of_cords
                        if [player_pos[x] - 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                            cord_1]:  # if the location the player is moving onto is the first cord pair
                            # then move the player to the second cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                        elif [player_pos[x] - 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                            cord_2]:  # if the location the player is moving onto is the second cord pair
                            # then move the player to the first cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                elif collision_output[0] == True:
                    # print("Collision detected:")
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                    else:
                        print("You cannot traverse a {}.".format(collision_output[1]))
                    sleep(0.5)
                elif mob_collision_a[0] and len(mob_collision_a) >= 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_a[1], mob_collision_a[2]))
                    else:
                        print("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_a[1], mob_collision_a[2]))
                    sleep(0.5)
                else:
                    reset_pos()
                    del stored_tile[0]
                    player_pos[x] -= 1
                    stored_tile.append(world.char(player_pos[x], player_pos[y]))
        elif motion == "d":
            collision_output = detect_collision("x", 1)
            mob_collision_d = detect_mob_collision("x", 1)
            for i in range(0, player.speed):
                if player_pos[x] + 1 > dim - 1 or player_pos[x] + 1 < 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot leave the map!")
                    else:
                        print("You cannot leave the map!")
                    sleep(0.5)
                elif (collision_output[0] == False) and (collision_output[2] in range(0, 10)):
                    cord_1 = 0
                    cord_2 = 1
                    # cord_iter = 0
                    for pair_of_cords in world.gateway_cords[
                        collision_output[2]]:  # checking whether player is moving onto a gateway and then moves them
                        # print(pair_of_cords)
                        # test_var = pair_of_cords
                        if [player_pos[x] + 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                            cord_1]:  # if the location the player is moving onto is the first cord pair
                            # then move the player to the second cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                        elif [player_pos[x] + 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                            cord_2]:  # if the location the player is moving onto is the second cord pair
                            # then move the player to the first cord pair
                            reset_pos()
                            del stored_tile[0]
                            player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                            player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                            stored_tile.append(world.char(player_pos[x], player_pos[y]))
                            if with_colors:
                                print(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                            else:
                                print("A mysterious gateway transports you elsewhere!")
                            sleep(0.5)
                            break
                elif collision_output[0] == True:
                    # print("Collision detected:")
                    if with_colors:
                        print(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                    else:
                        print("You cannot traverse a {}.".format(collision_output[1]))
                    sleep(0.5)
                elif mob_collision_d[0] and len(mob_collision_d) >= 2:
                    if with_colors:
                        print(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_d[1], mob_collision_d[2]))
                    else:
                        print("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_d[1], mob_collision_d[2]))
                    sleep(0.5)
                else:
                    reset_pos()
                    del stored_tile[0]
                    player_pos[x] += 1
                    stored_tile.append(world.char(player_pos[x], player_pos[y]))

    def randomly_locate_player():
        while True:
            new_x = randint(2, dim - 1)
            new_y = randint(2, dim - 1)
            new_location = world.char(new_x, new_y)
            if new_location == " " or new_location == world.tile_elements[2]["character"]:
                reset_pos()
                del stored_tile[0]
                player_pos[x] = new_x
                player_pos[y] = new_y
                stored_tile.append(world.char(player_pos[x], player_pos[y]))
                world.mod_char(player_pos[x], player_pos[y], player_character)
                break

    def return_player_to_origin(): # origin parameter should be list of [x,y] coordinates for player origin
        reset_pos()
        del stored_tile[0]
        player_pos[x] = origin_point[x]
        player_pos[y] = origin_point[y]
        stored_tile.append(world.char(player_pos[x], player_pos[y]))
        world.mod_char(player_pos[x], player_pos[y], player_character)

    def print_health():
        if "[admin]" not in player.name.lower():
            global with_colors
            healthString = ""
            if with_colors:
                heartString = colorama.Fore.RED + "O" + colorama.Fore.WHITE
            else:
                heartString = "O"
            for i in range(0, player.health):
                if i == 10:
                    healthString = healthString + "\n        {}".format(
                        heartString)  # start a second, aligned row of "hearts" if more than ten health
                else:
                    healthString = healthString + "{}".format(heartString)
            if with_colors:
                print(colorama.Fore.WHITE + "Health: " + "{}".format(healthString))
            else:
                print("Health: {}".format(healthString))
        else:
            return

    while player.lives > 0:

        while True:
            # if all mobs cleared, round system initializes (until story gameplay is built)
            if len(world.monsters) == 0 or (len(world.monsters) == 1 and world.monsters[0].name == "~~Wraith~~"):
                system(clear_command)
                new_round(difficulty)
                world.print_tile()
            sleep(0.1)
            if is_mac == False:
                player_input = keyboard.read_key()
            else:
                player_input = input()

            if player_input in accepted_motions:  # get player input to move on virtual map
                player_move(player_input)
            elif player_input == "z":
                quit() # loop kill switch
            elif player_input == "e":
                system(clear_command)
                if with_colors:
                    print(colorama.Fore.WHITE+"Inventory: \n")
                else:
                    print("Inventory: \n")
                for item in player_inventory:  # display inventory
                    # quantity = item[1]
                    if item[1] > 0:
                        print("   {}: ".format(item[0].name))
                        print(
                        "      Effect: {}\n      Duration: {}\n      Quantity: {}\n".format(item[0].effect_readable,
                        item[0].duration if isinstance(item[0], potion) else "n/a", item[1] ))
                while True:  # inventory system
                    e_input = input("Enter inventory command: ('e' to exit)\n")
                    if e_input == "e":
                        break
                    elif any(item[0].name == e_input for item in player_inventory):  # if there is an item object in player inventory with name input by user
                        for item in player_inventory:  # iterate through and find it
                            if e_input == item[0].name:
                                if item[1] == 0:  # if no more of this item in inventory
                                    print("You are out of this item. ")
                                    break
                                else:
                                    item[1] -= 1  # remove one of the item from inventory
                                    item[0].effect()  # and use its effect
                    else:
                        print("Unrecognized command")
                system(clear_command)
            else:
                print("Invalid key input!")
            world.mod_char(player_pos[x], player_pos[y],player_character)  # stores character location to virtual map
            system(clear_command)  # clears existing map
            world.print_tile()  # prints world (and new character location)

            damage_dealt_by_spikes = False # checking whether player receives damage from world elements during turn
            for element in world.all_elements:
                if element["character"] == stored_tile[0] and element["does_damage"] == True:
                    player.health -= element["damage"]
                    if element["name"] == "spikes":
                        damage_dealt_by_spikes = True
                        break
            print_health()

            print(action_string)
            if damage_dealt_by_spikes == True:
                if with_colors == True:
                    print(colorama.Fore.WHITE + "Spikes underfoot draw " + colorama.Fore.RED + "blood" + colorama.Fore.WHITE + "!")
                else:
                    print("Spikes underfoot draw blood!")
            if stored_tile[0] == world.dungeon_elements[8]["character"]:
                for sign_data in world.sign_info:
                    if [player_pos[x], player_pos[y]] in sign_data:
                        print(colorama.Fore.CYAN + "\nA posted sign reads:" if with_colors else "\nA posted sign reads:")
                        print(colorama.Fore.WHITE + sign_data[world.sign_text] if with_colors else sign_data[world.sign_text])
                        break
            sleep(0.2)
            for mob in world.monsters:
                if not player.invisible:
                    mob.move(player_pos, player)
                    world.mod_char(mob.x_index, mob.y_index, mob.symbol)
            sleep(0.1)
            system(clear_command)
            world.print_tile()
            print_health()
            print(action_string)
            if damage_dealt_by_spikes == True:
                if with_colors == True:
                    print(colorama.Fore.WHITE + "Spikes underfoot draw " + colorama.Fore.RED + "blood" + colorama.Fore.WHITE + "!")
                else:
                    print("Spikes underfoot draw blood!")
            if stored_tile[0] == world.dungeon_elements[8]["character"]:
                for sign_data in world.sign_info:
                    if [player_pos[x], player_pos[y]] in sign_data:
                        print(colorama.Fore.CYAN + "\nA posted sign reads:" if with_colors else "\nA posted sign reads:")
                        print(colorama.Fore.WHITE + sign_data[world.sign_text] if with_colors else sign_data[world.sign_text])
                        break
            if player.health <= 0:
                player.lives -= 1
                if player.lives == 0:
                    system(clear_command)
                    break
                else:
                    player.health = 15 if difficulty == "true seeker" else 20
                    player.lives -= 1
                    system(clear_command)
                    print(colorama.Fore.RED + ascii_resources.lives_left if with_colors else ascii_resources.lives_left)
                    if player.lives == 3:
                        print(colorama.Fore.RED + ascii_resources.three if with_colors else ascii_resources.three)
                    elif player.lives == 2:
                        print(colorama.Fore.RED + ascii_resources.two if with_colors else ascii_resources.two)
                    elif player.lives == 1:
                        print(colorama.Fore.RED + ascii_resources.one if with_colors else ascii_resources.one)
                    else:
                        print(colorama.Fore.RED + ascii_resources.zero if with_colors else ascii_resources.zero)
                    sleep(2)
                    system(clear_command)
                    print(
                        colorama.Fore.MAGENTA + ascii_resources.sword_and_shield if with_colors else ascii_resources.sword_and_shield)
                    sleep(2)
                    print(colorama.Fore.RED + ascii_resources.begin if with_colors else ascii_resources.begin)
                    sleep(2)
                    system(clear_command)
                    #randomly_locate_player()
                    return_player_to_origin() # return player to origin point
                    world.print_tile()

    print(colorama.Fore.RED + ascii_resources.game_over if with_colors else ascii_resources.game_over)
    sleep(3)
    # print(colorama.Fore.MAGENTA + ascii_resources.your_score if with_colors else ascii_resources.your_score)
    player.score += number_of_player_moves
    print(colorama.Fore.MAGENTA + "     Your Score: " + str(player.score) if with_colors else "     Your Score: " + str(
        player.score))
    high_scores = check_high_scores(player.name, player.score, world.tile_dim)
    print_high_scores(high_scores, with_colors)
    sleep(3)
    system(clear_command)
    while True:
        again = input(
            colorama.Fore.BLUE + ascii_resources.play_again + "  " if with_colors else ascii_resources.play_again + "  ")
        if again in "yes":
            play_again = True
            game_iteration += 1
            break
        elif again in "no":
            play_again = False
            break
