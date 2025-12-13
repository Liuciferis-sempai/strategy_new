import os
import json
import copy
from typing import Any, TYPE_CHECKING
from .. import root
from ..root import loading, logger
from ..gui.eventbox import *

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class EventManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.events: dict = {}
        self.events_queue: list[EventBox] = []

        self.load_events()
    
    def load_events(self):
        self.events = {}
        for eventfile in os.listdir("data/events"):
            if eventfile.endswith(".json"):
                with open(f"data/events/{eventfile}", "r", encoding="utf-8") as f:
                    event_data = json.load(f)
                    self.events[event_data["id"]] = event_data
    
    def get_event_by_id(self, event_id: str) -> dict:
        event = self.events.get(event_id)
        if not event:
            return {}.copy()
        return copy.deepcopy(event)

    def event_call(self, event: dict|str, event_context: dict = {}) -> str:
        if isinstance(event, str): event = self.get_event_by_id(event)
        if is_empty(event): return "event not found"

        self.events_queue.append(
            EventBox(
                event_id = event["id"],
                event_titel = event["id"],
                event_desc = event["desc"],
                event_choices = self._parsing_event_choices(event["choices"]),
                event_context=event_context
                )
        )
        return f"called event {event["id"]}"

    def _parsing_event_choices(self, choices: list) -> list[tuple[str, dict, tuple[int, int, int]]]:
        available_choices = []
        for event_choice in choices:
            if self._is_choice_trigger_available(event_choice):
                event_choice_color = event_choice.get("choice_color")
                if not event_choice_color: event_choice_color = (0, 0, 0)
                else: event_choice_color = tuple(event_choice_color)
                available_choices.append(
                    (event_choice["choice_name"], {}, event_choice_color)
                )

        return available_choices

    def _is_choice_trigger_available(self, event_choice: dict) -> bool:
        if not has(event_choice, "trigger"): return True
        if isinstance(event_choice["trigger"], dict):
            return self._check_choice_trigger(event_choice["trigger"])
        elif isinstance(event_choice["trigger"], list):
            result = []
            for trigger in event_choice["trigger"]:
                result.append(self._check_choice_trigger(trigger))
            return all(result)
        return False

    def _check_choice_trigger(self, trigger: dict) -> bool:
        if hasattr(self.game_manager.trigger_manager, trigger["type"]):
            self.game_manager.parsing_json_data(trigger)
            trigger_func = getattr(self.game_manager.trigger_manager, trigger["type"])
            is_allowed = trigger_func(**trigger["args"])
            if not is_allowed: self.game_manager.messenger.print_buffer()
            return is_allowed
        return False

    def _parsing_event_choice_result(self, event_choice: dict, event_context: dict) -> dict:
        return event_choice # @TODO
    
    def _execute_event_result(self, event_choice: dict, event_context: dict):
        event_choice = self._parsing_event_choice_result(event_choice, event_context)
        self.game_manager.parsing_json_data(event_choice, calling_fraction_id=event_context.get("fraction_id"))
        self.game_manager.execute_effect(event_choice)

    def draw(self):
        if len(self.events_queue) != 0:
            self.events_queue[0].draw()
    
    def event_choice(self, event_id: str, choice_name: str, event_context: dict|None):
        if not event_context: event_context = {}
        event = self.events.get(event_id)
        if not event: return

        for event_choice in event["choices"]:
            if event_choice["choice_name"] == choice_name:
                if has(event_choice, "result"):
                    if isinstance(event_choice["result"], dict):
                        self._execute_event_result(event_choice["result"], event_context)
                    elif isinstance(event_choice["result"], list):
                        for choise_result in event_choice["result"]:
                            self._execute_event_result(choise_result, event_context)
                break
        self.events_queue.pop(0)