from os import system

dim = int(input("Tile dimension?\n"))
system("clear")

class create_table:
    tile_dim = dim # change me to change world dimensions

    def __init__(self,): #creating the table
        self.tile_dim = self.tile_dim
        self.tile = []  # the actual tile that will be created
        for i in range(self.tile_dim): # create the table
            self.tile.append(["."] * self.tile_dim)

    def print_tile(self,): # printing the tile
        for row in self.tile:
            print(" ".join(row))
        print("\n")

    """
    POSITIONAL FUNCTIONS: RETURN DATA FROM THE TABLE
    """
    def row(self, index): # getting row by index, INDEXED FROM ONE TO DIM
        index = int(index)
        index *= -1
        return self.tile[index]
    def col(self, index): # getting column by index, INDEXED FROM ONE TO DIM
        index = int(index)
        column = []
        for row in self.tile:
            column.append(row[index-1])
        return column
    def char(self, x_index, y_index): # return character by (x,y) coordinates, INDEXED FROM ONE TO DIM
        x_index = int(x_index)
        y_index = int(y_index)
        y_index *= -1
        return self.tile[y_index][x_index-1]

    """
    MODIFICATION FUNCTIONS: MODIFY DATA IN THE TABLE
    """
    def mod_row(self, index, character): # modify all items in a world row to the character
        index = int(index)
        i = 0
        index *= -1
        while i < dim:
            self.tile[index][i] = character
            i += 1
    def mod_col(self, index, character): # modify all items in a world column to the character
        index = int(index)
        i = 0
        while i < dim:
            self.tile[i][index-1] = character
            i += 1
    def mod_char(self, x_index, y_index, character): # modify character at (x_position, y_position) to the character
        x_index = int(x_index)
        y_index = int(y_index)
        y_index *= -1
        self.tile[y_index][x_index-1] = character

world = create_table() # creating "world" object in "table" class

world.mod_char(1,1,"1,1")
world.mod_char(dim,dim,"X")
world.mod_char(1,dim/2,"Y")

world.print_tile()

