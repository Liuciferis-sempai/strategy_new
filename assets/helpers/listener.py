from typing import Any, TYPE_CHECKING
from ..auxiliary_stuff import *

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class Listener:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.waiting: dict[str, list[tuple[list[dict]|dict, list[dict]|dict]]] = {}

    def add(self, trigger: list[dict]|dict, effect: list[dict]|dict) -> tuple:
        if isinstance(trigger, dict):
            append(self.waiting, trigger["effect_type"], (trigger, effect))
            return (trigger["effect_type"], trigger, effect)
        elif isinstance(trigger, list):
            triggers = []
            for subtrigger in trigger:
                triggers.append(subtrigger["effect_type"])
                append(self.waiting, subtrigger["effect_type"], (trigger, effect))
            return (triggers, trigger, effect)

    def remove(self, listener: tuple[str|list[str], dict|list, dict|list]) -> bool:
        if isinstance(listener[0], str):
            if has(self.waiting, listener[0]):
                self.waiting[listener[0]].remove((listener[1], listener[2]))
                return True
            return False
        else:
            result = True
            for trigger in listener[0]:
                if has(self.waiting, trigger):
                    self.waiting[trigger].remove((listener[1], listener[2]))
                else: result = False
            return result

    def happend(self, happend: str, **kwargs):
        if has(self.waiting, happend):
            for waiting in self.waiting[happend]:
                self._check(waiting, happend, **kwargs)

    def _check(self, waiting: tuple[list[dict]|dict, list[dict]|dict], happend: str, **kwargs):
        trigger = waiting[0]
        effect = waiting[1]

        if isinstance(trigger, list):
            for subtrigger in trigger:
                if not has(subtrigger, "is_happened"):
                    if self._check_trigger(subtrigger, kwargs):
                        subtrigger["is_happened"] = True    
                    else:
                        return
                elif not subtrigger["is_happened"]:
                    return

            self.remove(([subtrigger["effect_type"] for subtrigger in trigger ], trigger, effect))
            self._do(effect)
        else:
            if not has(trigger, "is_happened"):
                if self._check_trigger(trigger, kwargs):
                    trigger["is_happened"] = True
                else:
                    return
            elif not trigger["is_happened"]:
                return
            
            self.remove((trigger["effect_type"], trigger, effect))
            self._do(effect)

    def _do(self, effect: dict|list[dict]):
        if isinstance(effect, list):
            for subeffect in effect:
                self.game_manager.execute_effect(subeffect)
        else:
            self.game_manager.execute_effect(effect)

        
    def _check_trigger(self, trigger: dict, happend: dict) -> bool:
        self.game_manager.parsing_json_data(trigger)
        for key in happend:
            if not equal(happend[key], trigger[key]):
                return False
        return True