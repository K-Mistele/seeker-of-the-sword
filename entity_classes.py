from tile_classes import world_tile
from random import randint
from local_resources.colorama_master import colorama

from math import ceil

class character:
    score = 0
    def __init__(self, name, health, damage, speed, lives):
        self.name = name
        self.health = health
        self.damage = damage
        self.speed = speed
        self.stored_tile = ["O"]
        self.lives = lives
        self.invisible = False


class monster: # for other monsters to inherit

    def __init__(self, world, dim, viable_tiles, symbol, m_range):

        """
        if platform.system() == 'Windows' or platform.system() == "Linux":
            self.with_colors = True
        else:
            self.with_colors = False
            """

        self.damage = 1 # default
        self.moves_this_turn = True
        self.occupied_tile = world
        self.viable_tiles = viable_tiles # default
        # random generation for mob
        self.range = m_range # default range
        while True:
            self.x_index = randint(2, dim - 1) # so mobs don't spawn on world borders
            self.y_index = randint(4, dim - 1) # so mobs don't spawn on world borders, or too close to player
            if world_tile.char(world, self.x_index, self.y_index) in viable_tiles:
                self.stored_char = world_tile.char(world,self.x_index, self.y_index)
                world_tile.mod_char(world, self.x_index, self.y_index, symbol)
                break  # mob has been spawned
            else:
                continue # keep trying until you get a valid x/y combo
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

    def detect_monster_collision_with_world(self, coordinate, direction, target):
        monster_collision = []
        if coordinate == "x":
            if self.occupied_tile.char(self.x_index+direction, self.y_index) not in self.viable_tiles:
                    monster_collision.append(True) # collision detected
                    monster_collision.append(self.occupied_tile.char(self.x_index+direction, self.y_index)) # char collided with
                    if monster_collision[1] == "+" or monster_collision[1] == colorama.Fore.WHITE + "+": # if monster collides with player
                        target.health -= self.damage
                        print("A {} has attacked you!".format(self.name))
            else:
                monster_collision.append(False)
            return monster_collision
        elif coordinate == "y":
            if self.occupied_tile.char(self.x_index, self.y_index+direction) not in self.viable_tiles:
                    monster_collision.append(True) # collision detected
                    monster_collision.append(self.occupied_tile.char(self.x_index, self.y_index+direction)) # char collided with
                    if monster_collision[1] == "+" or monster_collision[1] == colorama.Fore.WHITE + "+": # if monster collides with player
                        target.health -= self.damage
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
            """If farther apart in x than y"""
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

    def __init__(self, world, dim, with_colors):
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

    def __init__(self, world, dim, with_colors):
        self.viable_tiles = [world.tile_elements[0]["character"],
                             world.tile_elements[1]["character"],
                             world.tile_elements[2]["character"],
                             " "]
        self.range = ceil((1/2)*dim) # range is 1/2 the dimension
        self.symbol = colorama.Fore.RED + "%" if with_colors else "%"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range)
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

    def __init__(self, world, dim, with_colors):
        self.viable_tiles = [world.tile_elements[1]["character"],
                             " "]
        self.symbol = colorama.Fore.RED + "$" if with_colors else "$"
        self.range = ceil((1/4)*dim)  # tracking range 1/4 dim
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range)
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

    def __init__(self, world, dim, with_colors):
        self.viable_tiles = [world.tile_elements[2]["character"],
                             " "]
        self.range = ceil((1/5)*dim) # 1/5 tile dimension
        self.symbol = colorama.Fore.RED + "&" if with_colors else "&"
        monster.__init__(self, world, dim, self.viable_tiles, self.symbol, self.range)
        self.health = 8
        self.damage = 2
        self.speed = 1
