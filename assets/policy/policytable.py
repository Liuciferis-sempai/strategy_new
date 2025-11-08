import os
from assets.auxiliary_stuff.work_with_files import read_json_file
from .policy import PolicyCard
import assets.root as root
from assets.root import logger
from assets.root import loading
from assets.auxiliary_stuff.functions import update_gui

class PolicyTable:
    def __init__(self):
        self.all_policiec: list[PolicyCard] = []

        loading.draw("Loading policy cards...")
        self.load_policies_cards()

    def load_policies_cards(self):
        for policyfile in os.listdir("data/policy"):
            if policyfile.endswith(".json"):
                policy_data = read_json_file(f"data/policy/{policyfile}")
                self.all_policiec.append(PolicyCard(policy_data, (0, 0)))

    def load_policies_for_player(self):
        player_fraction = root.game_manager.fraction_manager.get_player_fraction()

        x = 0
        y = 0
        for policy in player_fraction.policies:
            if root.interface_size*x+root.interface_size//2+root.interface_size > root.window_size[0]:
                x = 0
                y += 1
            policy.change_position((root.interface_size*x+root.interface_size//2, (root.interface_size*2)*y+root.interface_size//2))
            x += 1

    def get_policy_by_id(self, policy_id:str) -> PolicyCard:
        for policy in self.all_policiec:
            if policy.id == policy_id:
                return policy
        logger.error(f"can not find policy by id {policy_id}", f"PolicyTable.get_policy_by_id({policy_id})")
        return PolicyCard({})