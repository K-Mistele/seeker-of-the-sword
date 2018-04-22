from random import randint

class inventory:
    def __init__(self, size_limit=None, override_items=None, generate_items=False, possible_items=None):
        #TODO: randomly generate contents

        #NOTE: inventory should be format of [[item1, quantitiy], [item2, quantity], ....]

        #size limit
        self.size_limit = size_limit

        self.generate_items=generate_items # Bool for if items are generated

        #if generating items but no size limit, set to default
        if self.generate_items == True and self.size_limit == None:
            self.size_limit = 5 # default size for generating items

       #Determine contents of chest
        if self.generate_items == True and override_items == None: # if generating items
            self.possible_items = possible_items
            for i in range(0, self.size_limit):
                poss_items = self.possible_items[:]
                index = randint(0, len(poss_items)-1)
                self.items.append([poss_items[index],
                                   randint(1, 3)])
                self.possible_items.remove(poss_items[index])

        elif self.generate_items == False and override_items != None: # if overriding items
            self.items = override_items

        else: # if no items
            self.items = []

    # class methods
    def empty_inventory(self):
        self.items = []

    def import_items(self, source_inventory, import_all_items=True, items_to_import=None):
        #NOTE: items_to_import should be list of namesof inventory items to import
        if isinstance(source_inventory, inventory):
            if import_all_items == True: # if importing all items and target has inventory attr
                #TODO: check for if item already exists so you can update quantity
                if len(self.items) == 0: # if own inventory is empty
                    self.items.extend(source_inventory.items)
                else: # if own inventory is not empty
                    # create shallow copies of source and target inventories
                    source_inventory_items = source_inventory.items[:]
                    own_inventory_items = self.items[:]

                    #Separate inventory item from its quantity in a new list
                    source_objects_only = []
                    for item in source_inventory_items:
                        source_objects_only.append(item[0])

                    #separate inventory quantity from its item in a new list
                    source_quants_only = []
                    for item in source_inventory_items:
                        source_quants_only.append(item[1])

                    #separate own inventory item form its quantity in a new list
                    own_objects_only = []
                    for item in own_inventory_items:
                        own_objects_only.append(item[0])

                    #for each item in source inventory
                    for source_object_only in source_objects_only:
                        if source_object_only in own_objects_only: # if source item is already in own inventory
                            index1 = own_objects_only.index(source_object_only) # get index of item
                            index2 = source_objects_only.index(source_object_only) # get index for its proper quantitiy in source_quants_only
                            self.items[index1][1] += source_quants_only[index2] # add quantities together
                        else: # add item and proper quantity to inventory
                            self.items.append([source_object_only, source_quants_only[source_objects_only.index(source_object_only)]])
            #else: TODO: write code for only transferring some items
            source_inventory.empty_inventory()






class potion:
    #TODO: update so quantity is not intrinsic to item
    def __init__(self, name, duration, item_id, effect, effect_readable):
        self.name = name
        self.duration = duration
        self.item_id = item_id
        #self.quantity = quantity
        self.effect = effect
        self.effect_readable = effect_readable

class melee_weapon: #swords, clubs, tridents, ~~MournBlade~~,
    def __init__(self, name, type, damage, ):
        self.name = name
        self.type = type
        self.damage = damage
    damage_radius = 1 # for all melee weapons. Might add another class for spears, lances, etc

class consumable: # for consumables that aren't potions e.g. TNT
    def __init__(self, name, item_id, effect, effect_readable):
        self.name = name
        self.item_id = item_id
        #self.quantity = quantity
        self.effect = effect
        self.effect_readable = effect_readable
