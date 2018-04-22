from time import sleep

class CollisionDetector:
    def __init__(self):
        pass
    def detect_collision(self,coordinate,direction,world_instance,player_instance):
        #Detects collision...
        
        #Make Compatable with legacy code .... future code should replace this...!!!
        player_pos = player_instance.exportPosition()
        x = 0
        y=1
        
        collision_output = []
        if coordinate == "x":
            for dict_element in world_instance.all_elements:
                if world_instance.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
                    "is_viable"] == False:  # collision
                    collision_output.append(True)
                    collision_output.append(dict_element["name"])
                    collision_output.append(20)
                    return collision_output
                elif world_instance.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
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
                elif world_instance.char(player_pos[x] + direction, player_pos[y]) == dict_element["character"] and dict_element[
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
            for dict_element in world_instance.all_elements:
                if world_instance.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
                    "is_viable"] == False:  # collision
                    collision_output.append(True)
                    collision_output.append(dict_element["name"])
                    collision_output.append(20)
                    return collision_output
                elif world_instance.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
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
                elif world_instance.char(player_pos[x], player_pos[y] + direction) == dict_element["character"] and dict_element[
                    "is_gateway"] == True:  # teleporters
                    collision_output.append(False)
                    collision_output.append(dict_element["name"])
                    collision_output.append(dict_element["gate_id"])
                    return collision_output

            collision_output.append(False)  # no collision
            collision_output.append(None)
            collision_output.append(None)
            return collision_output
    def detect_mob_collision(self,coordinate,direction,world_instance,player_instance):
        #detect collisions presents numerous problems as it is not just a collision detector but a world updating function
        #any function that updatees the world MUST either run on the adverture.py world instance...
        # depending on how python passes world_instance ==> by reference or value will effect the codes behavior
        # Since this is a single threaded program we can just use the horribly hacky way of redefining the world instance off of the
        # instance passed by value.... the same applies for the player

        #Remove this and refactor accoridingly in the code
        player_pos = player_instance.exportPosition()
        x = 0
        y = 1

        mob_collision_output = []
        if coordinate == "x":
            for mob in list(world_instance.monsters):  # iterate over a copy of monsters list
                # if world.char(player_pos[x]+direction,player_pos[y]) == mob.symbol:
                if (mob.x_index == player_pos[x] + direction and
                        mob.y_index == player_pos[y]):

                    mob_collision_output.append(True)
                    name = mob.name
                    mob_collision_output.append(name)
                    mob.health -= player_instance.damage
                    health = mob.health
                    mob_collision_output.append(health)
                    player_instance.score += mob.points
                    if mob.health <= 0:
                        mob.die()
                    return [mob_collision_output,player_instance,world_instance]
                    # return True

            mob_collision_output.append(False)
            return [mob_collision_output, player_instance, world_instance]
            # return False
        elif coordinate == "y":
            for mob in list(world_instance.monsters):  # iterate over a copy of monsters list
                # if world.char(player_pos[x],player_pos[y]+direction) == mob.symbol:
                if (mob.x_index == player_pos[x] and  # check based on mob locations not character at that location
                        mob.y_index == player_pos[y] + direction):

                    mob_collision_output.append(True)
                    name = mob.name
                    mob_collision_output.append(name)
                    mob.health -= player_instance.damage
                    health = mob.health
                    mob_collision_output.append(health)
                    player_instance.score += mob.points
                    if mob.health <= 0:
                        mob.die()
                    return [mob_collision_output, player_instance, world_instance]
                    # return True

            mob_collision_output.append(False)

            ### THIS FUNCTION NEEDS to be recoded so it does not Modify player or world!!! this is a hack to fix that for now
            return [mob_collision_output,player_instance,world_instance]