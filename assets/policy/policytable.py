import os
from assets.auxiliary_stuff.work_with_files import read_json_file
from .policy import PolicyCard
import assets.root as root
from assets.root import loading
from assets.auxiliary_stuff.functions import update_gui

class PolicyTable:
    def __init__(self):
        self.all_policiec = []
        self.policies = []
        self.chosen_policies = []

        loading.draw("Loading policy cards...")
        self.load_policies_cards()

    def load_policies_cards(self):
        for policyfile in os.listdir("data/policy"):
            if policyfile.endswith(".json"):
                policy_data = read_json_file(f"data/policy/{policyfile}")
                self.all_policiec.append(PolicyCard(policy_data, (0, 0)))

    def load_policies_for_player(self):
        self.chosen_policies = []
        player_fraction = root.game_manager.fraction_manager.get_player_fraction()
        if player_fraction is None:
            return
        x = 0
        y = 0
        for policy in player_fraction.policies:
            for policy_card in self.policies:
                if policy_card.data.get("id") == policy.get("id"):
                    if root.interface_size*x+root.interface_size//2+root.interface_size > root.window_size[0]:
                        x = 0
                        y += 1
                    policy_card.change_position((root.interface_size*x+root.interface_size//2, (root.interface_size*2)*y+root.interface_size//2))
                    self.chosen_policies.append(policy_card)
                    x += 1

    def get_policy_data_by_id(self, policy_id:str) -> PolicyCard|None:
        for policy in self.policies:
            if policy.data.get("id") == policy_id:
                return policy.data
        return None
    
    def update_positions(self):
        x = 0
        y = 0
        for policy in self.policies:
            if root.interface_size*x+root.interface_size//2+root.interface_size > root.window_size[0]:
                x = 0
                y += 1
            policy.rect.topleft = (root.interface_size*x+root.interface_size//2, (root.interface_size*2)*y+root.interface_size//2)
            x += 1
    
    def collidepoint(self, mouse_pos: tuple[int, int]) -> bool:
        for policy in self.policies:
            rect = policy.get("rect", (0, 0, 100, 100))
            if rect.collidepoint(mouse_pos):
                return True
        return False

    def draw(self):
        for policy in self.chosen_policies:
            policy.draw()
    
    def scroll_up(self):
        for policy in self.policies:
            policy.rect.y += root.interface_size//2
        update_gui()

    def scroll_down(self):
        for policy in self.policies:
            policy.rect.y -= root.interface_size//2
        update_gui()