from scavenge import scavenge_phase
from bunker import bunker_phase


def main():
    print("        WELCOME TO 60 SECONDS          ")

    backpack = scavenge_phase()

    if not backpack:
        print("\nYour backpack is empty! You died outside the bunker")
        print("GAME OVER")
        return

    bunker_phase(backpack)


if __name__ == "__main__":
    main()