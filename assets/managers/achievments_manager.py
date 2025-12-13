import os
import json
import copy
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import loading, logger
from ..auxiliary_stuff import *
from ..gui.achievment_box import AchievmentBox

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class AchievmentsManager:
    def __init__(self, game_manager: "GameManager", achievments: dict[str, bool]):
        self.game_manager = game_manager
        self.player_achievments = achievments
        
        self.achievments = {}
        self.achievments_boxs = []
        self.load_achievments()
        self.last_tick = 0
    
    def load_achievments(self):
        self.achievments = {}
        for achievmentsfile in os.listdir("data/achievments/data"):
            if achievmentsfile.endswith(".json"):
                with open(f"data/achievments/data/{achievmentsfile}", "r", encoding="utf-8") as f:
                    achievments_data = json.load(f)
                    self.achievments[achievments_data["id"]] = achievments_data
                    setattr(self, achievments_data["id"], self.player_achievments.get(achievments_data["id"], False))

    def do_achievment(self, achievment_id: str) -> bool:
        if not has(self.achievments, achievment_id): return False
        if get(self, achievment_id) == True: return False
        setattr(self, achievment_id, True)

        ach = self.achievments[achievment_id]
        self.achievments_boxs.append(
            AchievmentBox(
                font_color=ach.get("font_color", (0, 0, 0)),
                    titel_font_color=double_get(ach, "titel_font_color", "font_color", (0, 0, 0)),
                    desc_font_color=double_get(ach, "desc_font_color", "font_color", (0, 0, 0)),
                bg_color=ach.get("bg_color", (200, 200, 200)),
                ico=ach.get("img", None),
                titel=ach["id"],
                desc=ach["desc"],
                positioning="right_bottom",
                position=root.window_size
            )
        )
        update_gui()
        return True
    
    def check_trigger(self, trigger: dict, happend: dict) -> bool:
        self.game_manager.parsing_json_data(trigger)
        for key in happend:
            if not equal(happend[key], trigger[key]):
                return False
        return True

    def tick(self):
        if is_empty(self.achievments_boxs): return
        self.last_tick += 1
        if self.last_tick > 250:
            self.achievments_boxs.pop(0)
            self.last_tick = 0
            update_gui()
    
    def draw(self):
        if not is_empty(self.achievments_boxs):
            self.achievments_boxs[0].draw()