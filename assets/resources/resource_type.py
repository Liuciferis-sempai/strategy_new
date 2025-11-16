class ResourceType:
    def __init__(self, data:dict, amout:int):
        self.name = data.get("name", "")
        self.desc = data.get("desc", "")
        self.max_amout = data.get("max_amout", 1)
        self.amout = amout if amout <= self.max_amout else self.max_amout
        self.is_food = data.get("is_food", False)
        self.food_value = data.get("food_value", 0)
    
    def add(self, amout:int) -> int:
        if self.amout + amout <= self.max_amout:
            self.amout += amout
            return 0
        else:
            amout = self.amout + amout - self.max_amout
            self.amout = self.max_amout
            return amout
    
    def take(self, amout:int) -> bool:
        if self.amout - amout >= 0:
            self.amout -= amout
            return True
        else:
            return False