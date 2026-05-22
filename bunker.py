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
            print(f"[SYSTEM LOG]: {self.name} died or went insane...")
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


class BunkerManager:
    def __init__(self, backpack):
        self.day = 0
        storage.init_stocks(backpack)

        known_items = ["Water", "Food", "Medkit", "Axe", "Radio", "Flashlight"]
        self.characters = {}

        factory = CharacterFactory()

        for item in backpack:
            if item not in known_items and item not in self.characters:
                self.characters[item] = factory.create_character(item)

        self.events_pool = [
            BunkerEvent("Raiders are here!", "Axe", "Chased them!", "Lost 1 Water, 1 Food.", "raid"),
            BunkerEvent("Lights out!", "Flashlight", "Fixed it!", "Lost 1 Medkit in dark.", "darkness"),
            BunkerEvent("Mutant bugs attack!", "Axe", "Smashed them!", "Someone got sick.", "infection")
        ]

    def show_status(self):
        print("\n--- STATUS ---")
        print(f"Stocks: {storage.stocks}")
        for c in self.characters.values():
            if c.alive:
                health = "SICK" if c.sick else "OK"
                print(
                    f"{c.name} -> Water debt: {c.water_debt}/3 | Food debt: {c.food_debt}/5 | [{health}] | Depr: {c.depression}/3")


    def feeding_phase(self):
        print("\n--- FEEDING ---")
        for c in self.characters.values():
            if not c.alive: continue

            print(f"\nManaging {c.name}:")

            if not c.is_pet:
                choice_w = input(f"Give WATER to {c.name}? (1-Yes, 0-No): ")
                if choice_w == "1" and storage.get("Water") > 0:
                    storage.change("Water", -1)
                    c.water_debt = 0
                else:
                    c.water_debt += 1
                    if c.water_debt >= 2:
                        c.depression += 1
            else:
                c.water_debt = 0

            choice_f = input(f"Give FOOD to {c.name}? (1-Yes, 0-No): ")
            if choice_f == "1" and storage.get("Food") > 0:
                storage.change("Food", -1)
                c.food_debt = 0
            else:
                c.food_debt += 1
                if c.food_debt >= 3:
                    c.depression += 1

            if c.sick:
                choice_m = input(f"Use Medkit on {c.name}? (1-Yes, 0-No): ")
                if choice_m == "1" and storage.get("Medkit") > 0:
                    storage.change("Medkit", -1)
                    c.sick = False

            c.check_health()

    def run_expedition(self):
        scouts = []
        for c in self.characters.values():
            if c.alive and c.is_pet == False:
                scouts.append(c.name)

        if not scouts: return

        print("\nChoose scout:")
        for i, name in enumerate(scouts):
            print(f"{i + 1} - {name}")

        try:
            index = int(input(">> ")) - 1
            chosen = scouts[index]
            print(f"{chosen} left the bunker on a quick scout run...")

            outcome = random.randint(1, 3)
            if outcome == 1:
                print(f"{chosen} died in the Wasteland.")
                self.characters[chosen].alive = False
            elif outcome == 2:
                print(f"{chosen} returned empty-handed.")
            else:
                print(f"{chosen} returned safely and brought 2 Water, 2 Food!")
                storage.change("Water", 2)
                storage.change("Food", 2)
        except:
            print("Action cancelled.")



#Test
    def automated_feeding_test(self, feed_all=True):
        print("\n--- AUTOMATED FEEDING TEST ---")
        for c in self.characters.values():
            if not c.alive: continue

            print(f"Processing {c.name} (Auto)...")
            if feed_all:
                if not c.is_pet and storage.get("Water") > 0:
                    storage.change("Water", -1)
                    c.water_debt = 0
                elif not c.is_pet:
                    c.water_debt += 1

                if storage.get("Food") > 0:
                    storage.change("Food", -1)
                    c.food_debt = 0
                else:
                    c.food_debt += 1
            else:
                if not c.is_pet:
                    c.water_debt += 1
                c.food_debt += 1

            c.check_health()



#Test
    def automated_expedition_test(self):
        print("\n--- AUTOMATED EXPEDITION TEST ---")
        scouts = [c.name for c in self.characters.values() if c.alive and not c.is_pet]

        if not scouts:
            print("No scouts available.")
            return

        chosen = scouts[0]
        print(f"[AUTO]: Sending {chosen} to the Wasteland...")

        print(f"[AUTO]: {chosen} returned safely and brought 2 Water, 2 Food!")
        storage.change("Water", 2)
        storage.change("Food", 2)







# -------------------------------------------------------------
# THE SYSTEM TEST FOR BUNKER MANAGER

def bunker_phase(backpack):
    print("==================================================")
    print("===      STARTING MANAGER COMPONENT TEST       ===")
    print("==================================================")

    # 1. Initialize the Manager
    print("\n[STEP 1]: Initializing BunkerManager...")
    manager = BunkerManager(backpack)
    manager.show_status()

    # 2. Test Event execution via Manager's pool
    print("\n[STEP 2]: Triggering a random event from the pool...")
    test_event = manager.events_pool[0]  # Raiders event (Needs Axe)
    test_event.execute(list(manager.characters.values()), storage)
    manager.show_status()

    # 2. Тест экспедиции (Проверяем, прибавятся ли ресурсы)
    print("\n[STEP 2]: Simulating an Expedition...")
    print(f"Stocks BEFORE expedition: Water={storage.get('Water')}, Food={storage.get('Food')}")
    manager.automated_expedition_test()
    print(f"Stocks AFTER expedition: Water={storage.get('Water')}, Food={storage.get('Food')}")
    manager.show_status()


    # 3. Test Resources Distribution (Feeding Phase)
    print("\n[STEP 3]: Testing Automated Resource Distribution...")
    manager.automated_feeding_test(feed_all=True)
    manager.show_status()

    # 4. Test Sickness and Penalty Simulation
    print("\n[STEP 4]: Forcing infection penalty test...")
    storage.change("Axe", -storage.get("Axe"))
    infection_event = manager.events_pool[2]
    infection_event.execute(list(manager.characters.values()), storage)
    manager.show_status()

    print("\n==================================================")
    print("===          COMPONENT TEST COMPLETE           ===")
    print("==================================================")


if __name__ == "__main__":
    # Test dataset containing humans, a pet, and a set of utilities
    test_backpack = ["Alex", "Bob", "Pet", "Water", "Water", "Food", "Axe", "Flashlight"]
    bunker_phase(test_backpack)