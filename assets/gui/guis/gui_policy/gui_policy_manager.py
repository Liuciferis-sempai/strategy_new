import pygame as py
from ...buttons import *
from ...infoboxs import *
from ...contentbox import *
from ...statistikbox import *
from ...textfield import *
from ...iconbox import *
from ...listof import *
from ...inputfield import *
from .... import root
from ....root import logger
from ....auxiliary_stuff import *
from typing import Any, TYPE_CHECKING
from .gui_policy_list import GUIGPolicyList
from .gui_policy_stack import GUIGPolicyStack

if TYPE_CHECKING:
    from ....gamemanager import GameManager

class PolicyGUIManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.state = "list"
        self.titel = TextField(text="policy_list_titel")
        
        self.list = GUIGPolicyList(self.game_manager)
        self.stack = GUIGPolicyStack(self.game_manager)

    def do_for(self, func, *args, **kwargs):
        if self.state == "list":
            getattr(self.list, func)(*args, **kwargs)
        elif self.state == "stack":
            getattr(self.stack, func)(*args, **kwargs)
        else:
            logger.error(f"unknow policy state '{self.state}'", f"PolicyGUIManager.do_for(self, {func}, {args}, {kwargs})")

    def update_positions(self):
        self.list.update_positions()
        self.stack.update_positions()

    def chose(self, new_state: str):
        self.state = new_state
        update_gui()

    def draw(self):
        self.do_for("draw")

    def open(self):
        self.list.open()

    def click(self, mouse_pos):
        self.do_for("click", mouse_pos=mouse_pos)

    def move_up(self):
        self.do_for("move_up")

    def move_down(self):
        self.do_for("move_down")

    def move_left(self):
        pass

    def move_right(self):
        pass