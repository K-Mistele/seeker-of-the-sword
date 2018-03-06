from random import randint
from math import sqrt, ceil
from os import system
import platform
from local_modules.colorama_master import colorama
import platform

class world_tile:
    def __init__(self,dim,tile_type,with_colors,is_custom, filename): #creating the table
        self.is_custom = is_custom
        self.with_colors = with_colors
        self.tile = []  # the actual tile that will be created
        if with_colors:
            colorama.init()
        if tile_type == "world":
            self.tile_elements = [{"name": "lake", "character": colorama.Fore.BLUE +"o" if self.with_colors else ".", "is_viable": False},
                                  {"name": "mountain", "character":colorama.Fore.MAGENTA + "M" if self.with_colors else "M", "is_viable": False},
                                  {"name": "forest", "character": colorama.Fore.GREEN + "^" if self.with_colors else "^", "is_viable": True}
                                  ]
            if self.is_custom == False:
                self.tile_dim = dim
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
                self.mod_row(dim, self.tile_elements[1]["character"])
                self.mod_row(1, self.tile_elements[1]["character"])

            elif self.is_custom == True: # creating world if player decides to use a custom map
                custom_map = open("custom_map.txt")
                for line in custom_map: # converting text file to list information that is the world
                    self.tile.append(list(line.strip("\n")))

                if len(self.tile[0]) != len(self.tile): # making sure custom tile is square
                    print("Invalid custom map dimensions: tile must be square!")
                    quit()
                else: # storing dim if the tile is square
                    self.tile_dim = len(self.tile)

                if self.with_colors == True: # updating characters from stored map if game is loaded with colors
                    row_pos = self.tile_dim
                    for row in self.tile:
                        col_pos = 1
                        for character in row:
                            if character == ".":
                                self.mod_char(col_pos,row_pos,self.tile_elements[0]["character"])
                            elif character == "M":
                                self.mod_char(col_pos, row_pos, self.tile_elements[1]["character"])
                            elif character == "^":
                                self.mod_char(col_pos, row_pos, self.tile_elements[2]["character"])
                            elif character == " ":
                                self.mod_char(col_pos,row_pos, " ")
                            else:
                                self.mod_char(col_pos, row_pos, self.tile_elements[1]["character"]) # converting unrecognized characters to mountains
                            col_pos += 1
                        row_pos -= 1




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

