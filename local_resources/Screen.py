import platform
from os import system
from time import sleep
from local_resources.colorama_master import colorama

class Screen:
    def __init__(self):

        '''
                    +---------------+-------+
                    |               |       |
                    |               |inven- |
                    |      World    |-tory  |
                    |      KxK      |       |
                    |               | 20xK  |
                    +-------+-------+-------+
                    |status |  console      |
                    | 20x5  |    (K)x5       |
                    +-------+---------------+
        '''

        #System Configuration
        if platform.system() != "Windows":
            self._clear_command = "clear"
        else:
            self._clear_command = "cls"

        # Graph Setup
        self._worldGraph=""
        self._playerStatusGraph="\n\n\n\n\n"
        #self._inventoryGraph=""

        #Completed Abstract screen graph
        self._composedGraph=""

        #Blocks Storage:
        self._worldBlock=[]
        self._consoleBlock=["","","","",""]
        #self._inventoryBlock=[]

    #============= Update =============================
    def updateWorld(self,worldString):
        self._worldGraph=worldString
    def updateStatus(self,statusString):
        self._playerStatusGraph=statusString
    def console(self,newLine):

        # add the new lines and take only the previous 5
        newConsole = self._consoleBlock + newLine.split("\n")
        self._consoleBlock =newConsole[-5:]
    def updateInventory(self,inventoryString):
        self._inventoryGraph = inventoryString

    #============ Meta Functions ========================
    def clearScreen(self):
        # description: Clear all text on the screen
        system(self._clear_command)
    def _buildStatusBlock(self):

        #Parse the text
        lines = self._playerStatusGraph.split("\n")
        updatedLines=[]

        # Take only the first 5 lines
        for i in range(0,min(5,len(lines))):
            # Ensure line is 20 characters long and add
            updatedLine = lines[i] + "                    "    #These two lines cause a problem for color
            updatedLine = updatedLine[0:20]                    #These two lines cause a problem for color
            updatedLines.append(updatedLine)


        # Fix Vertically
        if len(lines)< 5:
            for i in range(0,5-len(lines)):
                updatedLines.append("                    ")

        #store the computation
        return updatedLines
    def _buildGraph(self):
        #top Graph
        topGraph = self._worldGraph

        # bottom Graph
        bottomGraph=""
        status = self._buildStatusBlock()
        for i in range(0,5):
            bottomGraph += status[i] + " " + self._consoleBlock[i] + "\n"

        #Store the Graph
        self._composedGraph = topGraph + "\n"+bottomGraph

    #============ Render the Screen ======================
    def render(self):
        # description: Prints the composed graph to the screen
        self._buildGraph()
        self.clearScreen()
        print(self._composedGraph)

#Testing
if __name__ == "__main__":
    colorama.init()
    test = Screen()
    test.console("[Console] Game Started")
    test.console("[Console] Attack")
    test.console("[Console] ")
    test.console("[Console] Right")
    test.console("[Console] "+colorama.Fore.BLUE+"Left")
    test.updateStatus("Health: 0000000000\n        0000000000\n        0000000000")
    test.render()
    sleep(3)
    test.console("[Console] Hello \n[Console] World")
    test.updateStatus("Health: 0000000000\n        00000")
    test.render()
    sleep(3)
    test.updateStatus("Health: 0000000000\n")
    test.render()