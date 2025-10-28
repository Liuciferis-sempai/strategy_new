from ..buttons import *
from ..infoboxs import *
from ..contentbox import *
from ..statistikbox import *
from ..textfield import *
from ..iconbox import *
from ..listof import *
import assets.root as root

class GUIGPolicy:
    def __init__(self):
        pass
    
    def open(self):
        root.game.policy_table.load_policies_for_player()
    
    def draw(self):
        root.screen.fill((0, 0, 0))
        root.game.policy_table.draw()
        root.need_update_gui = False