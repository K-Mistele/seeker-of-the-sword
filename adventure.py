#====== Imports ======
from os import system, listdir
from tile_classes import world_tile
# from local_resources.keyboard_master import keyboard # event listeners for keyboard
from local_resources.colorama_master import colorama  # color library
from time import sleep
from random import randint
from math import ceil, floor
from entity_classes import wraith, wyvern, goblin, cyclops, wizard, necromancer, cursed_shadow, chest #class character was reemoved
from inventory_classes import potion, melee_weapon, consumable
from local_resources import ascii_resources  # ascii art resources
from local_resources.ascii_credits import run_credits
import platform
from check_high_scores import check_high_scores, print_high_scores # csv high scores system

#Refactored Classes added
from local_resources.Screen import Screen
from local_resources.Splash import Splash
from local_resources.GenerateSettings import GenerateSettings
from local_resources.SpawnMobs import SpawnMobs
from local_resources.CollisionDetector import CollisionDetector
from local_resources.Player import Player

'''

# Foreward
+ The code present before the refactor works and is great however maintaining the project is/will
  get increasingly harder given none of the code is split among classes and files, and that it is not using
  quite an object oriented approach...
  Inventory classes will need to be done after the refactor...
  

# Issues to refactoring
+ The mob collision detection updates the world... tempory hack in place to allow refactoring...
+ The function player_move is 300 + lines long... and very repetitive besides the code to accomadate
  refactoring the code incrementally---> support legacy code
+ The player's origin was previously set and reset multiple times before the  game even renders for the first time
  consolidate this as one single update to the players location... currently the players origin is set in the class
  for player... This needs to be reconciled with the other calls

# Refactoring that needs to be done
+ see github issue manager for this branch for extensive list


# Other Notes:
+ The new refactored code makes heavy use of (informally) the python spread operator for function calls
+ If in the context of a coridinate it is always assumed that the 0th item is x, the next y


'''


