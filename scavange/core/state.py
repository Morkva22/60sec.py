from __future__ import annotations
from dataclasses import dataclass, field

from scavange.rooms.models import Room, Item


@dataclass
class GameState:
    """Single source of truth for a running game session."""
    rooms: list[Room]         = field(default_factory=list)
    inventory: list[Item]     = field(default_factory=list)
    current_room: Room | None = None
    time_left: float          = 60.0
    running: bool             = False

    _instance: "GameState | None" = field(default=None, init=False, repr=False)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    def reset(self) -> None:
        self.rooms        = []
        self.inventory    = []
        self.current_room = None
        self.time_left    = 60.0
        self.running      = False