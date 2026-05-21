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


class BunkerEvent:
    def __init__(self, text, item_needed, win_text, lose_text, event_type):
        self.text = text
        self.item_needed = item_needed
        self.win_text = win_text
        self.lose_text = lose_text
        self.event_type = event_type

    def execute(self, characters, storage):
        print(f"\n[EVENT]: {self.text}")
        if self.item_needed and storage.get(self.item_needed) > 0:
            storage.change(self.item_needed, -1)
            print(f"Success! You used: {self.item_needed}")
            print(self.win_text)
        elif self.item_needed:
            print(f"Failure! {self.lose_text}")
            self.apply_penalty(characters, storage)
        else:
            print(self.win_text)

    def apply_penalty(self, characters, storage):
        if self.event_type == "raid":
            storage.change("Water", -1)
            storage.change("Food", -1)
        elif self.event_type == "darkness":
            storage.change("Medkit", -1)
        elif self.event_type == "infection":
            alive_humans = [c for c in characters if c.alive and not c.is_pet]
            if alive_humans:
                target = random.choice(alive_humans)
                target.sick = True
                print(f"Warning: {target.name} is now sick!")


def bunker_phase(backpack):
    return None


if __name__ == "__main__":
    test_backpack = ["Alex", "Bob", "Pet", "Water", "Water", "Food", "Axe", "Radio", "Flashlight"]
    bunker_phase(test_backpack)

