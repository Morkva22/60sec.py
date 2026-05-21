import random


class Item:
    def __init__(self, name: str):
        self.name = name


class Room:
    def __init__(self, name, description, items):
        self.name = name
        self.description = description
        self.items = items

    def remove_item(self, item_name: str):
        for item in self.items:
            if item.name.lower() == item_name.lower().strip():
                self.items.remove(item)
                return item
        return None

    def has_items(self) -> bool:
        return len(self.items) > 0


ALL_ITEMS = {
    "Kitchen": ["Canned food", "Knife", "Water"],
    "Bathroom": ["Bandages", "Soap"],
    "Bedroom": ["Pistol", "Map"],
}


ROOM_DESCRIPTIONS = {
    "Kitchen": "Smells of rust.",
    "Bathroom": "Wet tiles.",
    "Bedroom": "Dust everywhere.",
}


class RoomFactory:
    @staticmethod
    def create_all():
        rooms = []

        for name, items in ALL_ITEMS.items():
            shuffled = items[:]
            random.shuffle(shuffled)

            chosen = [Item(i) for i in shuffled[: random.randint(1, 3)]]

            rooms.append(
                Room(
                    name=name,
                    description=ROOM_DESCRIPTIONS[name],
                    items=chosen,
                )
            )

        return rooms