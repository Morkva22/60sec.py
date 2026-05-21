import random
class BunkerStorage:
    def __init__(self):
        self.stocks = {
            "Water": 0,
            "Food": 0,
            "Medkit": 0,
            "Axe": 0,
            "Radio": 0,
            "Flashlight": 0
        }

    def init_stocks(self, backpack):
        for item in backpack:
            if item in self.stocks:
                self.stocks[item] = self.stocks[item] + 1

    def get(self, item):
        return self.stocks.get(item, 0)

    def change(self, item, amount):
        self.stocks[item] = self.stocks[item] + amount
        if self.stocks[item] < 0:
            self.stocks[item] = 0

storage = BunkerStorage()






def bunker_phase(backpack):
    return None


if __name__ == "__main__":
    test_backpack = ["Alex", "Bob", "Pet", "Water", "Water", "Food", "Axe", "Radio", "Flashlight"]
    bunker_phase(test_backpack)

