from assets import root
from assets.root import logger

class TurnManager:
    def __init__(self):
         
        self.turn = 0
        self.events = []

    def do_step(self):
        self.turn += 1
        root.game_manager.gui.game.turn_counter.change_value(1)

        for event in self.events:
            if event["turn"] == self.turn:
                logger.info(f"Executing turn event: {event}", f"TurnManager.do_step()")
                root.game_manager.effect_manager.do(event["event"]["do"], event["event"]["event_data"])
        for fraction in root.game_manager.fraction_manager.get_all_fractions():
            for producer in fraction.production["buildings"]:
                if self.turn >= producer.last_prodaction_at + producer.prodaction_time:
                    producer.last_prodaction_at = self.turn
                    producer.produce(producer)
            for town in fraction.towns:
                town.simulation()

    def add_event_in_queue(self, time: int, event: dict):
        '''
        event = {"do": event_type, "event_data": {"att": data...}}

        instead of {"att": data...} all attributes for the effects to be executed must be specified
        for example: {"do": event_type, "event_data": {"cell": root.game_manager.get_chosen_cell(), "resource": {"resource_0": 10, "resource_1": 5}}}
        '''
        if time == 0:
            logger.info(f"event {event} has time {time} (0) and will be executed on this turn {self.turn}", f"TurnManager.add_event_in_queue({time}, {event})")
            root.game_manager.effect_manager.do(event["do"], event["event_data"])
        elif time < 0:
            logger.error("Time for event must be a positive integer or zero", f"TurnManager.add_event_in_queue({time}, {event})")
        else:
            self.events.append({"turn": self.turn+time, "event": event})
            logger.info(f"event {event} successfully added in qeue with time: {time} and will be executed on turn {self.turn+time}", f"TurnManager.add_event_in_queue({time}, {event})")