#============================== Seeker of the Sword ==================================
if __name__ == "__main__":

    #==== Screen Setup ==wwwwwwwws===
    gameScreen = Screen()
    #   gameScreen.clearScreen() to clear the screen in any case...

    #==== Game Settings =====
    gameSettings = GenerateSettings(lightspeed=True)
    if gameSettings.with_colors:
        colorama.init()

    #FOR MIGRATION TO REFACTOR PURPOSES ONLY refactor these uses also
    with_colors = gameSettings.with_colors
    difficulty = gameSettings.difficulty_config[0]

    #==== System Notice ======
    if platform.system() == "Darwin":  # determining whether system is a mac for compatible modules
        is_mac = True
        print("We have detected you are using a Mac terminal. You may wish to change your background color to black"
              "for a better experience if you enable color mode.")
    else:
        is_mac = False
        from local_resources.keyboard_master import keyboard

    #===== Misc. Initilizations ====
    play_again = True
    game_iteration = 0

    #================ Main Game Loop =====================
    while play_again: # game replay loop
        #===== Title Sequence =======
        Splash(with_color=gameSettings.with_colors)
        if game_iteration ==0: #
            run_credits(with_color=gameSettings.with_colors,timeDuration=0) #TIME duration specifies time between prints... 0 for lightspeed

        #===== Init Player =========
        playerSettings = gameSettings.difficulty_config[1:7]
        playerSettings.append({"x":1,"y":2}) #Add the players starting origin to the config
        player = Player(*playerSettings)
        player.setupColor(gameSettings.with_colors,colorama.Fore.WHITE)#manages setting up color for the player

        ## replaces this

        ### FINDING PLAYER SPAWN POINT ###
        player_pos = [1, 2]  # creating player coordinate storage
        x = 0  # easy access to player position indices
        y = 1

        #===== Init World ==========
        world = world_tile(*gameSettings.world_settings) # note the spread operator
        if not gameSettings.world_do_generate: #If the world is not generated its dimension is predefined... update the settings for future use
            gameSettings.dim = world.tile_dim

        #==== Collision Detection Methods ====
        collisionDetector = CollisionDetector()

        """Creating effect functions for inventory items"""
        # inventory system
        def speed_potion_effect():
            global with_colors
            player.speed += 1
            moves_until_effect_expires["speed"] += speed_potion.duration
            if with_colors:
                print(colorama.Fore.WHITE+"You used a speed potion!")
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

        speed_potion = potion("Speed Potion", int(ceil(gameSettings.dim / 2)), "100", speed_potion_effect, "Speed x2")
        lesser_health_potion = potion("Lesser Health Potion", "instant", "101", lesser_health_effect, "Restores 5 health")
        greater_health_potion = potion("Greater Health Potion", "instant", "102", greater_health_effect, "Restores 10 health")
        invisibility_potion = potion("Invisibility Potion", 10, "103", invisibility_effect, "Become invisible for a short time")
        strength_potion = potion("Strength Potion", int(ceil(gameSettings.dim/3)), "104", strength_effect, "Double your strength for a short time!")
        tnt = consumable("TNT", "201", tnt_effect, "Clears a small area around you. Boom!")
        cataclysm = consumable("The Cataclysm", "202", cataclysm_effect, "WARNING: Kills all life in this world tile. ")
        # global-scope variables
        game_break = False  # creating end condition for game screen loop

        player.inventory.items.extend([[lesser_health_potion, 1],
                            [greater_health_potion, 1],
                            [tnt, 2]])  # hard-coding a speed potion into the inventory for now
        if "[admin]" in player.name:
            player.inventory.items.append([cataclysm, 1])
        # speed = 1 # for speed potion; DO NOT SET TO ZERO FOR ANY REASON
        number_of_player_moves = 0  # count of player moves for effect duration
        moves_until_effect_expires = {
            "speed": 0,
            "invisibility": 0,
            "strength": 0
        }

        """Possible items for chest inventories"""
        possible_items = [greater_health_potion, lesser_health_potion, invisibility_potion, strength_potion, speed_potion]

        world.chests.append(chest(world, possible_items,  False, inventory_size=5, max_number_of_items=1)) # larger inventory
        """Generate World, Monsters based on difficulty"""
        def spawn_mobs(difficulty):
            #world = world_tile(dim, "world", with_colors)  # creating "world" object in "table" class with user input
            if difficulty == "normal":
                world.monsters.append(wraith(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 5))):  world.monsters.append(goblin(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 6))):  world.monsters.append(wyvern(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 10))): world.monsters.append(cyclops(world, gameSettings.dim, with_colors))
            elif difficulty == "heroic":
                world.monsters.append(wraith(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 4))): world.monsters.append(goblin(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 5))): world.monsters.append(wyvern(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 8))): world.monsters.append(cyclops(world, gameSettings.dim, with_colors))
            elif difficulty == "seeker":
                world.monsters.append(wraith(world, gameSettings.dim, with_colors))
                world.monsters.append(wraith(world, gameSettings.dim, with_colors))
                for i in range(0, int(ceil(gameSettings.dim / 4))): world.monsters.append(goblin(world, gameSettings.dim, with_colors))
                for i in range(0, int(ceil(gameSettings.dim / 4))): world.monsters.append(wyvern(world, gameSettings.dim, with_colors))
                for i in range(0, int(ceil(gameSettings.dim / 5))): world.monsters.append(cyclops(world, gameSettings.dim, with_colors))
            else:
                world.monsters.append(wraith(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 5))):  world.monsters.append(goblin(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 6))):  world.monsters.append(wyvern(world, gameSettings.dim, with_colors))
                for i in range(0, int(floor(gameSettings.dim / 10))): world.monsters.append(cyclops(world, gameSettings.dim, with_colors))
            if gameSettings.name == "mob test":
                world.monsters.append(wizard(world, gameSettings.dim, with_colors))
                world.monsters.append(necromancer(world, gameSettings.dim, with_colors))
            if world.is_custom == True: # if world is generated --> a dungeon
                for i in range(0, int(ceil(world.tile_dim/16))): # scale number of necromancers and wizards spawned to world
                    world.monsters.append(necromancer(world, gameSettings.dim, with_colors))
                    world.monsters.append(wizard(world, gameSettings.dim, with_colors))
        #=== Spawn Mobs
        #WARNING: make sure world is passed by reference
        SpawnMobs(world,gameSettings.difficulty_config[0],gameSettings.dim,gameSettings.with_colors,gameSettings.name)

        def new_round(difficulty):
            #system(clear_command)
            print(colorama.Fore.BLUE + ascii_resources.new_round if gameSettings.with_colors else ascii_resources.new_round)
            #(0.2)
            print(colorama.Fore.MAGENTA + ascii_resources.plus_200_points if gameSettings.with_colors else ascii_resources.plus_200_points)
           # sleep(1.2)
            spawn_mobs(difficulty)
            return_player_to_origin()
            #system(clear_command)





        iter_row = 2
        found = False
        while iter_row <= gameSettings.dim - 1:
            spawn_row = world.row(iter_row)
            iter_character = int(ceil(gameSettings.dim / 3))
            index_counter = iter_character - 1
            for item in spawn_row:
                if iter_character - index_counter < int(ceil(gameSettings.dim / 3)):
                    iter_character += 1
                    continue
                elif item == " ":
                    player_pos[x] = iter_character - index_counter
                    found = True
                    break
                elif index_counter < gameSettings.dim - 1:
                    iter_character += 1
                else:
                    break
            if found == True:
                break
            iter_row += 1
            player_pos[y] = iter_row

        world.mod_char(*player.exportPlayer())  # markding origin on map
        origin_point = [player_pos[x], iter_row]
        gameScreen.updateWorld(world.print_tile())  # printing the world for the first time
        gameScreen.render()

        """
        functions for motion
        """
        stored_tile = [colorama.Fore.WHITE + "O" if gameSettings.with_colors else "O"]  # stores the tile the player is currently on
        # initial value marks origin

        def reset_pos():  # resets after motion the tile that the player was on
            resetPosSetting = player.exportPosition()
            resetPosSetting.append(stored_tile[0])
            world.mod_char(*resetPosSetting)



        action_string = ""
        accepted_motions = ["w", "a", "s", "d"]


        #dis is a monster function... idk If it can even be refactored
        def player_move(motion):

            #hacky
            global number_of_player_moves
            global moves_until_effect_expires
            global action_string

            #especially hacky
            global player
            global world

            print(player.exportPosition())

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

            #For legacy code support refactor this below!!!!
            player_pos = player.exportPosition()  # ONLY GETS THE POSTION
            x=0
            y=1

            ## REFACTOR: All of these if statements are nearly identical and repetitive
            # consider creating a curried function that generates each case off of an archtype
            # the only thing that changes is the addition or subtraction of the number 1 .... make
            # that a variable and have the code in the if block the main code and the if conditionals change that
            # one number between + and -

            if motion == "w":
                collision_output = collisionDetector.detect_collision("y", 1,world,player)
                collisionUpdates = collisionDetector.detect_mob_collision("y", 1,world,player)

                ### THIS IS A HORRIBLY HACKY way to fix the fact that detect_mob_collisions updates the world.... it does not just detect collisions
                world = collisionUpdates[2]
                player = collisionUpdates[1]
                mob_collision_w =collisionUpdates[0]

                for i in range(0, player.speed):
                    if player_pos[y] + 1 > gameSettings.dim - 1 or player_pos[y] + 1 < 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot leave the map!")
                        else:
                            gameScreen.console("You cannot leave the map!")
                        #sleep(0.5)
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

                                #Update player Position
                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]

                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_2][x],world.gateway_cords[collision_output[2]][cord_2][y])
                                stored_tile.append(world.char(*player.exportPosition()))

                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                               # sleep(0.5)
                                break
                            elif [player_pos[x], player_pos[y] + 1] == world.gateway_cords[collision_output[2]][
                                cord_2]:  # if the location the player is moving onto is the second cord pair
                                # then move the player to the first cord pair
                                reset_pos()
                                del stored_tile[0]
                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_1][x],world.gateway_cords[collision_output[2]][cord_1][y])
                                stored_tile.append(world.char(*player.exportPosition()))

                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                #sleep(0.5)
                                break
                    elif collision_output[0] == True:
                        # print("Collision detected:")
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                        else:
                            gameScreen.console("You cannot traverse a {}.".format(collision_output[1]))
                        #sleep(0.5)
                    elif mob_collision_w[0] and len(mob_collision_w) >= 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_w[1], mob_collision_w[2]))
                        else:
                            gameScreen.console("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_w[1], mob_collision_w[2]))
                        #sleep(0.5)
                    else:
                        reset_pos()  # clears character position and replaces with previous tile
                        del stored_tile[0]

                        oldPlayerPosition = player.exportPosition()
                        player.updatePosition(oldPlayerPosition[0],oldPlayerPosition[1]+1) # moves the player +1 in the y direction
                        stored_tile.append(world.char(*player.exportPosition()))  # stores tile that is about to be moved onto

                        #player_pos[y] += 1  # moves character location on virtual map
                        #stored_tile.append(world.char(player_pos[x], player_pos[y]))  # stores tile that is about to be moved onto
            elif motion == "s":
                collision_output = collisionDetector.detect_collision("y", -1,world,player)
                collisionUpdates = collisionDetector.detect_mob_collision("y", -1,world,player)
                mob_collision_s = collisionUpdates[0]
                world = collisionUpdates[2]
                player = collisionUpdates[1]
                for i in range(0, player.speed):
                    if player_pos[y] - 1 > gameSettings.dim - 1 or player_pos[y] - 1 < 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot leave the map!")
                        else:
                            gameScreen.console("You cannot leave the map!")
                        #sleep(0.5)
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
                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_2][x],world.gateway_cords[collision_output[2]][cord_2][y])
                                stored_tile.append(world.char(*player.exportPosition()))
                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))

                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                            elif [player_pos[x], player_pos[y] - 1] == world.gateway_cords[collision_output[2]][
                                cord_2]:  # if the location the player is moving onto is the second cord pair
                                # then move the player to the first cord pair
                                reset_pos()
                                del stored_tile[0]

                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_1][x],world.gateway_cords[collision_output[2]][cord_1][y])
                                stored_tile.append(world.char(*player.exportPosition()))
                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                    elif collision_output[0] == True:
                        # print("Collision detected:")
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                        else:
                            gameScreen.console("You cannot traverse a {}.".format(collision_output[1]))
                        sleep(0.5)
                    elif mob_collision_s[0] and len(mob_collision_s) >= 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_s[1], mob_collision_s[2]))
                        else:
                            gameScreen.console("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_s[1], mob_collision_s[2]))
                        sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        oldPlayerPosition = player.exportPosition()
                        player.updatePosition(oldPlayerPosition[0],oldPlayerPosition[1] -1)
                        stored_tile.append(world.char(*player.exportPosition()))
                        #player_pos[y] -= 1
                        #stored_tile.append(world.char(player_pos[x], player_pos[y]))
            elif motion == "a":
                collision_output = collisionDetector.detect_collision("x", -1,world,player)
                collisionUpdates = collisionDetector.detect_mob_collision("x", -1,world,player)
                mob_collision_a = collisionUpdates[0]
                player = collisionUpdates[1]
                world = collisionUpdates[2]

                for i in range(0, player.speed):
                    if player_pos[x] - 1 > gameSettings.dim - 1 or player_pos[x] - 1 < 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot leave the map!")
                        else:
                            gameScreen.console("You cannot leave the map!")
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

                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_2][x],world.gateway_cords[collision_output[2]][cord_2][y])
                                stored_tile.append(world.char(*player.exportPosition()))

                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                            elif [player_pos[x] - 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                                cord_2]:  # if the location the player is moving onto is the second cord pair
                                # then move the player to the first cord pair
                                reset_pos()
                                del stored_tile[0]
                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_1][x],world.gateway_cords[collision_output[2]][cord_1][y])
                                stored_tile.append(world.char(*player.exportPosition()))

                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                    elif collision_output[0] == True:
                        # print("Collision detected:")
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                        else:
                            gameScreen.console("You cannot traverse a {}.".format(collision_output[1]))
                        sleep(0.5)
                    elif mob_collision_a[0] and len(mob_collision_a) >= 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_a[1], mob_collision_a[2]))
                        else:
                            gameScreen.console("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_a[1], mob_collision_a[2]))
                        #sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        oldPlayerPosition = player.exportPosition()
                        player.updatePosition(oldPlayerPosition[0]-1,oldPlayerPosition[1])
                        stored_tile.append(world.char(*player.exportPosition()))
                        #player_pos[x] -= 1
                        #stored_tile.append(world.char(player_pos[x], player_pos[y]))
            elif motion == "d":
                collision_output = collisionDetector.detect_collision("x", 1,world,player)
                collisionUpdates = collisionDetector.detect_mob_collision("x", 1,world,player)
                mob_collision_d = collisionUpdates[0]
                player = collisionUpdates[1]
                world = collisionUpdates[2]

                for i in range(0, player.speed):
                    if player_pos[x] + 1 > gameSettings.dim - 1 or player_pos[x] + 1 < 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot leave the map!")
                        else:
                            gameScreen.console("You cannot leave the map!")
                        #sleep(0.5)
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
                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_2][x],world.gateway_cords[collision_output[2]][cord_2][y])
                                stored_tile.append(world.char(*player.exportPosition()))
                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_2][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_2][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                            elif [player_pos[x] + 1, player_pos[y]] == world.gateway_cords[collision_output[2]][
                                cord_2]:  # if the location the player is moving onto is the second cord pair
                                # then move the player to the first cord pair
                                reset_pos()
                                del stored_tile[0]
                                player.updatePosition(world.gateway_cords[collision_output[2]][cord_1][x],world.gateway_cords[collision_output[2]][cord_1][y])
                                stored_tile.append(world.char(*player.exportPosition()))

                                #player_pos[x] = world.gateway_cords[collision_output[2]][cord_1][x]
                                #player_pos[y] = world.gateway_cords[collision_output[2]][cord_1][y]
                                #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                                if with_colors:
                                    gameScreen.console(colorama.Fore.CYAN + "A mysterious gateway transports you elsewhere!"+colorama.Fore.WHITE)
                                else:
                                    gameScreen.console("A mysterious gateway transports you elsewhere!")
                                sleep(0.5)
                                break
                    elif collision_output[0] == True:
                        # print("Collision detected:")
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You cannot traverse a {}.".format(collision_output[1]))
                        else:
                            gameScreen.console("You cannot traverse a {}.".format(collision_output[1]))
                        sleep(0.5)
                    elif mob_collision_d[0] and len(mob_collision_d) >= 2:
                        if with_colors:
                            gameScreen.console(colorama.Fore.WHITE+"You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_d[1], mob_collision_d[2]))
                        else:
                            gameScreen.console("You attacked a {0}! {0}'s health is now {1}!".format(mob_collision_d[1], mob_collision_d[2]))
                        sleep(0.5)
                    else:
                        reset_pos()
                        del stored_tile[0]
                        oldPlayerPosition = player.exportPosition()
                        player.updatePosition(oldPlayerPosition[0] + 1, oldPlayerPosition[1])
                        stored_tile.append(world.char(*player.exportPosition()))
                        #player_pos[x] += 1
                        #stored_tile.append(world.char(player_pos[x], player_pos[y]))

        def randomly_locate_player():
            while True:
                new_x = randint(2, gameSettings.dim - 1)
                new_y = randint(2, gameSettings.dim - 1)
                new_location = world.char(new_x, new_y)
                if new_location == " " or new_location == world.tile_elements[2]["character"]:
                    reset_pos()
                    del stored_tile[0]
                    player.updatePosition(new_x,new_y)
                    stored_tile.append(world.char(*player.exportPosition())) #maybe not computationally efficient.. just put new_x and y
                    #player_pos[x] = new_x
                    #player_pos[y] = new_y
                    #stored_tile.append(world.char(player_pos[x], player_pos[y]))
                    world.mod_char(*player.exportPlayer())
                    break

        def return_player_to_origin(): # origin parameter should be list of [x,y] coordinates for player origin
            reset_pos()
            del stored_tile[0]
            #player_pos[x] = origin_point[x]
            #player_pos[y] = origin_point[y]

            player.updatePosition(origin_point[x],origin_point[y])
            stored_tile.append(world.char(*player.exportPosition()))
            world.mod_char(*player.exportPlayer())



#This section is also repetitive.... besides the legacy support code while refactoring is being done
#This will need to be refactored more deeply

        while player.lives > 0:
            open_chest = True
            while True:
                # if all mobs cleared, round system initializes (until story gameplay is built)
                if len(world.monsters) == 0 or (len(world.monsters) == 1 and world.monsters[0].name == "~~Wraith~~"):
                    #system(clear_command)
                    new_round(difficulty)
                    gameScreen.updateWorld(world.print_tile())
                    gameScreen.render()
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
                    #system(clear_command)
                    if with_colors:
                        print(colorama.Fore.WHITE+"Inventory: \n")
                    else:
                        print("Inventory: \n")
                    for item in player.inventory.items:  # display inventory
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
                        elif any(item[0].name == e_input for item in player.inventory.items):  # if there is an item object in player inventory with name input by user
                            for item in player.inventory.items:  # iterate through and find it
                                if e_input == item[0].name:
                                    if item[1] == 0:  # if no more of this item in inventory
                                        print("You are out of this item. ")
                                        break
                                    else:
                                        item[1] -= 1  # remove one of the item from inventory
                                        item[0].effect()  # and use its effect
                        else:
                            print("Unrecognized command")
                    #system(clear_command)
                else:
                    gameScreen.console("Invalid key input!")
                world.mod_char(*player.exportPlayer())  # stores character location to virtual map
                #system(clear_command)  # clears existing map
                gameScreen.updateWorld(world.print_tile())  # prints world (and new character location)
                gameScreen.render()

                damage_dealt_by_spikes = False # checking whether player receives damage from world elements during turn
                for element in world.all_elements:
                    if element["character"] == stored_tile[0] and element["does_damage"] == True:
                        player.health -= element["damage"]
                        if element["name"] == "spikes":
                            damage_dealt_by_spikes = True
                            break
                gameScreen.updateStatus(player.getHealthString())

                gameScreen.console(action_string)
                if damage_dealt_by_spikes == True:
                    if with_colors == True:
                        gameScreen.console(colorama.Fore.WHITE + "Spikes underfoot draw " + colorama.Fore.RED + "blood" + colorama.Fore.WHITE + "!")
                    else:
                        gameScreen.console("Spikes underfoot draw blood!")
                if stored_tile[0] == world.dungeon_elements[8]["character"]:
                    player_pos = player.exportPosition() #use for now to support legacy code... refactor into it later...
                    x=0
                    y=1
                    for sign_data in world.sign_info:
                        if [player_pos[x], player_pos[y]] in sign_data:
                            gameScreen.console(colorama.Fore.CYAN + "\nA posted sign reads:" if with_colors else "\nA posted sign reads:")
                            gameScreen.console(colorama.Fore.WHITE + sign_data[world.sign_text] if with_colors else sign_data[world.sign_text])
                            break
                sleep(0.2)
                for mob in world.monsters:
                    if not player.invisible:
                        player_pos = player.exportPosition()  # use for now to support legacy code... refactor into it later...
                        x = 0
                        y = 1
                        mob.move(player_pos, player)
                        world.mod_char(mob.x_index, mob.y_index, mob.symbol)
                sleep(0.1)
                #system(clear_command)
                gameScreen.updateWorld(world.print_tile())
                gameScreen.render()
                gameScreen.updateStatus(player.getHealthString())
                gameScreen.console(action_string)
                if damage_dealt_by_spikes == True:
                    if with_colors == True:
                        gameScreen.console(colorama.Fore.WHITE + "Spikes underfoot draw " + colorama.Fore.RED + "blood" + colorama.Fore.WHITE + "!")
                    else:
                        gameScreen.console("Spikes underfoot draw blood!")
                # if player is standing on a sign
                if stored_tile[0] == world.dungeon_elements[8]["character"]:
                    for sign_data in world.sign_info:
                        player_pos = player.exportPosition()  # use for now to support legacy code... refactor into it later...
                        x = 0
                        y = 1
                        if [player_pos[x], player_pos[y]] in sign_data:
                            gameScreen.console(colorama.Fore.CYAN + "\nA posted sign reads:" if with_colors else "\nA posted sign reads:")
                            gameScreen.console(colorama.Fore.WHITE + sign_data[world.sign_text] if with_colors else sign_data[world.sign_text])
                            break

                # if player is standing on a chest
                if stored_tile[0] == (colorama.Fore.CYAN + "H" if with_colors else "H") and open_chest == True:
                    #system(clear_command)
                    gameScreen.console(colorama.Fore.WHITE + "Chest Inventory:\n" if with_colors else "Chest Inventory:\n")
                    for chest in world.chests:
                        player_pos = player.exportPosition()  # use for now to support legacy code... refactor into it later...
                        x = 0
                        y = 1
                        if chest.x_index == player_pos[x] and chest.y_index == player_pos[y]:
                            for item in chest.inventory.items:
                                print("    {}:".format(item[0].name))
                                print("      Effect: {}\n      Duration: {}\n      Quantity: {}\n".format(
                                        item[0].effect_readable,
                                        item[0].duration if isinstance(item[0], potion) else "n/a", item[1]))
                            while True:
                                c_input = input("Transfer Items to inventory?\n")
                                if c_input in "yes":
                                    player.inventory.import_items(chest.inventory)
                                    print("Items transferred to your inventory!")
                                    sleep(1)
                                    break
                                elif c_input in "no":
                                    print("Items not transferred.")
                                    sleep(1)
                                    break
                                else:
                                    continue
                    open_chest = False
                    #system(clear_command)
                    gameScreen.updateWorld(world.print_tile())
                    gameScreen.render()
                else:
                    open_chest = True
                if player.health <= 0:
                    player.lives -= 1
                    if player.lives == 0:
                        #system(clear_command)
                        break
                    else:
                        player.health = 15 if difficulty == "true seeker" else 20
                        player.lives -= 1
                        #system(clear_command)
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
                        #system(clear_command)
                        print(
                            colorama.Fore.MAGENTA + ascii_resources.sword_and_shield if with_colors else ascii_resources.sword_and_shield)
                        sleep(2)
                        print(colorama.Fore.RED + ascii_resources.begin if with_colors else ascii_resources.begin)
                        sleep(2)
                        #system(clear_command)
                        #randomly_locate_player()
                        return_player_to_origin() # return player to origin point
                        gameScreen.updateWorld(world.print_tile())
                        gameScreen.render()

        print(colorama.Fore.RED + ascii_resources.game_over if with_colors else ascii_resources.game_over)
        #sleep(3)
        # print(colorama.Fore.MAGENTA + ascii_resources.your_score if with_colors else ascii_resources.your_score)
        player.score += number_of_player_moves
        print(colorama.Fore.MAGENTA + "     Your Score: " + str(player.score) if with_colors else "     Your Score: " + str(
            player.score))
        high_scores = check_high_scores(player.name, player.score, world.tile_dim)
        print_high_scores(high_scores, with_colors)
        #sleep(3)
        #system(clear_command)
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
