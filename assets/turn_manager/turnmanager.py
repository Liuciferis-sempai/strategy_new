from assets import root
from assets.functions import logging

class TurnManager:
    def __init__(self):
         
        self.turn = 0
        self.events = []

    def do_step(self):
        self.turn += 1
        root.handler.gui.game.turn_counter.change_value(1)

        for event in self.events:
            if event["turn"] == self.turn:
                logging("INFO", f"Executing turn event: {event}", "TurnManager.do_step")
                root.handler.effect_manager.do(event["event"]["do"], event["event"]["event_data"])

    def add_event_in_queue(self, time: int, event: dict):
        '''
        event = {"do": event_type, "event_data": {"att": data...}}

        instead of {"att": data...} all attributes for the effects to be executed must be specified
        for example: {"do": event_type, "event_data": {"cell": root.handler.get_chosen_cell(), "resource": {"resource_0": 10, "resource_1": 5}}}
        '''
        if time == 0:
            logging("INFO", f"event {event} has time {time} (0) and will be executed on this turn {self.turn}", "TurnManager.add_event_in_queue")
            root.handler.effect_manager.do(event["do"], event["event_data"])
        elif time < 0:
            logging("ERROR", "Time for event must be a positive integer or zero", "TurnManager.add_event_in_queue", f"time: {time}, event: {event}")
        else:
            self.events.append({"turn": self.turn+time, "event": event})
            logging("INFO", f"event {event} successfully added in qeue with time: {time} and will be executed on turn {self.turn+time}", "TurnManager.add_event_in_queue")