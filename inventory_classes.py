class potion:
    def __init__(self, name, duration, item_id, effect, effect_readable):
        self.name = name
        self.duration = duration
        self.item_id = item_id
        #self.quantity = quantity
        self.effect = effect
        self.effect_readable = effect_readable

class consumable: # for consumables that aren't potions e.g. TNT
    def __init__(self, name, item_id, effect, effect_readable):
        self.name = name
        self.item_id = item_id
        #self.quantity = quantity
        self.effect = effect
        self.effect_readable = effect_readable

class weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class melee_weapon(weapon):
    def __init__(self, name, damage, classification, durability, material, enchanted=False, enchantment_effect=None):
        weapon.__init__(self, name, damage)
        self.classification = classification
        self.durability = durability
        self.material=material
        self.is_enchanted = enchanted
        if self.is_enchanted:
            if enchantment_effect == None:
                #TODO: randomly pick an enchantment for the weapon
                print() # placeholder
            else:
                self.enchantment_effect = enchantment_effect

class ranged_weapon(weapon):
    def __init__(self, name, damage, classification,  durability, material, enchanted=False, enchantment_effect=None):
        weapon.__init__(self, name, damage)
        self.durability = durability
        self.material = material

        # determine classification, type of ammo used
        self.classification = classification
        if self.classification == "bow":
            self.ammo_used = "arrow"
        elif self.classification == "sling":
            self.ammo_used = "sling stone"
        elif self.classification == "gun":
            self.ammo_used = "shot"
        elif self.classification == "RPG": # for admins only :D
            self.ammo_used = "missile"
        else:
            self.ammo_used = "arrow" # default
        self.is_enchanted = enchanted
        if self.is_enchanted:
            if enchantment_effect == None:
                #TODO: randomly pick enchantment for the weapon
                print() # placeholder
            else:
                self.enchantment_effect = enchantment_effect

class ranged_ammo():
    def __init__(self, classification, damage, material):
        self.classification = classification
        self.damage = damage
        self.material = material