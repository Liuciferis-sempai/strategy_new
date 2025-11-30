import pygame as py
from ... import root
from typing import Any
import copy
import math

class PolicyStack:
    def __init__(self, data: dict):
        data = copy.deepcopy(data)
        
        self.id = data.get("id", "unknow")
        self.cards = data.get("cards", [])