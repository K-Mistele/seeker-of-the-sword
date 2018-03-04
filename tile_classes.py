from random import randint
from math import sqrt, ceil
from os import system
import platform
from local_modules.colorama_master import colorama

class world_tile:
    def __init__(self,dim,tile_type,with_colors): #creating the table
        self.with_colors = with_colors
        self.tile_dim = dim
        self.tile = []  # the actual tile that will be created
        if tile_type == "world":
            self.tile_elements = [{"name": "lake", "character":"o" if with_colors else ".", "is_viable": False},
                                  {"name": "mountain", "character":"M", "is_viable": False},
                                  {"name": "forest", "character":"^", "is_viable": True}
                                  ]
            # self.tile_elements = ["M",".","^"]
            for i in range(self.tile_dim): # create the table
                self.tile.append([" "] * self.tile_dim)

            ### RANDOMIZE SOME ELEMENTS IN TABLE ###
            #tile_elements = ["M",".","^"]
            for item in self.tile_elements:
                for number in range(int(sqrt(self.tile_dim)), self.tile_dim+(int(ceil(sqrt(self.tile_dim))/2))): # replace with self.time_dim
                    x = randint(1,self.tile_dim)
                    y = randint(1, self.tile_dim)
                    self.mod_char(x,y,item["character"])
                    ### GROUP RANDOMIZED ELEMENTS TOGETHER SOMEWHAT
                    for num in range(int(sqrt(self.tile_dim))):
                        if (x != 1 and x!= self.tile_dim) and  (y != 1 and y!= self.tile_dim):
                            if randint(0,1) == True:
                                if randint(0,1) == True:
                                    x += 1
                                    self.mod_char(x, y, item["character"])
                                else:
                                    x -= 1
                                    self.mod_char(x, y, item["character"])
                            else:
                                if randint(0,1) == True:
                                    y += 1
                                    self.mod_char(x, y, item["character"])
                                else:
                                    y -= 1
                                    self.mod_char(x, y, item["character"])
            self.mod_col(1, self.tile_elements[1]["character"]) # creating vertical edges of mountains on the world
            self.mod_col(dim, self.tile_elements[1]["character"])
    def print_tile(self,): # printing the tile
        if self.with_colors == True:
            system("color 07")
            colorama.init()
            for row in self.tile:
                for item in row:
                    if item == self.tile_elements[0]["character"]:
                        print(colorama.Fore.BLUE + item, end=" ")
                    elif item == self.tile_elements[1]["character"]:
                        print(colorama.Fore.MAGENTA + item, end=" ")
                    elif item == self.tile_elements[2]["character"]:
                        print(colorama.Fore.GREEN + item,end=" ")
                    elif item == "O":
                        print(colorama.Fore.BLACK + item,end=" ")
                    elif item == "+":
                        print(colorama.Fore.RED + item,end=" ")
                    else:
                        print(colorama.Fore.WHITE + item, end=" ")
                print(" ")
            #colorama.deinit()
        else:
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

