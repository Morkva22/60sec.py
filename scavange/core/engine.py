"""
GameEngine — orchestrates the 60-second scavenge loop.
All state changes fire through EventBus.notify() — never direct calls.
Pattern: Observer (engine fires events), Singleton (GameState), Factory (RoomFactory)
"""
from __future__ import annotations
import time
from typing import Any

from scavange.events.observer import EventBus, GameEvent, IObserver
from scavange.core.state import GameState
from scavange.rooms.models import RoomFactory, Room
from scavange.ui.render import (
    render_room_list,
    render_room_chaos,
    render_inventory,
    render_game_over,
)


class TimerObserver(IObserver):
    def __init__(self, state: GameState) -> None:
        self._state = state
        EventBus().subscribe(GameEvent.TIMER_TICK, self)

    def on_notify(self, event: GameEvent, payload: dict[str, Any]) -> None:
        if self._state.time_left <= 0:
            self._state.running = False
            EventBus().notify(GameEvent.TIMER_EXPIRED)


class GameEngine:
    """
    Main game controller.
    Wires up observers, manages the room navigation loop,
    and delegates every piece of output to UIObserver / renderers.
    """

    def __init__(self) -> None:
        self._state = GameState()
        self._bus = EventBus()
        self._timer_observer = TimerObserver(self._state)

    def start(self) -> list[str]:
        self._state.reset()
        self._state.rooms = RoomFactory.create_all()
        self._state.running = True

        self._bus.notify(GameEvent.GAME_STARTED)

        start_time = time.time()

        while self._state.running:
            elapsed = time.time() - start_time
            self._state.time_left = max(0.0, 60.0 - elapsed)
            self._bus.notify(GameEvent.TIMER_TICK, {"time_left": self._state.time_left})

            if not self._state.running:
                break

            self._show_room_selection()

        result = [item.name for item in self._state.inventory]
        render_game_over(self._state.inventory)
        return result

    def _show_room_selection(self) -> None:
        render_room_list(self._state.rooms)
        print(f"  ⏱  Time left: {self._state.time_left:.1f}s")
        choice = input("\n  Enter room number (or 0 for inventory): ").strip()

        if choice == "0":
            render_inventory(self._state.inventory)
            input("  Press ENTER to continue...")
            return

        if not choice.isdigit():
            return

        idx = int(choice) - 1
        if 0 <= idx < len(self._state.rooms):
            self._enter_room(self._state.rooms[idx])

    def _enter_room(self, room: Room) -> None:
        self._state.current_room = room
        self._bus.notify(GameEvent.ROOM_ENTERED, {"room": room.name})

        while self._state.running:
            elapsed = time.time()
            render_room_chaos(room, self._state.time_left)

            if not room.has_items():
                print("  (room is empty)")

            cmd = input("  > ").strip()

            if cmd.upper() == "EXIT":
                self._bus.notify(GameEvent.ROOM_EXITED, {"room": room.name})
                self._state.current_room = None
                break

            if cmd:
                item = room.remove_item(cmd)
                if item:
                    self._state.inventory.append(item)
                    self._bus.notify(GameEvent.ITEM_PICKED_UP, {"item": item.name})
                    time.sleep(0.4)
                else:
                    self._bus.notify(GameEvent.ITEM_NOT_FOUND, {"name": cmd})
                    time.sleep(0.4)

            from time import time as _t
            elapsed = _t() - (elapsed)
            self._state.time_left = max(0.0, self._state.time_left)
            self._bus.notify(GameEvent.TIMER_TICK, {"time_left": self._state.time_left})

    @staticmethod
    def handle_game_over_choice() -> str:
        """
        Returns: 'restart' | 'rules' | 'exit'
        """
        while True:
            choice = input("  Your choice (1/2/3): ").strip()
            if choice == "1":
                return "restart"
            if choice == "2":
                return "rules"
            if choice == "3":
                return "exit"
