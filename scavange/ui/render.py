import os
import random
from typing import Iterable

WIDTH = 58


class Renderer:
    """Responsible only for rendering UI."""

    @staticmethod
    def clear_screen() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def line(char: str = "═") -> str:
        return char * WIDTH


renderer = Renderer()


def on_item_picked(data):
    print(f"\n  ✔  Picked up: {data['item']}")


def on_item_not_found(data):
    print(f"\n  ✘  '{data['name']}' — not found here.")


def on_room_entered(data):
    print(f"\n  →  Entering: {data['room']}")


def on_room_exited(data):
    print(f"\n  ←  Left room: {data['room']}")


def on_timer_expired(data):
    print("\n  ⚠  TIME IS UP!\n")


def render_main_menu() -> None:
    renderer.clear_screen()

    print(f"""
  ╔{renderer.line()}╗
  ║{"":^58}║
  ║{"██████╗ ██╗   ██╗███╗  ██╗██╗  ██╗███████╗██████╗":^58}║
  ║{"██╔══██╗██║   ██║████╗ ██║██║ ██╔╝██╔════╝██╔══██╗":^58}║
  ║{"██████╔╝██║   ██║██╔██╗██║█████╔╝ █████╗  ██████╔╝":^58}║
  ║{"SCAVANGE  —  60 seconds. No second chances.":^58}║
  ║{"":^58}║
  ╠{renderer.line()}╣
  ║{"  1  ·  Start Game":<58}║
  ║{"  2  ·  Rules":<58}║
  ║{"  3  ·  Exit":<58}║
  ╚{renderer.line()}╝
""")


def render_rules() -> None:
    renderer.clear_screen()

    print(f"""
  ╔{renderer.line()}╗
  ║{"  R U L E S":^58}║
  ╠{renderer.line()}╣
  ║{"":^58}║
  ║{"  You have 60 seconds to loot the bunker.":<58}║
  ║{"  Move between rooms and pick up items.":<58}║
  ║{"":^58}║
  ║{"  Commands inside a room:":<58}║
  ║{"    <item name>  — pick up the item":<58}║
  ║{"    EXIT         — leave the room":<58}║
  ║{"":^58}║
  ║{"  Items shuffle every run — chaos rules.":<58}║
  ║{"":^58}║
  ╚{renderer.line()}╝
""")

    input("  Press ENTER to go back...")


def render_room_list(rooms, time_left: float = 0.0) -> None:
    renderer.clear_screen()

    print(f"  ╔{renderer.line()}╗")
    print(f"  ║  {'CHOOSE A ROOM':<28}⏱  {time_left:.1f}s{'':<10}║")
    print(f"  ╠{renderer.line()}╣")

    for i, room in enumerate(rooms, start=1):
        print(f"  ║  {i}  ·  {room.name:<12}  {room.description:<32}║")

    print(f"  ╠{renderer.line()}╣")
    print(f"  ║  {'0  ·  Inventory':<58}║")
    print(f"  ╚{renderer.line()}╝")


def render_inventory(inventory) -> None:
    renderer.clear_screen()

    print(f"  ╔{renderer.line()}╗")
    print(f"  ║  {'INVENTORY':<58}║")
    print(f"  ╠{renderer.line()}╣")

    if inventory:
        for item in inventory:
            print(f"  ║  - {item.name:<54}║")
    else:
        print(f"  ║  (empty){'':<50}║")

    print(f"  ╚{renderer.line()}╝")


def render_room_chaos(room, time_left: float) -> None:
    renderer.clear_screen()

    print(f"  ╔{renderer.line()}╗")
    print(f"  ║ ROOM: {room.name:<20} ⏱ {time_left:.1f}s{'':<10}║")
    print(f"  ║ {room.description:<58}║")
    print(f"  ╠{renderer.line()}╣")

    print("  Items:")
    for item in room.items:
        print(f"  ║  - {item.name}")

    print(f"  ╚{renderer.line()}╝")


def render_game_over(inventory) -> None:
    renderer.clear_screen()

    print(f"  ╔{renderer.line()}╗")
    print(f"  ║  GAME OVER{'':<46}║")
    print(f"  ╠{renderer.line()}╣")

    print(f"  Items collected: {len(inventory)}")

    for item in inventory:
        print(f"  - {item.name}")

    print(f"  ╚{renderer.line()}╝")
