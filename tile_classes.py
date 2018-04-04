from random import randint
from math import sqrt, ceil

from local_resources.colorama_master import colorama


class world_tile:
    def __init__(self,dim,tile_type,with_colors,is_custom, filename, default_chests=None): #creating the table,
        # chests should be a list if there are hardcoded chests
        self.is_custom = is_custom
        self.with_colors = with_colors
        self.tile = []  # the actual tile that will be created
        self.monsters = []
        # chests
        if default_chests == None:
            self.chests = [] # by default an empty list, can append to
        else:
            self.chests = default_chests
        if with_colors:
            colorama.init()
        if tile_type == "world":
            self.tile_elements = [
                {"name": "lake", "character": colorama.Fore.BLUE + "o" if self.with_colors else ".",
                 "is_viable": False, "does_damage": False, "directional": False, "is_gateway": False},
                {"name": "mountain", "character": colorama.Fore.MAGENTA + "M" if self.with_colors else "M",
                 "is_viable": False, "does_damage": False, "directional": False, "is_gateway": False},
                {"name": "forest", "character": colorama.Fore.GREEN + "f" if self.with_colors else "f",
                 "is_viable": True, "does_damage": False, "directional": False, "is_gateway": False}
                ]
            self.dungeon_elements = [
                {"name": "vertical wall", "character": colorama.Fore.YELLOW + "|" if self.with_colors else "|",
                 "is_viable": False, "does_damage": False, "directional": False, "is_gateway": False},
                {"name": "horizontal wall", "character": colorama.Fore.YELLOW + "-" if self.with_colors else "-",
                 "is_viable": False, "does_damage": False, "directional": False, "is_gateway": False},
                {"name": "structure", "character": colorama.Fore.WHITE + "□" if self.with_colors else "□",
                 "is_viable": False, "does_damage": False, "directional": False, "is_gateway": False},
                {"name": "spikes", "character": colorama.Fore.RED + "w" if self.with_colors else "w",
                 "is_viable": True, "does_damage": True, "directional": False, "is_gateway": False, "damage": 1},
                {"name": "left ridge", "character": colorama.Fore.YELLOW + "<" if self.with_colors else "<",
                 "is_viable": True, "does_damage": False, "directional": True, "direction": "left","is_gateway": False},
                {"name": "right ridge", "character": colorama.Fore.YELLOW + ">" if self.with_colors else ">",
                 "is_viable": True, "does_damage": False, "directional": True, "direction": "right","is_gateway": False},
                {"name": "down ridge", "character": colorama.Fore.YELLOW + "v" if self.with_colors else "v",
                 "is_viable": True, "does_damage": False, "directional": True, "direction": "down","is_gateway": False},
                {"name": "up ridge", "character": colorama.Fore.YELLOW + "^" if self.with_colors else "^",
                 "is_viable": True, "does_damage": False, "directional": True, "direction": "up","is_gateway": False},
                {"name": "sign", "character": colorama.Fore.CYAN + "T" if self.with_colors else "T",
                 "is_viable": True, "does_damage": False, "directional": False, "is_gateway": False}
                ]
            self.gateway_elements = [
                {"name": "gateway 1", "character": colorama.Fore.CYAN + "1" if self.with_colors else "1",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 0, "is_gateway": True},
                {"name": "gateway 2", "character": colorama.Fore.CYAN + "2" if self.with_colors else "2",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 1, "is_gateway": True},
                {"name": "gateway 3", "character": colorama.Fore.CYAN + "3" if self.with_colors else "3",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 2, "is_gateway": True},
                {"name": "gateway 4", "character": colorama.Fore.CYAN + "4" if self.with_colors else "4",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 3, "is_gateway": True},
                {"name": "gateway 5", "character": colorama.Fore.CYAN + "5" if self.with_colors else "5",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 4, "is_gateway": True},
                {"name": "gateway 6", "character": colorama.Fore.CYAN + "6" if self.with_colors else "6",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 5, "is_gateway": True},
                {"name": "gateway 7", "character": colorama.Fore.CYAN + "7" if self.with_colors else "7",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 6, "is_gateway": True},
                {"name": "gateway 8", "character": colorama.Fore.CYAN + "8" if self.with_colors else "8",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 7, "is_gateway": True},
                {"name": "gateway 9", "character": colorama.Fore.CYAN + "8" if self.with_colors else "9",
                 "is_viable": True, "does_damage": False, "directional": False, "gate_id": 8, "is_gateway": True}
                ]
            self.all_elements = self.tile_elements + self.dungeon_elements + self.gateway_elements
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


            elif self.is_custom == True:  # creating world if player decides to use a custom map
                self.sign_info = []
                self.sign_text = 0
                self.sign_cords = 1
                custom_map_with_signs = open("custom_maps/" + filename)
                line_1 = custom_map_with_signs.readline()
                if "signs=" in line_1:
                    line_1 = line_1.strip("signs=\n")
                    sign_count = int(line_1)
                    for line in range(sign_count):
                        self.sign_info.append([custom_map_with_signs.readline()])

                custom_map = open("custom_maps/" + filename)
                for line in range(sign_count + 1):  # stripping lines with sign information on them so the square map checker works
                    custom_map.readline()
                for line in custom_map:  # converting text file to list information that is the world
                    self.tile.append(list(line.strip("\n")))

                any_long_line = False
                for line in self.tile:
                    if len(line) != len(self.tile):
                        any_long_line = True
                        break
                if any_long_line == True:  # making sure custom tile is square
                    print("Invalid custom map dimensions: tile must be square!")
                    quit()
                else:  # storing dim if the tile is square
                    self.tile_dim = len(self.tile)
                self.gateway_cords = [
                    [],  # gateway 1
                    [],  # gateway 2
                    [],  # gateway 3
                    [],  # gateway 4
                    [],  # gateway 5
                    [],  # gateway 6
                    [],  # gateway 7
                    [],  # gateway 8
                    [],  # gateway 9
                ]

                if True:  # updating characters from stored map if game is loaded with colors
                    row_pos = self.tile_dim
                    for row in self.tile:
                        sign_total = 0
                        col_pos = 1
                        for character in row:
                            ### Regular world elements ###
                            if character == "." or character == "o":
                                self.mod_char(col_pos, row_pos, self.tile_elements[0]["character"])
                            elif character == "M":
                                self.mod_char(col_pos, row_pos, self.tile_elements[1]["character"])
                            elif character == "f":
                                self.mod_char(col_pos, row_pos, self.tile_elements[2]["character"])
                            elif character == " ":
                                self.mod_char(col_pos, row_pos, " ")

                            ### Dungeon world elements ###
                            elif character == "|":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[0]["character"])
                            elif character == "-":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[1]["character"])
                            elif character == "#":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[2]["character"])
                            elif character == "w":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[3]["character"])
                            elif character == "<":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[4]["character"])
                            elif character == ">":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[5]["character"])
                            elif character == "v":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[6]["character"])
                            elif character == "^":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[7]["character"])
                            elif character == "T":
                                self.mod_char(col_pos, row_pos, self.dungeon_elements[8]["character"])
                                self.sign_info[sign_total].append([col_pos, row_pos])
                                sign_total += 1

                            ### Gateway world elements
                            elif character == "1":  # gateway 1
                                self.mod_char(col_pos, row_pos, self.gateway_elements[0]["character"])
                                self.gateway_cords[0].append([col_pos, row_pos])
                            elif character == "2":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[1]["character"])
                                self.gateway_cords[1].append([col_pos, row_pos])
                            elif character == "3":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[2]["character"])
                                self.gateway_cords[2].append([col_pos, row_pos])
                            elif character == "4":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[3]["character"])
                                self.gateway_cords[3].append([col_pos, row_pos])
                            elif character == "5":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[4]["character"])
                                self.gateway_cords[4].append([col_pos, row_pos])
                            elif character == "6":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[5]["character"])
                                self.gateway_cords[5].append([col_pos, row_pos])
                            elif character == "7":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[6]["character"])
                                self.gateway_cords[6].append([col_pos, row_pos])
                            elif character == "8":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[7]["character"])
                                self.gateway_cords[7].append([col_pos, row_pos])
                            elif character == "9":
                                self.mod_char(col_pos, row_pos, self.gateway_elements[8]["character"])
                                self.gateway_cords[8].append([col_pos, row_pos])
                            else:
                                self.mod_char(col_pos, row_pos, self.tile_elements[1]["character"])  # converting unrecognized characters to mountains
                            col_pos += 1
                        row_pos -= 1

    def print_tile(self,): # printing the tile
        graph=""
        for row in self.tile:
            graph += " ".join(row) + "\n"
        return graph
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
