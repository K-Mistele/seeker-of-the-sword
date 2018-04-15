#Imports
from math import ceil, floor
from entity_classes import wraith, wyvern, goblin, cyclops, wizard, necromancer, cursed_shadow, chest

#A class that spawns mobs
class SpawnMobs:
    def __init__(self,world,difficulty,dim,with_colors,name):
        # world = world_tile(dim, "world", with_colors)  # creating "world" object in "table" class with user input
        if difficulty == "normal":
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))):  world.monsters.append(
                goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 6))):  world.monsters.append(
                wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 10))): world.monsters.append(
                cyclops(world, dim, with_colors))
        elif difficulty == "heroic":
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 4))): world.monsters.append(
                goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))): world.monsters.append(
                wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 8))): world.monsters.append(
                cyclops(world, dim, with_colors))
        elif difficulty == "seeker":
            world.monsters.append(wraith(world, dim, with_colors))
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 4))): world.monsters.append(
                goblin(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 4))): world.monsters.append(
                wyvern(world, dim, with_colors))
            for i in range(0, int(ceil(dim / 5))): world.monsters.append(
                cyclops(world, dim, with_colors))
        else:
            world.monsters.append(wraith(world, dim, with_colors))
            for i in range(0, int(floor(dim / 5))):  world.monsters.append(
                goblin(world, dim, with_colors))
            for i in range(0, int(floor(dim / 6))):  world.monsters.append(
                wyvern(world, dim, with_colors))
            for i in range(0, int(floor(dim / 10))): world.monsters.append(
                cyclops(world, dim, with_colors))
        if name == "mob test":
            world.monsters.append(wizard(world, dim, with_colors))
            world.monsters.append(necromancer(world, dim, with_colors))
        if world.is_custom == True:  # if world is generated --> a dungeon
            for i in range(0,
                           int(ceil(world.tile_dim / 16))):  # scale number of necromancers and wizards spawned to world
                world.monsters.append(necromancer(world, dim, with_colors))
                world.monsters.append(wizard(world, dim, with_colors))