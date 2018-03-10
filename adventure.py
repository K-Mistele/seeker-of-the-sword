from os import system
from tile_classes import world_tile
from local_resources.keyboard_master import keyboard # event listeners for keyboard
from local_resources.colorama_master import colorama # color library
from time import sleep
from math import ceil, floor
from entity_classes import character, wraith, wyvern, goblin, cyclops
from inventory_classes import potion
from local_resources import ascii_resources # ascii art resources
from local_resources.ascii_credits import run_color_credits, run_plain_credits
import platform

play_again = True
game_iteration = 0
while play_again:
    system("cls")
    # display splash screen in color or plain
    if platform.system() == "Windows" or platform.system() == "Linux":
        colorama.init()
        print(colorama.Fore.MAGENTA + ascii_resources.color_splash_screen[0] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[1] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[2] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[3] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[4] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[5] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[6] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[7] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[8] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[9] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[10] +
              colorama.Fore.BLUE    + ascii_resources.color_splash_screen[11] +
              colorama.Fore.RED     + ascii_resources.color_splash_screen[12] +
              colorama.Fore.GREEN   + ascii_resources.color_splash_screen[13] +
              colorama.Fore.WHITE)
        colorama.deinit()
        sleep(5)
        if game_iteration == 0:
            run_color_credits()
    else:
        print(ascii_resources.plain_splash_screen)
        sleep(5)
        if game_iteration == 0:
            run_plain_credits()


    dim = int(input("Tile dimension?\n")) # getting world dimensions from user
    name = input("Please enter your name:  ")

    if platform.system() == "Windows"or platform.system() == "Linux":  # option to turn off colors to improve performance
        with_colors = input("Initiate with colors? ")
        if "Y" in with_colors or "y" in with_colors:
            with_colors = True
        else:
            with_colors = False
    else:
        with_colors = False

    """Difficulty"""
    difficulty = ""
    while True:
        select_difficulty = input("Please select difficulty: Normal, Heroic, or True Seeker.  ").lower()
        if select_difficulty in "normal":
            difficulty = "normal"
            player = character(name, 20, 2, 1, 3)  # basic difficulty
            break
        elif select_difficulty in "heroic":
            difficulty = "heroic"
            player = character(name, 20, 2, 1, 2)  # more mobs will spawn
            break
        elif select_difficulty in "true seeker":
            difficulty = "seeker"
            player = character(name, 15, 4, 1, 1)  # lower health, higher damage; more mobs will spawn
            break
        else:
            continue

    # inventory system
    def speed_potion_effect():
        player.speed += 1
        moves_until_effect_expires["speed"] += speed_potion.duration
        print("You used a speed potion!")

    def lesser_health_effect():
        if player.health < 20:
            i = 0
            while i < 5:
                if player.health < 20:
                    player.health += 1
                    i += 1
        print("You used a lesser health potion! \n Health restored to {}!".format( player.health))

    def greater_health_effect():
        if player.health < 20:
            i = 0
            while i < 10:
                if player.health < 20:
                    player.health += 1
                    i += 1
        print("You used a greater health potion! \n Health restored to {}!".format( player.health))


    def invisibility_effect():
        global invisible
        global invisibility_turns
        invisible = True
        moves_until_effect_expires["invisibility"] += invisibility_potion.duration
        print("You used an invisibility potion!")


    speed_potion = potion("Speed Potion", int(ceil(dim/2)), "100", 1, speed_potion_effect, "Speed x2")
    lesser_health_potion = potion("Lesser Health Potion", "instant", "101", 1, lesser_health_effect, "Restores 5 health")
    greater_health_potion = potion("Greater Health Potion", "instant", "102", 1, greater_health_effect, "Restores 10 health")
    invisibility_potion = potion("Invisibility Potion", 10, 103, 1, invisibility_effect, "Become invisible for a short time")



    # global-scope variables
    game_break = False # creating end condition for game screen loop
    player_inventory = [speed_potion, lesser_health_potion, greater_health_potion, invisibility_potion] # hard-coding a speed potion into the inventory for now
    #speed = 1 # for speed potion; DO NOT SET TO ZERO FOR ANY REASON
    number_of_player_moves = 0 # count of player moves for effect duration
    moves_until_effect_expires = {
        "speed": 0,
        "invisibility": 0
    }

    """Generate World, Monsters based on difficulty"""

    world = world_tile(dim, "world", with_colors) # creating "world" object in "table" class with user input
    if difficulty == "normal":
        world.monsters.append(wraith(world, dim, with_colors))
        for i in range(0, int(floor(dim/5))):  world.monsters.append(goblin(world, dim, with_colors))
        for i in range(0, int(floor(dim/6))):  world.monsters.append(wyvern(world, dim, with_colors))
        for i in range(0, int(floor(dim/10))): world.monsters.append(cyclops(world, dim, with_colors))
    elif difficulty == "heroic":
        world.monsters.append(wraith(world, dim, with_colors))
        for i in range(0, int(floor(dim/4))): world.monsters.append(goblin(world, dim, with_colors))
        for i in range(0, int(floor(dim/5))): world.monsters.append(wyvern(world, dim, with_colors))
        for i in range(0, int(floor(dim/8))): world.monsters.append(cyclops(world, dim, with_colors))
    elif difficulty == "seeker":
        world.monsters.append(wraith(world, dim, with_colors))
        world.monsters.append(wraith(world, dim, with_colors))
        for i in range(0, int(ceil(dim/4))): world.monsters.append(goblin(world, dim, with_colors))
        for i in range(0, int(ceil(dim/4))): world.monsters.append(wyvern(world, dim, with_colors))
        for i in range(0, int(ceil(dim/5))): world.monsters.append(cyclops(world, dim, with_colors))
    else:
        world.monsters.append(wraith(world, dim, with_colors))
        for i in range(0, int(floor(dim / 5))):  world.monsters.append(goblin(world, dim, with_colors))
        for i in range(0, int(floor(dim / 6))):  world.monsters.append(wyvern(world, dim, with_colors))
        for i in range(0, int(floor(dim / 10))): world.monsters.append(cyclops(world, dim, with_colors))
    system("cls") # clearing screen to prepare for game

    while player.lives > 0:
        ### FINDING PLAYER SPAWN POINT ###
        player_pos = [1,2] # creating player coordinate storage
        x = 0 # easy access to player position indices
        y = 1
        spawn_row = world.row(2)
        i = int(ceil(dim/3))
        for item in spawn_row: # finding empty space in first row for player to spawn
            if item == " ":
                player_pos[x] = i
                break
            i += 1
        world.mod_char(player_pos[x],2,colorama.Fore.WHITE + "+" if with_colors else "+") # marking origin on map
        world.print_tile() # printing the world for the first time

        """
        functions for motion
        """
        stored_tile = [colorama.Fore.WHITE + "O" if with_colors else "O"] # stores the tile the player is currently on (initial value will mark origin

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

        def detect_mob_collision(coordinate,direction):
            mob_collision_output = []
            if coordinate == "x":
                for mob in list(world.monsters): # iterate over a copy of monsters list
                    #if world.char(player_pos[x]+direction,player_pos[y]) == mob.symbol:
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
                            world.mod_char(mob.x_index, mob.y_index, mob.stored_char)# reset where mob was
                            world.monsters.remove(mob) # remove mob from original list
                        return mob_collision_output
                        #return True

                mob_collision_output.append(False)
                return mob_collision_output
                        #return False
            elif coordinate == "y":
                for mob in list(world.monsters): # iterate over a copy of monsters list
                    #if world.char(player_pos[x],player_pos[y]+direction) == mob.symbol:
                    if (mob.x_index == player_pos[x] and # check based on mob locations not character at that location
                        mob.y_index == player_pos[y] + direction):

                        mob_collision_output.append(True)
                        name = mob.name
                        mob_collision_output.append(name)
                        mob.health -= player.damage
                        health = mob.health
                        mob_collision_output.append(health)
                        player.score += mob.points
                        if mob.health <= 0:
                            world.mod_char(mob.x_index, mob.y_index, mob.stored_char)# reset where mob was
                            world.monsters.remove(mob) # remove mob from original list
                        return mob_collision_output
                        #return True

                mob_collision_output.append(False)
                return mob_collision_output

        accepted_motions = [["w","a","s","d"],["2w","2a","2s","2d"]]
        def player_move(motion):
            global number_of_player_moves
            global moves_until_effect_expires
            number_of_player_moves += 1 # upping the count of player moves by one

            # making speed timer count down
            if player.speed > 1:
                if moves_until_effect_expires["speed"] == 0:
                    player.speed -= 1
                else:
                    moves_until_effect_expires["speed"] -= 1
            # making invisibility potion timer count down
            if player.invisible:
                if moves_until_effect_expires["invisibility"] == 0:
                    player.invisible = False
                else:
                    moves_until_effect_expires["invisibility"] -=1
            if motion == "w":
                mob_collision_w = detect_mob_collision("y", 1)
                for i in range(0, player.speed):
                    if player_pos[y]+1 > dim-1 or player_pos[y]+1 < 1:
                        print("You cannot leave the map!")
                        sleep(0.5)
                    elif detect_collision("y",1)[0] == True:
                        print("Collision detected:")
                        print("You cannot traverse a {}".format(detect_collision("y",1)[1]))
                        sleep(0.5)
                    elif mob_collision_w[0] and len(mob_collision_w) >= 2:
                        print("You attacked a {0}!\n{0}'s health is now {1}!".format(mob_collision_w[1], mob_collision_w[2]))
                        sleep(0.5)
                    else:
                        reset_pos() # clears character position and replaces with previous tile
                        del stored_tile[0]
                        player_pos[y] += 1 # moves character location on virtual map
                        stored_tile.append(world.char(player_pos[x], player_pos[y]))  # stores tile that is about to be moved onto
            elif motion == "s":
                mob_collision_s = detect_mob_collision("y", -1)
                for i in range(0, player.speed):
                    if player_pos[y]-1 > dim-1 or player_pos[y]-1 < 1:
                        print("You cannot leave the map!")
                        sleep(0.5)
                    elif detect_collision("y",-1)[0] == True:
                        print("Collision detected:")
                        print("You cannot traverse a {}".format(detect_collision("y",-1)[1]))
                        sleep(0.5)
                    elif mob_collision_s[0] and len(mob_collision_s) >= 2:
                        print("You attacked a {0}!\n{0}'s health is now {1}!".format(mob_collision_s[1], mob_collision_s[2]))
                        sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        player_pos[y] -= 1
                        stored_tile.append(world.char(player_pos[x], player_pos[y]))
            elif motion == "a":
                mob_collision_a = detect_mob_collision("x", -1)
                for i in range(0, player.speed):
                    if player_pos[x]-1 > dim-1 or player_pos[x]-1 < 2:
                        print("You cannot leave the map!")
                        sleep(0.5)
                    elif detect_collision("x",-1)[0] == True:
                        print("Collision detected:")
                        print("You cannot traverse a {}".format(detect_collision("x",-1)[1]))
                        sleep(0.5)
                    elif mob_collision_a[0] and len(mob_collision_a) >= 2:
                        print("You attacked a {0}!\n{0}'s health is now {1}!".format(mob_collision_a[1], mob_collision_a[2]))
                        sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        player_pos[x] -= 1
                        stored_tile.append(world.char(player_pos[x], player_pos[y]))
            elif motion == "d":
                mob_collision_d = detect_mob_collision("x", 1)
                for i in range(0, player.speed):
                    if player_pos[x]+1 > dim-1 or player_pos[x]+1 < 2:
                        print("You cannot leave the map!")
                        sleep(0.5)
                    elif detect_collision("x",1)[0] == True:
                        print("Collision detected:")
                        print("You cannot traverse a {}".format(detect_collision("x",1)[1]))
                        sleep(0.5)
                    elif mob_collision_d[0] and len(mob_collision_d) >= 2:
                        print("You attacked a {0}!\n{0}'s health is now {1}!".format(mob_collision_d[1], mob_collision_d[2]))
                        sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        player_pos[x] += 1
                        stored_tile.append(world.char(player_pos[x], player_pos[y]))

        def print_health():
            global with_colors
            healthString = ""
            if with_colors:
                heartString = colorama.Fore.RED + "O"
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
                print(colorama.Fore.WHITE + "Coordinates:")
                print(colorama.Fore.WHITE + str(player_pos))
            else:
                print("Health: {}".format(healthString))
                print("Coordinates:")
                print(player_pos)


        while True:
            sleep(0.1)
            player_input = keyboard.read_key()

            if player_input in accepted_motions[0]: # get player input to move on virtual map
                player_move(player_input)
            elif player_input == "z":
                break # loop kill switch
            elif player_input == "e":
                system("cls")
                print("Inventory: \n")
                for item in player_inventory: # display inventory
                    if item.quantity > 0:
                        print("   {}: ".format(item.name))
                        print("      Effect: {}\n      Duration: {}\n      Quantity: {}\n".format(item.effect_readable, item.duration, item.quantity))
                while True: # inventory system
                    e_input = input("Enter inventory command: ('e' to exit)\n")
                    if e_input == "e":
                        break
                    elif any (item.name == e_input for item in player_inventory): # if there is an item object in player inventory with name input by user
                        for item in player_inventory: # iterate through and find it
                            if e_input == item.name:
                                if item.quantity == 0: # if no more of this item in inventory
                                    print("You are out of this item. ")
                                    break
                                else:
                                    item.quantity -=1 # remove one of the item from inventory
                                    item.effect() # and use its effect
                    else:
                        print("Unrecognized command")
                system("cls")
            else:
                print("Invalid key input!")
            world.mod_char(player_pos[x], player_pos[y], colorama.Fore.WHITE + "+"if with_colors else "+") # stores character location to virtual map
            system("cls") # clears existing map
            world.print_tile() #prints world (and new character location)
            print_health()
            sleep(0.2)
            for mob in world.monsters:
                if not player.invisible:
                    mob.move(player_pos, player)
                    world.mod_char(mob.x_index, mob.y_index, mob.symbol)
            system("cls")
            world.print_tile()
            print_health()
            if player.health <= 0:
                if player.lives == 0:
                    system("cls")
                    break
                else:
                    player.health = 15 if difficulty == "heroic" else 20
                    player.lives -= 1
                    system("cls")
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
                    system("cls")

    print(colorama.Fore.RED + ascii_resources.game_over if with_colors else ascii_resources.game_over)
    sleep(3)
    #print(colorama.Fore.MAGENTA + ascii_resources.your_score if with_colors else ascii_resources.your_score)
    print(colorama.Fore.MAGENTA + "     Your Score: " + str(player.score) if with_colors else "     Your Score: " + str(player.score))
    sleep(3)
    system("cls")
    while True:
        again = input(colorama.Fore.BLUE + ascii_resources.play_again + "  " if with_colors else ascii_resources.play_again + "  ")
        if again in "yes":
            play_again = True
            game_iteration += 1
            break
        elif again in "no":
            play_again = False
            break

