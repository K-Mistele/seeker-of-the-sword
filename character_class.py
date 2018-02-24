class character:
    def __init__(self, name, health, damage, speed):
        self.name = name
        self.health = health
        self.damage = damage
        self.speed = speed

# slow moving, invulnerable, high damage
class wraith:
    def __init__(self):
        self.moves_this_turn = False, # should only move once every other turn --> use a `not` toggle
        self.health = 1000000 # large enough that they're functionally invincible
        self.damage = 15 # better not let a wraith get near you, then
        self.speed = 1
    symbol = "?" # shared by all wraiths
    name = "~~Wraith~~"

# low health, low damage
class wyvern:
    def __init__(self):
        self.health = 2
        self.damage = 3
        self.speed = 2
    symbol = "%"
    name = "Wyvern"

# medium health, medium damage
class goblin:
    def __init__(self):
        self.health = 4
        self.damage = 4
        self.speed = 1
    symbol = "$"
    name = "Goblin"

# high health, low damage
class cyclops:
    def __init__(self):
        self.health = 8
        self.damage = 2
        self.speed = 1
    symbol = "&"
    name = "Cyclops"