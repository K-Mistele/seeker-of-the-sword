from math import ceil

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

# =========================== Different Types of Potions =============================

class speed_potion(potion):
    def __init__(self,speed_potion_effect,dim):
        potion.__init__(self,"Speed Potion", int(ceil(dim / 2)), "100", speed_potion_effect, "Speed x2")

class lesser_health_potion(potion):
    def __int__(self,lesser_health_effect,dim):
        potion.__init__(self,"Lesser Health Potion", "instant", "101", lesser_health_effect, "Restores 5 health")

class greater_health_potion(potion):
    def __init__(self,greater_health_effect,dim):
        potion.__init__(self,"Greater Health Potion", "instant", "102", greater_health_effect, "Restores 10 health")

class invisibility_potion(potion):
    def __init__(self,invisibility_effect,dim):
        potion.__init__(self,"Invisibility Potion", 10, "103", invisibility_effect, "Become invisible for a short time")

class strength_potion(potion):
    def __init(self,strength_effect,dim):
        potion.__init__(self,"Strength Potion", int(ceil(dim/3)), "104", strength_effect, "Double your strength for a short time!")

# =========================== Different Types of consumables =============================

class tnt(consumable):
    def __int__(self,tnt_effect,dim):
        consumable.__init__(self,"TNT", "201", tnt_effect, "Clears a small area around you. Boom!")

class cataclysm(consumable):
    def __int__(self, cataclysm_effect,dim):
        consumable.__init__(self,"The Cataclysm", "202", cataclysm_effect, "WARNING: Kills all life in this world tile. ")