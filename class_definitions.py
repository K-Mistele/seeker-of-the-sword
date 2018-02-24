from random import randint
from math import sqrt, ceil

class create_table:
    def __init__(self,dim): #creating the table
        self.tile_dim = dim
        self.tile = []  # the actual tile that will be created
        self.tile_elements = ["M",".","^"]
        for i in range(self.tile_dim): # create the table
            self.tile.append([" "] * self.tile_dim)

        ### RANDOMIZE SOME ELEMENTS IN TABLE ###
        #tile_elements = ["M",".","^"]
        for item in self.tile_elements:
            for number in range(int(sqrt(self.tile_dim)), self.tile_dim+(int(ceil(sqrt(self.tile_dim))/2))): # replace with self.time_dim
                x = randint(1,self.tile_dim)
                y = randint(1, self.tile_dim)
                self.mod_char(x,y,item)
                ### GROUP RANDOMIZED ELEMENTS TOGETHER SOMEWHAT
                for num in range(int(sqrt(self.tile_dim))):
                    if (x != 1 and x!= self.tile_dim) and  (y != 1 and y!= self.tile_dim):
                        if randint(0,1) == True:
                            if randint(0,1) == True:
                                x += 1
                                self.mod_char(x, y, item)
                            else:
                                x -= 1
                                self.mod_char(x, y, item)
                        else:
                            if randint(0,1) == True:
                                y += 1
                                self.mod_char(x, y, item)
                            else:
                                y -= 1
                                self.mod_char(x, y, item)
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
        while i < self.tile_dim:
            self.tile[index][i] = character
            i += 1
    def mod_col(self, index, character): # modify all items in a world column to the character
        index = int(index)
        i = 0
        while i < self.tile_dim:
            self.tile[i][index-1] = character
            i += 1
    def mod_char(self, x_index, y_index, character): # modify character at (x_position, y_position) to the character
        x_index = int(x_index)
        y_index = int(y_index)
        y_index *= -1
        self.tile[y_index][x_index-1] = character

