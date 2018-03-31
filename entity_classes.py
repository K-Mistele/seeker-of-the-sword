from tile_classes import world_tile
from random import randint
from local_resources.colorama_master import colorama
from math import ceil, floor

class character:
    score = 0
    def __init__(self, name, health, base_damage, damage, speed, lives):
        self.name = name
        if "[admin]" in self.name.lower() :
            self.health = 100000
            self.damage = 100000
            self.base_damage = 100000
        else:
            self.health = health
            self.damage = damage
            self.base_damage = base_damage
        self.speed = speed
        self.stored_tile = ["O"]
        self.lives = lives
        self.invisible = False

class chest:



    def __init__(self, world, possible_items, location_override=False, location_override_x=0, location_override_y=0,
                 inventory_size=3, generate_items=True, inventory_override=None, ):

        self.world = world
        self.viable_tiles = [" "]
        self.symbol = colorama.Fore.CYAN + "H" if self.world.with_colors else "H"

        # locating chest
        self.location_override = location_override
        if self.location_override:
            # hard-code chest location
            self.x_index = location_override_x
            self.y_index = location_override_y
        else:
            # randomly locate chest
            while True:
                self.x_index = randint(2, self.world.dim - 1) # so mobs don't spawn on world borders
                self.y_index = randint(4, self.world.dim - 1) # so mobs don't spawn on world borders, or too close to player
                if world_tile.char(self.world, self.x_index, self.y_index) in self.viable_tiles:
                    # self.stored_char = world_tile.char(world,self.x_index, self.y_index)
                    world_tile.mod_char(self.world, self.x_index, self.y_index, self.symbol)
                    break  # mob has been spawned
                else:
                    continue # keep trying until you get a valid x/y combo
        self.inventory = []
        self.possible_items = possible_items

        self.generate_items = generate_items
        if inventory_override == None:
            self.inventory_override = []
        else:
            self.inventory_override = inventory_override
        self.inventory_size = int(inventory_size)

        # determine items in chest inventory
        if self.generate_items == True:
            for i in range(0, inventory_size):
                index = randint(0, len(self.possible_items)-1) # select a random item from possible items
                self.inventory.append(self.possible_items[index]) # and add it to the chest's inventory
        else:
            self.inventory.extend(self.inventory_override)


