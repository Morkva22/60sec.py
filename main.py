from scavange.ui.render import (
    render_main_menu,
    render_rules,
)
from scavange.core.engine import GameEngine


class App:
    """Main application controller."""

    def __init__(self):
        self.running = True

    def run(self) -> None:
        while self.running:
            choice = self._show_main_menu()
            self._handle_main_menu(choice)

    def _show_main_menu(self) -> str:
        render_main_menu()
        return input("  Your choice (1/2/3): ").strip()

    def _handle_main_menu(self, choice: str) -> None:
        match choice:
            case "1":
                self._start_game()

            case "2":
                render_rules()

            case "3":
                self._exit_game()

            case _:
                pass

    def _start_game(self) -> None:
        while True:
            engine = GameEngine()
            engine.start()

            action = engine.handle_game_over_choice()

            match action:
                case "restart":
                    continue

                case "rules":
                    render_rules()
                    break

                case "exit":
                    self.running = False
                    break

                case _:
                    break

    @staticmethod
    def _exit_game() -> None:
        print("\n  Goodbye, survivor.\n")


if __name__ == "__main__":
    App().run()