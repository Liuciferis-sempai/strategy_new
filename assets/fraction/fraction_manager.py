from .fraction import Fraction
from assets import root
from assets.functions import logging

class AllFactions:
    def __init__(self):
        self.fractions: list = []

    def create_fraction(self, name: str, type: str, id: int, data: dict={}):
        fraction = Fraction(name, type, id, data)
        self._add_fraction(fraction)
        return fraction

    def _add_fraction(self, fraction: Fraction):
        self.fractions.append(fraction)

    def get_fraction_by_name(self, name: str) -> Fraction:
        for fraction in self.fractions:
            if fraction.name == name:
                return fraction
        logging("ERROR", f"fraction by name {name} not found", "AllFactions.get_fraction_by_name")
        return Fraction()

    def get_all_fractions(self) -> list[Fraction]:
        return self.fractions
    
    def get_player_fraction(self) -> Fraction:
        for fraction in self.fractions:
            if fraction.type == "player" and fraction.id == root.player_id:
                return fraction
        logging("ERROR", f"player fraction not found", "AllFactions.get_fraction_by_name")
        return Fraction()

    def get_fraction_by_id(self, id: int) -> Fraction:
        for fraction in self.fractions:
            if fraction.id == id:
                return fraction
        logging("ERROR", f"fraction id not found", "AllFactions.get_fraction_by_name")
        return Fraction()

    def edit_fraction(self, name:str="", id:int=0, data:dict={}) -> bool:
        if name == "" and id == 0:
            return False
        for fraction in self.fractions:
            if fraction.name == name or fraction.id == id:
                fraction.edit(data=data)
                return True
        return False