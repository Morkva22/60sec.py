from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any


class GameEvent(Enum):
    GAME_STARTED = auto()
    ROOM_ENTERED = auto()
    ROOM_EXITED = auto()
    ITEM_PICKED_UP = auto()
    ITEM_NOT_FOUND = auto()
    TIMER_TICK = auto()
    TIMER_EXPIRED = auto()


class IObserver(ABC):
    @abstractmethod
    def on_notify(self, event: GameEvent, payload: dict[str, Any]) -> None:
        pass


class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def subscribe(self, event: GameEvent, observer: IObserver):
        self._subscribers.setdefault(event, []).append(observer)

    def notify(self, event: GameEvent, payload=None):
        payload = payload or {}
        for obs in self._subscribers.get(event, []):
            obs.on_notify(event, payload)