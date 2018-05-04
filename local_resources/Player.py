from tile_classes import world_tile
from random import randint
from local_resources.colorama_master import colorama
from inventory_classes import inventory
#This class is to replace the character class for player
# This is a more object oriented apprach...

class Player:
    def __init__(self,name="[default] John",health=20,base_damage=2,damage=2,speed=1,lives=3,origin={"x":0,"y":0}):

        #==== Init Player Properties
        self.score = 0
        self.name = name
        self.speed = speed
        self.stored_tile = ["O"]
        self.character = "+"
        self.lives = lives
        self.invisible = False
        self.health = health
        self.damage = damage
        self.base_damage = base_damage
        self.origin = origin


        #==== Other Player properties
        self.position = origin
        self.colorString = ""
        self.with_colors = False
        self.render_priority=1#Render Priority Depth

        #Player Inventory
        #self.inventory = []
        self.inventory = inventory()
    def setupColor(self,with_colors,colorString):
        if with_colors:
            self.colorString = colorString
            self.with_colors = True
        else:
            self.colorString=""

    # def addToInventory(self,itemInstance):
    #     #     #add a potion or item to players inventory
    #     #     self.inventory.append(itemInstance)

    def updatePosition(self,newX,newY):
        #This assumes the new position is a valid move
        self.position["x"] = newX
        self.position["y"] = newY

    def exportPosition(self):
        #just a small wrapper
        return [self.position["x"],self.position["y"]]

    def exportPlayer(self):
        #This is forthe map to render the player
        return [self.position["x"],self.position["y"],self.colorString+self.character]

    def getHealthString(self):
        #Gets a graphical string representing the health of the player
        if "[admin]" not in self.name.lower():
            healthString = ""
            if self.with_colors:
                heartString = colorama.Fore.RED + "O" + colorama.Fore.WHITE
            else:
                heartString = "O"
            for i in range(0, self.health):
                if i == 10:
                    healthString = healthString + "\n        {}".format(
                        heartString)  # start a second, aligned row of "hearts" if more than ten health
                else:
                    healthString = healthString + "{}".format(heartString)
            if self.with_colors:
                #gameScreen.updateStatus(colorama.Fore.WHITE + "Health: " + "{}".format(healthString))
                    return colorama.Fore.WHITE + "Health: " + "{}".format(healthString)
            else:
                #gameScreen.updateStatus("Health: {}".format(healthString))
                return "Health: {}".format(healthString)
        else:
            return "[Admin Health]"