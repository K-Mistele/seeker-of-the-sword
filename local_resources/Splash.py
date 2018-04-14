from local_resources import ascii_resources  # ascii art resources
from local_resources.colorama_master import colorama  # color library
class Splash:
    def __init__(self,with_color=False):
        # Splash Screen: the Main logo of the game!
        if with_color:
            print(colorama.Fore.MAGENTA + ascii_resources.color_splash_screen[0] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[1] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[2] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[3] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[4] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[5] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[6] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[7] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[8] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[9] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[10] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[11] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[12] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[13] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[14] +
                  colorama.Fore.BLUE + ascii_resources.color_splash_screen[15] +
                  colorama.Fore.RED + ascii_resources.color_splash_screen[16] +
                  colorama.Fore.GREEN + ascii_resources.color_splash_screen[17] +
                  colorama.Fore.WHITE)
        else:
            print(ascii_resources.plain_splash_screen)
