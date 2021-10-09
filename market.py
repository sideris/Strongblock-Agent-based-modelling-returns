import random


class Market:
    def __init__(self, starting_price=400):
        self.price = starting_price

    def tick(self):
        self.price += self.price * (100 + self.get_pc_change()) / 100

    def get_current_price(self) -> float:
        return self.price

    def get_pc_change(self) -> float:
        if self.price >= 400:
            return random.uniform(-2, 9)
        if self.price >= 500:
            return random.uniform(-3, 6)
        if self.price >= 700:
            return random.uniform(-4, 4)
        if self.price >= 1000:
            return random.uniform(-6, 3)
