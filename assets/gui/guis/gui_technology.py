from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root

class GUITechnology:
    def __init__(self):
        pass
    
    def open(self):
        pass

    def draw(self):
        root.screen.fill((0, 0, 0))
        root.game_manager.tech_tree.draw()
        root.need_update_gui = False