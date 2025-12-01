from .. import root
from ..root import logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..gamemanager import GameManager

class TurnManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.turn = 0
        self.events = []

    def do_step(self):
        self.turn += 1
        self.game_manager.gui.game.turn_counter.change_value(1)

        for event in self.events:
            if event["turn"] == self.turn:
                logger.info(f"Executing turn event: {event}", f"TurnManager.do_step()")
                self.game_manager.effect_manager.do(event["event"]["do"], event["event"]["event_data"])

        self.game_manager.town_manager.turn()
        self.game_manager.storage_manager.turn()
        self.game_manager.producer_manager.turn()
        self.game_manager.workbench_manager.turn()

    def add_event_in_queue(self, time: int, event: dict) -> None|dict:
        '''
        event = {"do": event_type, "event_data": {"att": data...}}

        instead of {"att": data...} all attributes for the effects to be executed must be specified
        for example: {"do": event_type, "event_data": {"cell": self.game_manager.get_chosen_cell(), "resource": {"resource_0": 10, "resource_1": 5}}}
        '''
        if time == 0:
            logger.info(f"event {event["do"]} has time {time} (0) and will be executed on this turn {self.turn}", f"TurnManager.add_event_in_queue(...)")
            self.game_manager.effect_manager.do(event["do"], event["event_data"])
        elif time < 0:
            logger.error(f"Time for event must be a positive integer or zero, event {event["do"]}", f"TurnManager.add_event_in_queue(...)")
        else:
            effect = {"turn": self.turn+time, "event": event}
            self.events.append(effect)
            logger.info(f"event {event["do"]} successfully added in qeue with time: {time} and will be executed on turn {self.turn+time}", f"TurnManager.add_event_in_queue(...)")
            return effect

    def remove_event(self, effect: dict) -> bool:
        try:
            self.events.remove(effect)
            return True
        except:
            return False