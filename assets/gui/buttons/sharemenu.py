from .sample import Button
from ... import root

class InventoryCellButton(Button):
    def __init__(self, width: int, height: int, resource_name: str, resource_amount: int, img: str):
        super().__init__(width=width, height=height, img=img, text="")
        self.resource_name = resource_name
        self.resource_amount = resource_amount
    
    def click(self):
        super().click()