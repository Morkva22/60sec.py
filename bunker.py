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

class Character:
    def __init__(self, name, is_pet):
        self.name = name
        self.is_pet = is_pet
        self.alive = True
        self.water_debt = 0
        self.food_debt = 0
        self.sick = False
        self.depression = 0

    def check_health(self):
        if not self.alive:
            return False


        if (self.water_debt >= 3 and not self.is_pet) or self.food_debt >= 5 or self.depression >= 3:
            print(f"{self.name} died or went insane...")
            self.alive = False
        return self.alive


class CharacterFactory:
    def create_character(self, name):
        low_name = name.lower()
        if low_name == "pet" or low_name == "dog" or low_name == "cat":
            return Character(name, True)
        return Character(name, False)


def bunker_phase(backpack):
    return None


if __name__ == "__main__":
    test_backpack = ["Alex", "Bob", "Pet", "Water", "Water", "Food", "Axe", "Radio", "Flashlight"]
    bunker_phase(test_backpack)

