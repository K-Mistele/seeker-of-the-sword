from os import system

dim = int(input("Tile dimension?\n"))
system("clear")

class table:
    tile_dim = dim # change me to change world dimensions

    def __init__(self,): #creating the table
        self.tile_dim = self.tile_dim
        self.tile = []  # the actual tile that will be created
        for i in range(self.tile_dim): # create the table
            self.tile.append(["."] * self.tile_dim)

    def print_tile(self,): # printing the tile
        for row in self.tile:
            print(" ".join(row))

    def row(self, index): # getting row by index, INDEXED FROM ONE TO DIM
        return self.tile[index-1]

    def col(self, index): # getting column by index, INDEXED FROM ONE TO DIM
        column = []
        for row in self.tile:
            column.append(row[index-1])
        return column

    def mod_row(self, index, character): # modify all items in a world row to the character
        i = 0
        while i < dim:
            self.tile[index-1][i] = character
            i += 1

    def mod_col(self, index, character): # modify all items in a world column to the character
        i = 0
        while i < dim:
            self.tile[i][index-1] = character
            i += 1


world = table() # creating "world" object in "table" class
print(world.tile)
world.print_tile()

world.tile[0][0] = "1,1"
world.tile[world.tile_dim-1][world.tile_dim-1] = "{},{}".format(dim,dim)

print(world.tile)
world.print_tile()

"""  ### FOR DEBUGGING AND TESTING 'row', 'col', 'mod_row', and 'mod_col' METHODS ###
print("Rows:")
print(world.row(1))
print(world.row(dim))
print("\n")

print("Columns:")
print(world.col(1))
print(world.col(dim))
print("\n")

print("Modded row:")
world.mod_row(2,"K")
world.print_tile()
print("\n")

print("Modded column:")
world.mod_col(2,"P")
world.print_tile()
"""