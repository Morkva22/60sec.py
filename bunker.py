import random

class BunkerStorage:
    _instance = None

    def __init__(self):
        self.stocks = {
            "Water": 0, "Food": 0, "Medkit": 0,
            "Axe": 0, "Radio": 0, "Flashlight": 0,
            "Gun": 0, "Map": 0, "Ammo": 0
        }
        self.durability = {
            "Axe": 0, "Radio": 0, "Map": 0
        }

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = BunkerStorage()
        return cls._instance

    def init_stocks(self, backpack):
        for item in backpack:
            if item in self.stocks:
                self.stocks[item] += 1

        for item in ["Axe", "Radio", "Map"]:
            if self.stocks[item] > 0:
                self.durability[item] = self.stocks[item] * 2

    def get(self, item):
        return self.stocks.get(item, 0)

    def use_item_durability(self, item):
        if item in self.durability and self.durability[item] > 0:
            self.durability[item] -= 1
            print(f"[{item}] Used! Durability left: {self.durability[item]}")
            if self.durability[item] % 2 == 0:
                self.stocks[item] -= 1
                print(f"One [{item}] broke!")
            return True
        return False

    def change(self, item, amount):
        if item in self.stocks:
            self.stocks[item] += amount
            if self.stocks[item] < 0:
                self.stocks[item] = 0

            if item in ["Axe", "Radio", "Map"]:
                self.durability[item] = self.stocks[item] * 2


class Character:
    def __init__(self, name, is_pet):
        self.name = name
        self.is_pet = is_pet
        self.alive = True
        self.water_debt = 0
        self.food_debt = 0
        self.sick = False
        self.depression = 0
        self.fed_today = False
        self.watered_today = False
        self.expedition_days_left = 0

    def check_health(self):
        if not self.alive:
            return False

        if self.sick and self.fed_today and self.watered_today:
            print(f"{self.name} has recovered thanks to food and water!")
            self.sick = False

        if self.is_pet:
            if self.food_debt >= 3:
                print(f"Your pet {self.name} died of starvation...")
                self.alive = False
        else:
            if self.water_debt >= 3 or self.food_debt >= 5 or self.depression >= 3:
                print(f"{self.name} died or went insane...")
                self.alive = False
        return self.alive


def create_character(name):
    name_lower = name.lower()
    if name_lower in ["dog", "cat", "pet"]:
        return Character(name, is_pet=True)
    return Character(name, is_pet=False)


class BaseEvent:
    def __init__(self, text):
        self.text = text

    def execute(self, characters):
        pass


class RaidEvent(BaseEvent):
    def execute(self, characters):
        storage = BunkerStorage.get_instance()
        print(f"\n[EVENT]: {self.text}")
        print("1 - Stay quiet\n2 - Fight back\n3 - Bribe them with food/water")
        choice = input("Choice >> ")

        if choice == "1":
            if random.random() < 0.4:
                print("Lucky! The bandits thought the bunker was empty and left.")
            else:
                print("The door was breached! You got raided.")
                storage.change("Water", -2)
                storage.change("Food", -2)
                for c in characters:
                    if c.alive and not c.is_pet: c.depression += 1
        elif choice == "2":
            print("Choose weapon: 1 - Gun (Requires Ammo), 2 - Axe")
            w_choice = input("Weapon >> ")
            if w_choice == "1" and storage.get("Gun") > 0 and storage.get("Ammo") > 0:
                storage.change("Ammo", -1)
                print("Bang! You fought them off perfectly!")
            elif w_choice == "2" and storage.get("Axe") > 0:
                storage.use_item_durability("Axe")
                print("You attacked with the axe! The bandits fled, but the axe took damage.")
            else:
                print("No weapon available! The bandits heavily raided you.")
                storage.change("Water", -3)
                storage.change("Food", -3)
        elif choice == "3":
            if storage.get("Food") >= 2 and storage.get("Water") >= 2:
                storage.change("Food", -2)
                storage.change("Water", -2)
                print("The bandits took the bribe and walked away.")
            else:
                print("Not enough resources for a bribe! The bandits got angry and took everything.")
                storage.change("Food", -4)
                storage.change("Water", -4)


class RatsEvent(BaseEvent):
    def execute(self, characters):
        storage = BunkerStorage.get_instance()
        print(f"\n[EVENT]: {self.text}")
        has_pet = any(c.alive and c.is_pet and c.expedition_days_left == 0 for c in characters)

        if has_pet:
            print("Your pet hunted down all the mutated rats! Food is safe.")
        else:
            print("No pet inside. What will you do?\n1 - Use Axe\n2 - Do nothing")
            choice = input("Choice >> ")
            if choice == "1" and storage.get("Axe") > 0:
                storage.use_item_durability("Axe")
                print("Rats were eliminated with the axe.")
            else:
                print("The rats chewed through your food and infected someone!")
                storage.change("Food", -3)
                humans = [c for c in characters if
                          c.alive and not c.is_pet and not c.sick and c.expedition_days_left == 0]
                if humans:
                    random.choice(humans).sick = True


class RadioEvent(BaseEvent):
    def execute(self, characters):
        storage = BunkerStorage.get_instance()
        print(f"\n[EVENT]: {self.text}")
        if storage.get("Radio") > 0:
            storage.use_item_durability("Radio")
            print("You tuned into a signal! Everyone feels more hopeful.")
        else:
            print("The endless static sounds made the bunker depressing.")
            for c in characters:
                if c.alive: c.depression += 1


