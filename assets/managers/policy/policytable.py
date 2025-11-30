import os
from ...auxiliary_stuff import read_json_file, update_gui, is_color_cold, is_color_warm, cold_degree
from .policycard import PolicyCard
from .policystack import PolicyStack
from ... import root
from ...root import logger, loading
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class PolicyTable:
    angles_per_figure = {
        "circle": 0,
        "triangle": 3,
        "square": 4,
        "pentagon": 5,
        "hexagon": 6,
        "octagon": 8
    }

    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self.all_stacks: list[PolicyStack] = []
        self.all_policiec: list[PolicyCard] = []
        self.card_size = int(root.interface_size * 1.6)

        loading.draw("Loading policy cards...")
        self.load_policies_stacks()
        self.load_policies_cards()

    def load_policies_cards(self):
        for policyfile in os.listdir("data/policy/policy_cards"):
            if policyfile.endswith(".json"):
                policy_data = read_json_file(f"data/policy/policy_cards/{policyfile}")
                self.all_policiec.append(PolicyCard(policy_data, (0, 0), self.card_size))
    
    def load_policies_stacks(self):
        for stackfile in os.listdir("data/policy/policy_stacks"):
            if stackfile.endswith(".json"):
                stack_data = read_json_file(f"data/policy/policy_stacks/{stackfile}")
                self.all_stacks.append(PolicyStack(stack_data))

    def get_policy_by_id(self, policy_id: str) -> PolicyCard:
        for policy in self.all_policiec:
            if policy.id == policy_id:
                policy_card = policy.copy()
                policy_card.check_available_status()
                return policy_card
        logger.error(f"can not find policy by id {policy_id}", f"PolicyTable.get_policy_by_id({policy_id})")
        return PolicyCard({})
    
    def get_policy_stack(self, policy: PolicyCard) -> list[PolicyCard]|None:
        policy_stack = []
        for stack in self.all_stacks:
            if policy.id in stack.cards:
                for card in stack.cards:
                    policy_card = self.get_policy_by_id(card)
                    policy_card.check_available_status()
                    policy_stack.append(policy_card)
                return policy_stack
    
    def set_policy_sinergy(self, policies: list[PolicyCard]):
        if len(policies) <= 1: #if only one policy is set, no sinergy calculation needed
            policies[0].set_influence_weight(1.0)
            return
        map(lambda policy: policy.set_influence_weight(1.0), policies)
    
        cold_colors = [policy.color for policy in policies if is_color_cold(policy.color) and policy.color != "#000000" and policy.color != "#FFFFFF"]
        warm_colors = [policy.color for policy in policies if is_color_warm(policy.color) and policy.color != "#000000" and policy.color != "#FFFFFF"]
        if len(cold_colors) > len(warm_colors):
            majority_colors = cold_colors
            minority_colors = warm_colors
        elif len(warm_colors) > len(cold_colors):
            majority_colors = warm_colors
            minority_colors = cold_colors
        else:
            majority_colors = []
            minority_colors = []
        
        figueres_angle = [self._get_angles_per_figure(policy.figure) for policy in policies]
        figueres_angle = {angles_count: figueres_angle.count(angles_count)/len(figueres_angle) for angles_count in set(figueres_angle)}
        circle_count = len([policy_.figure for policy_ in policies if policy_.figure == "circle"])

        even_numbers = [policy.number for policy in policies if policy.number % 2 == 0 and policy.number != 0]
        not_even_numbers = [policy.number for policy in policies if policy.number % 2 != 0]
        avg_numver = sum([policy.number for policy in policies])/len(policies)
        if len(even_numbers) > len(not_even_numbers):
            majority_numbers = even_numbers
            minority_numbers = not_even_numbers
        elif len(not_even_numbers) > len(even_numbers):
            majority_numbers = not_even_numbers
            minority_numbers = even_numbers
        else:
            majority_numbers = []
            minority_numbers = []

        for policy in policies:
            weight = 1.0
            if policy.color in majority_colors:
                if (is_color_cold(policy.color) and cold_degree(policy.color) > 0.5) or (is_color_warm(policy.color) and (1 - cold_degree(policy.color)) > 0.5):
                    weight += 0.1
                elif (is_color_cold(policy.color) and cold_degree(policy.color) > 0.2) or (is_color_warm(policy.color) and (1 - cold_degree(policy.color)) > 0.2):
                    weight += 0.05
                else:
                    weight += 0.02
            elif policy.color in minority_colors:
                if (is_color_cold(policy.color) and cold_degree(policy.color) > 0.5) or (is_color_warm(policy.color) and (1 - cold_degree(policy.color)) > 0.5):
                    weight -= 0.3
                elif (is_color_cold(policy.color) and cold_degree(policy.color) > 0.2) or (is_color_warm(policy.color) and (1 - cold_degree(policy.color)) > 0.2):
                    weight -= 0.1
                else:
                    weight -= 0.05

            if policy.number in majority_numbers:
                if abs(policy.number - avg_numver) < 6:
                    weight += 0.15
                elif abs(policy.number - avg_numver) < 3:
                    weight += 0.1
                elif policy.number != avg_numver:
                    weight += 0.05
                else:
                    weight += 0.02
            elif policy.number in minority_numbers:
                if abs(policy.number - avg_numver) < 6:
                    weight -= 0.4
                elif abs(policy.number - avg_numver) < 3:
                    weight -= 0.25
                elif policy.number != avg_numver:
                    weight -= 0.15
                else:
                    weight -= 0.05
            
            angle_count = self._get_angles_per_figure(policy.figure)
            if angle_count > 0:
                similar_angle_count = figueres_angle.get(angle_count, 0) + figueres_angle.get(angle_count - 1, 0) + figueres_angle.get(angle_count + 1, 0)
                if similar_angle_count > 0.6:
                    weight += 0.15
                elif similar_angle_count > 0.5:
                    weight += 0.1
                elif similar_angle_count > 0.35:
                    weight += 0.05
                elif similar_angle_count > 0.2:
                    weight -= 0.3
                elif similar_angle_count > 0.1:
                    weight -= 0.2
                else:
                    weight -= 0.25

            if policy.color == "#000000" and is_color_warm(majority_colors[0]): weight *= 1.2
            elif policy.color == "#FFFFFF" and is_color_cold(majority_colors[0]): weight *= 1.2

            if policy.number == 0: pass

            if angle_count == 0: weight *= 1 + circle_count/20

            policy.set_influence_weight(weight)
            policy.update_info()
            logger.info(f"policy {policy} has new weight {weight}", "PolicyTable.set_policy_sinergy(...)")
        if majority_numbers: number = "even" if majority_numbers[0] % 2 == 0 else "not event"
        else: number = "even and not even are equal"
        if majority_colors: color = "cold" if is_color_cold(majority_colors[0]) else "warm"
        else: color = "warm and cold are equel"
        logger.info(f"most color are: {color} number and {number}", "PolicyTable.set_policy_sinergy(...)")
    
    def _get_angles_per_figure(self, figure: str) -> int:
        return self.angles_per_figure.get(figure.lower(), 4)

    #def set_policy_sinergy(self, policies: list[PolicyCard]):
    #    if len(policies) <= 1: #if only one policy is set, no sinergy calculation needed
    #        policies[0].set_influence_weight(1.0)
    #        return

    #    policies_ids = [policy.id for policy in policies]

    #    policies_colors = [policy.color for policy in policies]
    #    policies_colors_percents = {color: policies_colors.count(color)/len(policies) for color in set(policies_colors)}
    #    #policies_colors_count = {color: policies_colors.count(color) for color in set(policies_colors)}

    #    policies_figures = [policy.figure for policy in policies]
    #    policies_figures_percent = {figure: policies_figures.count(figure)/len(policies_figures) for figure in set(policies_figures)}
    #    #policies_figures_count = {figure: policies_figures.count(figure) for figure in set(policies_figures)}

    #    policies_numbers = [policy.number for policy in policies]
    #    policies_numbers_percent = {number: policies_numbers.count(number)/len(policies) for number in set(policies_numbers)}
    #    #policies_numbers_count = {number: policies_numbers.count(number) for number in set(policies_numbers)}

    #    #root.logger.info(f"fractions policies sinergy calculation:", "PolicyTable.set_policy_sinergy(...)")
    #    #root.logger.info(f"colors distribution: {policies_colors_percents}", "PolicyTable.set_policy_sinergy(...)")
    #    #root.logger.info(f"figures distribution: {policies_figures_percent}", "PolicyTable.set_policy_sinergy(...)")
    #    #root.logger.info(f"numbers distribution: {policies_numbers_percent}", "PolicyTable.set_policy_sinergy(...)")

    #    for policy in policies:
    #        color_percent = policies_colors_percents.get(policy.color, 0)
    #        figure_percent = policies_figures_percent.get(policy.figure, 0)
    #        number_percent = policies_numbers_percent.get(policy.number, 0)

    #        parameters = [color_percent, figure_percent, number_percent]

    #        if _no_one_parameter_under(parameters, 0.5): #все три имеют долю более 50%
    #            policy.set_influence_weight(1.5)
    #        elif _is_parameter_over(parameters, 2, 0.5) and _is_parameter_over(parameters, 3, 0.3): #два более 50% и один более 30%
    #            policy.set_influence_weight(1.2)
    #        elif _is_parameter_over(parameters, 1, 0.5) and _is_parameter_over(parameters, 2, 0.3) and _no_one_parameter_under(parameters, 0.1): #один более 50% и один 30%-50% и не один менее 10%
    #            policy.set_influence_weight(1.0)
    #        elif _is_parameter_over(parameters, 1, 0.5) and _no_one_parameter_under(parameters, 0.1): #один более 50% и не один менее 10%
    #            policy.set_influence_weight(0.9)
    #        elif _is_parameter_over(parameters, 2, 0.3) and _no_one_parameter_under(parameters, 0.1): #два более 30% и один не менее 10%
    #            policy.set_influence_weight(0.8)
    #        elif _is_parameter_over(parameters, 1, 0.3) and _no_one_parameter_under(parameters, 0.1): #один более 30% и не один менее 10%
    #            policy.set_influence_weight(0.75)
    #        elif _is_parameter_over(parameters, 3, 0.1): #все три более 10%
    #            policy.set_influence_weight(0.6)
    #        elif _is_parameter_over(parameters, 2, 0.1): #два более 10%
    #            policy.set_influence_weight(0.4)
    #        elif _is_parameter_over(parameters, 1, 0.1): #один более 10%
    #            policy.set_influence_weight(0.35)
    #        else:
    #            policy.set_influence_weight(0.2)

    #        if "sinergy_with" in policy.data:
    #            for sinergy_policy_id, sinergy_value in policy.data["sinergy_with"].items():
    #                if sinergy_policy_id in policies_ids:
    #                    policy.set_influence_weight(policy.get_influence_weight()*(1+sinergy_value))

    #        if policy.get_influence_weight() < 0:
    #            policy.set_influence_weight(0)
    #        policy.update_info()