class monster: # for other monsters to inherit

    def __init__(self, world, dim, viable_tiles, symbol, m_range, location_override=False, location_override_x=0, location_override_y=0):

        """
        if platform.system() == 'Windows' or platform.system() == "Linux":
            self.with_colors = True
        else:
            self.with_colors = False
            """
        self.special_condition = eval("False")
        self.attack_range = 1
        self.damage = 1 # default
        self.moves_this_turn = True
        self.occupied_tile = world
        self.viable_tiles = viable_tiles # default
        # random generation for mob
        self.range = m_range # default range
        self.location_override = location_override
        if self.location_override == False:
            while True:
                self.x_index = randint(2, dim - 1) # so mobs don't spawn on world borders
                self.y_index = randint(4, dim - 1) # so mobs don't spawn on world borders, or too close to player
                if world_tile.char(world, self.x_index, self.y_index) in viable_tiles:
                    self.stored_char = world_tile.char(world,self.x_index, self.y_index)
                    world_tile.mod_char(world, self.x_index, self.y_index, symbol)
                    break  # mob has been spawned
                else:
                    continue # keep trying until you get a valid x/y combo
        elif self.location_override == True:
            self.x_index = location_override_x
            self.y_index = location_override_y
            self.stored_char = world_tile.char(world, self.x_index, self.y_index)
            world_tile.mod_char(world, self.x_index, self.y_index, symbol)
    """Detects if will cause mob to collide with another mob"""
    def does_mob_overlap(self, world, x_coord, y_coord): # coordinates should be a pair [x, y]
        mob_overlap_output = []
        for mob in world.monsters:
            if (mob.x_index == x_coord and
                mob.y_index == y_coord):
                mob_overlap_output.append(True)
                mob_overlap_output.append("Target: {} at coordinates [{}, {}]".format(mob.name, mob.x_index, mob.y_index))
                return mob_overlap_output
        mob_overlap_output.append(False)
        return mob_overlap_output

    def reset_monster_pos(self): # reset the tile where the monster was
        world_tile.mod_char(self.occupied_tile, self.x_index, self.y_index, self.stored_char)

    def detect_monster_collision_with_world(self, coordinate, direction, target, targeting=True):
        monster_collision = []
        if coordinate == "x":
            if self.occupied_tile.char(self.x_index+direction, self.y_index) not in self.viable_tiles:
                    monster_collision.append(True) # collision detected
                    monster_collision.append(self.occupied_tile.char(self.x_index+direction, self.y_index)) # char collided with
                    if targeting:
                        if monster_collision[1] == "+" or monster_collision[1] == colorama.Fore.WHITE + "+": # if monster collides with player
                            target.health -= self.damage
                            if self.with_colors:
                                print(colorama.Fore.RED+"A {} has attacked you!".format(self.name))
                            else:
                                print("A {} has attacked you!".format(self.name))
            else:
                monster_collision.append(False)
            return monster_collision
        elif coordinate == "y":
            if self.occupied_tile.char(self.x_index, self.y_index+direction) not in self.viable_tiles:
                    monster_collision.append(True) # collision detected
                    monster_collision.append(self.occupied_tile.char(self.x_index, self.y_index+direction)) # char collided with
                    if targeting:
                        if monster_collision[1] == "+" or monster_collision[1] == colorama.Fore.WHITE + "+": # if monster collides with player
                            target.health -= self.damage
                            if self.with_colors:
                                print(colorama.Fore.RED+"A {} has attacked you!".format(self.name))
                            else:
                                print("A {} has attacked you!".format(self.name))
            else:
                monster_collision.append(False)
            return monster_collision

    def move(self, player_coords, player):
        if self.name == "~~Wraith~~": # if a wraith
            self.moves_this_turn = not(self.moves_this_turn)
            if self.moves_this_turn:
                self.chase(player_coords, player)
        else: # if not a wraith
            self.chase(player_coords, player)

    """
    Chase() makes monsters move towards player
    """

    def chase(self, player_coords, player): # equivalent of player move function for monsters

        player_x = player_coords[0]
        player_y = player_coords[1]
        if abs(self.x_index - player_x) < self.range or abs(self.y_index - player_y) < self.range: # if player within range

            # wizard's range attack
            if self.name == "Wizard" and (abs(self.x_index - player_x) <= self.attack_range and abs(self.y_index - player_y) <= self.attack_range):
                player.health -= self.damage
                print(colorama.Fore.RED + "A wizard casts a magic gaffe at you!" if self.with_colors else "A wizard casts a magic gaffe at you!")
                # prevent wizard from moving in too close to player
                if (abs(player_x - self.x_index) <= ceil(self.attack_range/2) and abs( player_y - self.y_index) <= ceil(self.attack_range/2) ):
                    return # abort the function so wizard doesn't move closer

            # necromancer summon attack
            if self.name == "Necromancer":
                self.spawn_cursed_shadow()

                # prevent necromancer from moving within 5 tiles of player
                if (abs(player_x - self.x_index) <= 6 and abs( player_y - self.y_index) <= 6 ):
                    return # abort the function so necromancer doesn't move closer

            # if farther apart in x than y
            if abs(self.x_index - player_x) > abs(self.y_index - player_y):
                # move towards player in x
                if self.x_index > player_x: # if monster is to the right of player
                    if (self.detect_monster_collision_with_world("x", -1, player)[0] == False # if mob does not collide with world
                        and self.does_mob_overlap(self.occupied_tile, self.x_index - 1, self.y_index)[0] == False
                        and not(self.x_index-1 > self.occupied_tile.tile_dim-1 or self.x_index-1 < 2)): # and if mob isn't trying to move onto world boundary
                        self.reset_monster_pos()
                        self.x_index -= 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                else: # if monster is to the left of player
                    if (self.detect_monster_collision_with_world("x", 1, player)[0] == False
                        and self.does_mob_overlap(self.occupied_tile, self.x_index + 1, self.y_index)[0] == False
                        and not (self.x_index+1 > self.occupied_tile.tile_dim-1 or self.x_index+1 < 2)):
                        self.reset_monster_pos()
                        self.x_index += 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                """If farther apart in y than x"""
            elif abs(self.x_index - player_x) < abs(self.y_index - player_y): # if farther apart in y than x
                if self.y_index > player_y: # if monster is above player
                    if (self.detect_monster_collision_with_world("y", -1, player)[0] == False
                        and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index - 1)[0] == False
                        and not(self.y_index-1 > self.occupied_tile.tile_dim-1 or self.y_index-1 < 1)):
                        self.reset_monster_pos()
                        self.y_index -= 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                else: # if monster is below
                    if (self.detect_monster_collision_with_world("y", 1, player)[0] == False
                        and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index + 1)[0] == False
                        and not (self.y_index+1 > self.occupied_tile.tile_dim-1 or self.y_index+1 < 1)):
                        self.reset_monster_pos()
                        self.y_index += 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
            else: # default, when is equidistant from player in x and y
                # move towards player in y
                if self.y_index > player_y: # if monster is above player
                    if (self.detect_monster_collision_with_world("y", -1, player)[0] == False
                        and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index - 1)[0] == False
                        and not(self.y_index-1 > self.occupied_tile.tile_dim-1 or self.y_index-1 < 1)):
                        self.reset_monster_pos()
                        self.y_index -= 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                else: # if monster is below
                     if (self.detect_monster_collision_with_world("y", 1, player)[0] == False
                        and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index + 1)[0] == False
                        and not (self.y_index+1 > self.occupied_tile.tile_dim-1 or self.y_index+1 < 1)):
                        self.reset_monster_pos()
                        self.y_index += 1
                        self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)

        else: # if player not in range
            """If player isn't in range, this should produce a side-to-side, up-and-down motion where able"""
            # move side to side repeatedly
            if self.x_index % 2 == 0: # move left
                if (self.detect_monster_collision_with_world("x", -1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index - 1, self.y_index)[0] == False
                    and not (self.x_index - 1 > self.occupied_tile.tile_dim - 1 or self.x_index - 1 < 2)):
                    self.reset_monster_pos()
                    self.x_index -= 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("x", 1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index + 1, self.y_index)[0] == False
                    and not (self.x_index + 1 > self.occupied_tile.tile_dim - 1 or self.x_index + 1 < 2)):
                    self.reset_monster_pos()
                    self.x_index += 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("y", -1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index - 1)[0] == False
                    and not(self.y_index-1 > self.occupied_tile.tile_dim-1 or self.y_index-1 < 1)):
                    self.reset_monster_pos()
                    self.y_index -= 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("y", 1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index + 1)[0] == False
                    and not (self.y_index+1 > self.occupied_tile.tile_dim-1 or self.y_index+1 < 1)):
                    self.reset_monster_pos()
                    self.y_index += 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                # otherwise, monster can't move
            else: # try moving right, doing everything in opposite order
                if (self.detect_monster_collision_with_world("x", 1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index + 1, self.y_index)[0] == False
                    and not (self.x_index + 1 > self.occupied_tile.tile_dim - 1 or self.x_index + 1 < 2)):
                    self.reset_monster_pos()
                    self.x_index += 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("x", -1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index - 1, self.y_index)[0] == False
                    and not (self.x_index - 1 > self.occupied_tile.tile_dim - 1 or self.x_index - 1 < 2)):
                    self.reset_monster_pos()
                    self.x_index -= 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("y", 1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index + 1)[0] == False
                    and not (self.y_index+1 > self.occupied_tile.tile_dim-1 or self.y_index+1 < 1)):
                    self.reset_monster_pos()
                    self.y_index += 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)
                elif (self.detect_monster_collision_with_world("y", -1, player)[0] == False
                    and self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index - 1)[0] == False
                    and not(self.y_index-1 > self.occupied_tile.tile_dim-1 or self.y_index-1 < 1)):
                    self.reset_monster_pos()
                    self.y_index -= 1
                    self.stored_char = self.occupied_tile.char(self.x_index, self.y_index)

