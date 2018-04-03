from inventory_classes import *

#Stores and Manages Player Inventory
class Inventory:
    def __init__(self,effectFunctions,dim):
        # Stores default casses with potion quantity
        # descrition: Class Object stored Here ( NOT INSTANCES)
        self.inventory=[
            [lesser_health_potion, 1],
            [greater_health_potion, 1],
            [tnt, 2],
            [speed_potion,0],
            [invisibility_potion,0],
            [strength_potion,0],
            [cataclysm,0]
        ]

        #assign effects to potions
        for i in range(0, len(self.inventory)):
            self.inventory[i][0] = self.inventory[i][0](effectFunctions[i],dim)


    def use(self,itemName):
        #only use if quantity > 0
        for i in range(0, len(self.inventory)):
            item = self.inventory[i] #store reference
            if item[0].name == itemName and item[1] > 0 :
                self.inventory[i][0].effect() #must access by explicit reference b/c python inconclusive reference collapse
                self.inventory[i][1] -= 1

    def add(self,itemName,quantity=1):
        #only use if quantity > 0
        for i in range(0, len(self.inventory)):
            item = self.inventory[i] #store reference
            if item[0].name == itemName:
                self.inventory[i][1] += quantity #must access by explicit reference b/c python inconclusive reference collapse