class potion:
    def __init__(self, name, duration, item_id, quantity, effect, effect_readable):
        self.name = name
        self.duration = duration
        self.item_id = item_id
        self.quantity = quantity
        self.effect = effect
        self.effect_readable = effect_readable

class melee_weapon: #swords, clubs, tridents, ~~MournBlade~~,
    def __init__(self, name, type, damage, ):
        self.name = name
        self.type = type
        self.damage = damage
    damage_radius = 1 # for all melee weapons. Might add another class for spears, lances, etc
