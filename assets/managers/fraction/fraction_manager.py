from .fraction import Fraction
from ... import root
from ...root import logger
from typing import Any, TYPE_CHECKING
from ..policy.policytable import PolicyTable
from ..policy.policycard import PolicyCard

if TYPE_CHECKING:
    from ...gamemanager import GameManager

class FractionManager:
    def __init__(self, game_manager: "GameManager"):
        self.game_manager = game_manager
        self._default_fraction = self.game_manager.get_default_fraction()

        self.fractions: list = []
        self.blooked_fraction_ids: list[int] = []

    def create_fraction(self, name: str, type: str, id: int = 0, data: dict={}):
        if id not in self.blooked_fraction_ids: self.blooked_fraction_ids.append(id)
        else: return self.create_fraction(name, type, id+1, data)
        fraction = Fraction(name, type, id, data, False)
        self._add_fraction(fraction)
        return fraction

    def _add_fraction(self, fraction: Fraction):
        self.fractions.append(fraction)

    def get_fraction_by_name(self, name: str) -> Fraction:
        for fraction in self.fractions:
            if fraction.name == name:
                return fraction
        logger.error(f"fraction by name {name} not found", f"AllFactions.get_fraction_by_name({name})")
        return self._default_fraction

    def get_all_fractions(self) -> list[Fraction]:
        return self.fractions
    
    def get_player_fraction(self) -> Fraction:
        for fraction in self.fractions:
            if fraction.type == "player" and fraction.id == root.player_id:
                return fraction
        logger.error(f"player fraction not found", "AllFactions.get_fraction_by_name()")
        return self._default_fraction

    def get_fraction_by_id(self, id: int) -> Fraction:
        for fraction in self.fractions:
            if fraction.id == id:
                return fraction
        logger.error(f"fraction id not found", f"AllFactions.get_fraction_by_name({id})")
        return self._default_fraction

    def edit_fraction(self, name:str="", id:int=0, data:dict={}) -> bool:
        if name == "" and id == 0:
            return False
        for fraction in self.fractions:
            if fraction.name == name or fraction.id == id:
                fraction.edit(data=data)
                return True
        return False
    
    def add_policy_to_fraction(self, fraction: int|Fraction, policy: str|dict|PolicyCard) -> str:
        if isinstance(fraction, int):
            fraction = self.get_fraction_by_id(fraction)
        
        if isinstance(policy, str):
            policy = self.game_manager.policy_table.get_policy_by_id(policy)
        elif isinstance(policy, dict):
            policy = self.game_manager.policy_table.get_policy_by_id(policy.get("id", "unknow"))
        
        fraction.policies.append(policy)
        self.game_manager.policy_table.set_policy_sinergy(fraction.policies)
        return f"added {policy.id} to {fraction.name} ({fraction.id})"
    
    def remove_policy_to_fraction(self, fraction: int|Fraction, policy: str|dict|PolicyCard) -> str:
        if isinstance(fraction, int):
            fraction = self.get_fraction_by_id(fraction)
        
        if isinstance(policy, str):
            policy = self.game_manager.policy_table.get_policy_by_id(policy)
        elif isinstance(policy, dict):
            policy = self.game_manager.policy_table.get_policy_by_id(policy.get("id", "unknow"))

        fraction.policies.remove(policy)
        self.game_manager.policy_table.set_policy_sinergy(fraction.policies)
        return f"removed {policy.id} by {fraction.name} ({fraction.id})"