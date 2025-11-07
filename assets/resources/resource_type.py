class ResourceType:
    def __init__(self, data:dict, amount:int):
        self.name = data.get("name", "")
        self.desc = data.get("desc", "")
        self.max_amount = data.get("max_amount", 1)
        self.amount = amount if amount <= self.max_amount else self.max_amount
        self.is_food = data.get("is_food", False)
        self.food_value = data.get("food_value", 0)
    
    def add(self, amount:int) -> int:
        if self.amount + amount <= self.max_amount:
            self.amount += amount
            return 0
        else:
            amount = self.amount + amount - self.max_amount
            self.amount = self.max_amount
            return amount
    
    def take(self, amount:int) -> bool:
        if self.amount - amount >= 0:
            self.amount -= amount
            return True
        else:
            return False