class BunkerManager:
    def __init__(self, backpack):
        self.day = 0
        self.storage = BunkerStorage.get_instance()
        self.storage.init_stocks(backpack)

        known_items = ["Water", "Food", "Medkit", "Axe", "Radio", "Flashlight", "Gun", "Map", "Ammo"]
        self.characters = {}

        for item in backpack:
            if item not in known_items and item not in self.characters:
                # ИЗМЕНЕНИЕ 6: Вызываем функцию create_character напрямую
                self.characters[item] = create_character(item)

        self.events_pool = [
            RaidEvent("Armed bandits are banging on the bunker door"),
            RatsEvent("Mutated rats are invading the food containers"),
            RadioEvent("Try to catch an emergency broadcast?")
        ]

    def has_living_humans_inside(self):
        return any(c.alive and not c.is_pet and c.expedition_days_left == 0 for c in self.characters.values())

    def show_status(self):
        print("\n--- STATUS ---")
        dur_info = f"Axe: {self.storage.durability['Axe']} | Radio: {self.storage.durability['Radio']}"
        print(f"Stocks: {self.storage.stocks} ({dur_info})")
        for c in self.characters.values():
            if c.alive:
                if c.expedition_days_left > 0:
                    print(f"{c.name} -> AWAY ON EXPEDITION ({c.expedition_days_left} days left)")
                else:
                    status = "SICK" if c.sick else "OK"
                    if c.is_pet:
                        print(f"{c.name} (PET) -> Food debt: {c.food_debt}/3 | [{status}]")
                    else:
                        print(
                            f"{c.name} -> Water: {c.water_debt}/3 | Food: {c.food_debt}/5 | Depr: {c.depression}/3 | [{status}]")

    def update_expeditions(self):
        for c in self.characters.values():
            if c.alive and c.expedition_days_left > 0:
                c.expedition_days_left -= 1
                if c.expedition_days_left == 0:
                    print(f"\n[EXPEDITION RETURN]: {c.name} has returned!")
                    outcome = random.randint(1, 2)
                    if outcome == 1:
                        print(f"{c.name} returned empty-handed and got sick.")
                        c.sick = True
                    else:
                        w, f = random.randint(1, 2), random.randint(1, 3)
                        print(f"{c.name} brought back: Water +{w}, Food +{f}")
                        self.storage.change("Water", w)
                        self.storage.change("Food", f)

    def feeding_phase(self):
        print("\n------- RESOURCE DISTRIBUTION  -------")
        for c in self.characters.values():
            if not c.alive or c.expedition_days_left > 0: continue

            print(f"\nManaging: {c.name}")
            c.fed_today = False
            c.watered_today = False

            mult = 2 if c.sick else 1

            if not c.is_pet:
                if self.storage.get("Water") > 0:
                    ch = input(f"Give WATER to {c.name}? (1-Yes, 0-No): ")
                    if ch == "1":
                        self.storage.change("Water", -1)
                        c.water_debt = 0
                        c.watered_today = True
                    else:
                        c.water_debt += 1 * mult
                else:
                    print(f"No water left for {c.name}!")
                    c.water_debt += 1 * mult

            if self.storage.get("Food") > 0:
                ch = input(f"Give FOOD to {c.name}? (1-Yes, 0-No): ")
                if ch == "1":
                    self.storage.change("Food", -1)
                    c.food_debt = 0
                    c.fed_today = True
                else:
                    c.food_debt += 1 * mult
            else:
                print(f"No food left for {c.name}!")
                c.food_debt += 1 * mult

            if c.sick and not c.is_pet and self.storage.get("Medkit") > 0:
                ch = input(f"Use Medkit on {c.name}? (1-Yes, 0-No): ")
                if ch == "1":
                    self.storage.change("Medkit", -1)
                    c.sick = False

            c.check_health()

    def run_expedition(self):
        scouts = [c.name for c in self.characters.values() if c.alive and not c.is_pet and c.expedition_days_left == 0]
        if not scouts:
            print("No scouts available.")
            return

        print("\nChoose scout:")
        for i, name in enumerate(scouts):
            print(f"{i + 1} - {name}")

        try:
            idx = int(input(">> ")) - 1
            chosen = scouts[idx]
            self.characters[chosen].expedition_days_left = random.randint(2, 4)
            print(f"{chosen} left for the wasteland.")
        except:
            print("Cancelled.")


class SurvivalFacade:
    def __init__(self, backpack):
        self.game = BunkerManager(backpack)

    def start_survival(self):


#***********************************
        print("      WELCOME TO 60 SECONDS      ")
#***********************************


        while any(c.alive for c in self.game.characters.values()):
            self.game.day += 1
            print(f"\n---------------- DAY {self.game.day} ------------------")

            self.game.update_expeditions()

            if not self.game.has_living_humans_inside():
                print("No living humans left inside to manage the bunker.")
                break

            while True:
                print("\n1-Status | 2-Feed | 3-Expedition | 4-End Day")
                choice = input("Choice >> ")
                if choice == "1":
                    self.game.show_status()
                elif choice == "2":
                    self.game.feeding_phase()
                elif choice == "3":
                    self.game.run_expedition()
                elif choice == "4":
                    break

            if self.game.has_living_humans_inside():
                if random.random() < 0.7:
                    random.choice(self.game.events_pool).execute(list(self.game.characters.values()))
                else:
                    print("\nThe night was quiet.")

            if self.game.day >= 10 and self.game.storage.get("Radio") > 0:
                print("\nYou won! You were rescued by the military via radio signal!")
                return

            input("\nPress ENTER to continue...")

        print(f"\nGAME OVER. Days survived: {self.game.day}")


if __name__ == "__main__":
    mock_backpack = ["Alex", "Mary", "Dog", "Water", "Water", "Food", "Axe", "Radio", "Gun", "Ammo"]

    facade = SurvivalFacade(mock_backpack)
    facade.start_survival()