#Imports
from local_resources.colorama_master import colorama
from os import listdir

class GenerateSettings:
    #============ Init =======================
    def __init__(self,lightspeed=False):
        #====== Default settings ========
        #== _query_with_colors
        self.with_colors = True
        #==  _query_name
        self.name="[devmode] Player"
        #== _query_difficulty_config
        self.difficulty_config = ['normal',self.name, 20, 2, 2, 1, 3] #basic difficulty
        #== _query_map_settings
        self.dim=16
        self.world_settings = [self.dim, "world", self.with_colors, False,""]#
        self.world_do_generate = True #IF THIS IS FALSE the instance of GenerateSettings.dim MUST be explicitly set
        #                              as GenerateSettings.dim = world.tile_dim WILL Cause error if not set

        #======= Otherwise Generate =======
        #Lightspeed: skip asking the user for input; and use the default settings
        if not lightspeed:

            #NOTE functions called in this order... some  rely on variables generated in
            #These will set the class properties above...
            self._query_with_colors()
            self._query_name()
            self._query_difficulty_config()
            self._query_map_settings()

    # ============= Query Functions ======================
    def _query_with_colors(self):

        #Ask the user if they want to init with_colors
        while True:
            with_colors = input("Initiate with colors?\n")
            if "y" in with_colors.lower():
                self.with_colors = True
                break
            elif "n" in with_colors.lower():
                self.with_colors= False
                break
            else:
                print("Invalid input!")
                continue
    def _query_name(self):

        #Ask the user to input their name
        if self.with_colors:
            name = input(colorama.Fore.WHITE + "Please enter your name:\n")
            if name.lower() == "hot dog":
                print(colorama.Fore.GREEN + "\nWelcome, [ADMIN]\n")
        else:
            name = input("Please enter your name:\n")
            if "[admin]" in name.lower():
                print("\nWelcome, [ADMIN]\n")

        self.name = name
    def _query_difficulty_config(self):

        #Set the config for difficulty
        while True:
            if self.with_colors:
                select_difficulty = input(colorama.Fore.WHITE+"Please select difficulty: Normal, Heroic, or True Seeker:\n").lower()
            else:
                select_difficulty = input("Please select difficulty: Normal, Heroic, or True Seeker:\n").lower()
            if select_difficulty in "normal":
                self.difficulty_config = ['normal',self.name, 20, 2, 2, 1, 3]# basic difficulty
                break
            elif select_difficulty in "heroic":
                self.difficulty_config = ['heroic', self.name, 20, 2, 2, 1, 3] #more mobs will spawn
                break
            elif select_difficulty in "true seeker":
                self.difficulty_config = ['seeker', self.name, 15, 4, 4, 1, 1]# lower health, higher damage; more mobs will spawn
                break
            else:
                continue
    def _query_map_settings(self):
        while True:

            #=== [Generate/Custom]?
            if self.with_colors:
                with_custom = input(colorama.Fore.WHITE+"Generate map or use custom?\n").lower()
            else:
                with_custom = input("Generate map or use custom?\n").lower()  # asking user to either generate or use custom map

            #=== Generate Option
            if with_custom in "generate" or "generate" in with_custom:
                while True:  # sanitized getting dim
                    if self.with_colors:
                        self.dim = input(colorama.Fore.WHITE+"Tile dimension?(minimum 16)\n")
                    else:
                        self.dim = input("Tile dimension?(minimum 16)\n")  # getting world dimensions from user
                    try:
                        self.dim = int(self.dim)
                        if self.dim < 16:
                            if self.with_colors:
                                print(colorama.Fore.WHITE+"Tile size too small.")
                            else:
                                print("Tile size too small.")
                            continue
                        break
                    except:
                        if self.with_colors:
                            print(colorama.Fore.WHITE+"Invalid input!")
                        else:
                            print("Invalid input!")
                        continue
                self.world_settings= [self.dim, "world", self.with_colors, False,""]# creating "world" object in "table" class with user input
                self.world_do_generate = True
                #world = world_tile(dim, "world", with_colors, False,"")
                #system(clear_command)  # clearing screen to prepare for game
                break

            #=== Custom Option
            elif with_custom in "custom" or "custom" in with_custom:
                self.dim = 5
                available_files = listdir("custom_maps")  # getting all files in directory that stores maps
                available_maps = []
                for file in available_files:  # only preparing files to display to user that are text files
                    if ".txt" in file:
                        available_maps.append(file[:-4])
                if self.with_colors:
                    print(colorama.Fore.WHITE+"\nAvailable maps:")
                else:
                    print("\nAvailable maps:")
                for map in available_maps:  # printing maps that the user can choose from
                    if self.with_colors:
                        print(colorama.Fore.WHITE+map)
                    else:
                        print(map)
                while True:
                    if self.with_colors:
                        filename = input(colorama.Fore.WHITE+"\nInput name of file to be imported:\n")
                    else:
                        filename = input("\nInput name of file to be imported:\n")
                    if filename in available_maps:
                        self.world_settings = [self.dim, "world", self.with_colors, True, filename+".txt"]
                        self.world_do_generate=False
                        #world = world_tile(dim, "world", with_colors, True, filename+".txt")
                        #system(clear_command)
                        break
                    else:
                        if self.with_colors:
                            print(colorama.Fore.WHITE+"Invalid file name!")
                        else:
                            print("Invalid file name!")
                        continue
                break
            else:
                if self.with_colors:
                    print(colorama.Fore.WHITE+"Invalid Input!")
                else:
                    print("Invalid input!")
                continue
        #dim = world.tile_dim !!!!!!!!!!!!!!!! The code was adapted but it is spagetti... this
        #code alone needs to be split into 4 seperate functions

if __name__ == "__main__":
    pass