"""
Wraith Class
"""

# slow moving, invulnerable, high damage
class wraith(monster):

    name = "~~Wraith~~"
    points = 10000

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[1]["character"],
                             world.tile_elements[2]["character"],
                             " "]
        self.with_colors = with_colors
        self.symbol = colorama.Fore.RED + "?" if with_colors else "?"
        self.range = 10000 # functionally unlimited range
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range)
        self.moves_this_turn = False, # should only move once every other turn --> use a `not` toggle
        self.health = 1000000 # large enough that they're functionally invincible
        self.damage = 20 # better not let a wraith get near you, then
        self.speed = 1


"""
Wyvern Class
"""
# low health, low damage
class wyvern(monster):

    name = "Wyvern"
    points = 10

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[0]["character"],
                             world.tile_elements[1]["character"],
                             world.tile_elements[2]["character"],
                             " "]
        self.with_colors = with_colors
        self.range = ceil((1/2)*dim) # range is 1/2 the dimension
        self.symbol = colorama.Fore.RED + "%" if with_colors else "%"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 2
        self.damage = 2
        self.speed = 1


"""
Goblin Class
"""
# medium health, medium damage
class goblin(monster):

    name = "Goblin"
    points = 20

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[1]["character"],
                             " "]
        self.with_colors = with_colors
        self.symbol = colorama.Fore.RED + "$" if with_colors else "$"
        self.range = ceil((1/4)*dim)  # tracking range 1/4 dim
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 3
        self.damage = 3
        self.speed = 1


