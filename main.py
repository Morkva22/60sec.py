from scavenge import scavenge_phase
from bunker import SurvivalFacade

def main():
    print("          WELCOME TO 60 SECONDS          ")


    backpack = scavenge_phase()

    if not backpack:
        print("\nYour backpack is empty! You didn't save anyone.")
        print("GAME OVER")
        return

    facade = SurvivalFacade(backpack)
    facade.start_survival()

if __name__ == "__main__":
    main()