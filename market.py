import random


class Market:
    def __init__(self, starting_price=400):
        self.day = 0
        self.price = starting_price
        self.price_history = [starting_price]

    def tick(self):
        change = round(self.get_pc_change(), 2)
        self.price += self.price * change / 100
        self.price = round(self.price, 4)
        self.price_history.append(self.price)
        self.day += 1

    def get_current_price(self) -> float:
        return self.price

    def get_pc_change(self) -> float:
        if self.price <= 400:
            return random.uniform(-4, 5)
        if self.price <= 800:
            return random.uniform(-2.3, 3)
        if self.price <= 1100:
            return random.uniform(-4, 4)
        if self.price > 1100:
            return random.uniform(-6, 3)
