import random


class Market:
    def __init__(self, starting_price=400):
        self.price = starting_price
        self.price_history = [starting_price]

    def tick(self):
        change = round(self.get_pc_change(), 2)
        self.price += self.price * change / 100
        self.price = round(self.price, 4)
        self.price_history.append(self.price)

    def get_current_price(self) -> float:
        return self.price

    def get_pc_change(self) -> float:
        if self.price <= 400:
            return random.uniform(-4, 6)
        if self.price <= 500:
            return random.uniform(-2, 5)
        if self.price <= 700:
            return random.uniform(-4, 4)
        if self.price > 700:
            return random.uniform(-6, 3)