# high health, low damage
"""
Cyclops Class
"""
class cyclops(monster):

    name = "Cyclops"
    points = 50

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[1]["character"],
                             world.tile_elements[2]["character"]]
        self.with_colors = with_colors
        self.range = ceil((1/5)*dim) # 1/5 tile dimension
        self.symbol = colorama.Fore.RED + "&" if with_colors else "&"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 8
        self.damage = 2
        self.speed = 1

"""
Wizard Class
"""
class wizard(monster):
    name = "Wizard"
    points = 40

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[2],
                             world.dungeon_elements[3],
                             world.dungeon_elements[4],
                             world.dungeon_elements[5],
                             world.dungeon_elements[6],
                             world.dungeon_elements[7],
                             " "]
        self.with_colors = with_colors
        self.range = ceil((1/4)*dim) # 1/4 tile dimension
        self.symbol = colorama.Fore.RED + "!" if with_colors else "!"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 3
        self.damage = 1
        self.speed = 1
        self.attack_range = 3

class necromancer(monster):
    name = "Necromancer"
    points = 40

    def __init__(self, world, dim, with_colors, location_override=False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[2],
                             world.dungeon_elements[0],
                             world.dungeon_elements[1],
                             world.dungeon_elements[2],
                             world.dungeon_elements[3],
                             world.dungeon_elements[4],
                             world.dungeon_elements[5],
                             world.dungeon_elements[6],
                             world.dungeon_elements[7],
                             " "]
        self.with_colors = with_colors
        self.range = ceil((1/4)*dim) # 1/4 world dim
        self.symbol = colorama.Fore.RED + "*" if with_colors else "*"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 1
        self.damage = 0 # necromancer's power is its ability to summon imps (skeletons?)
        self.speed = 1
        self.cursed_shadow_counter = 0
        self.necromancer_count = 0
        self.spawn_cooldown = False
        # special method to spawn cursed shadows

    def spawn_cursed_shadow(self):

        # update number of cursed shadows and necromancers in world
        self.cursed_shadow_counter = 0
        self.necromancer_count = 0
        for monster in self.occupied_tile.monsters:
            if monster.name == "Cursed Shadow":
                self.cursed_shadow_counter += 1
            if monster.name == "Necromancer":
                self.necromancer_count += 1

        # make sure there can only be three cursed shadows per necromancer, and a necromancer can only spawn once every other turn
        if floor(self.cursed_shadow_counter / self.necromancer_count) < 3 and self.spawn_cooldown == False:

            # try spawning a cursed shadow if there are empty tiles adjacent to necromancer
            if (self.does_mob_overlap(self.occupied_tile, self.x_index + 1, self.y_index)[0] == False and
                    self.detect_monster_collision_with_world("x", 1, None, targeting=False)[0] == False):
                self.occupied_tile.monsters.append(
                    cursed_shadow(self.occupied_tile, self.occupied_tile.tile_dim, self.with_colors, True,
                                  self.x_index + 1, self.y_index))
                self.spawn_cooldown = True
                print(colorama.Fore.RED + "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!" if self.with_colors else "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!")

            elif (self.does_mob_overlap(self.occupied_tile, self.x_index - 1, self.y_index)[0] == False and
                    self.detect_monster_collision_with_world("x", -1, None, targeting=False)[0] == False):
                self.occupied_tile.monsters.append(
                    cursed_shadow(self.occupied_tile, self.occupied_tile.tile_dim, self.with_colors, True,
                                  self.x_index - 1, self.y_index))
                self.spawn_cooldown = True
                print(colorama.Fore.RED + "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!" if self.with_colors else "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!")

            elif (self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index + 1)[0] == False and
                    self.detect_monster_collision_with_world("y", 1, None, targeting=False)[0] == False):
                self.occupied_tile.monsters.append(
                    cursed_shadow(self.occupied_tile, self.occupied_tile.tile_dim, self.with_colors, True, self.x_index,
                                  self.y_index + 1))
                self.spawn_cooldown = True
                print(colorama.Fore.RED + "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!" if self.with_colors else "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!")

            elif (self.does_mob_overlap(self.occupied_tile, self.x_index, self.y_index - 1)[0] == False and
                    self.detect_monster_collision_with_world("x", -1, None, targeting=False)[0] == False):
                self.occupied_tile.monsters.append(
                    cursed_shadow(self.occupied_tile, self.occupied_tile.tile_dim, self.with_colors, True, self.x_index,
                                  self.y_index - 1))
                self.spawn_cooldown = True
                print(colorama.Fore.RED + "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!" if self.with_colors else "A Necromancer summons a Cursed Shadow from the Netherworld to pursue you!")

        else:
            self.spawn_cooldown = False


class cursed_shadow(monster): # summoned by necromancers, extraordinarily weak
    name = "Cursed Shadow"
    points = 5

    def __init__(self, world, dim, with_colors, location_override = False, location_override_x=0, location_override_y=0):
        self.viable_tiles = [world.tile_elements[2],
                             world.tile_elements[1],
                             world.dungeon_elements[0],
                             world.dungeon_elements[1],
                             world.dungeon_elements[2],
                             world.dungeon_elements[3],
                             world.dungeon_elements[4],
                             world.dungeon_elements[5],
                             world.dungeon_elements[6],
                             world.dungeon_elements[7],
                             " "]
        self.with_colors = with_colors
        self.range = ceil((1/2)*dim)
        self.symbol = colorama.Fore.RED + "`" if with_colors else "`"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range, location_override, location_override_x, location_override_y)
        self.health = 1
        self.damage = 1
        self.speed = 1
