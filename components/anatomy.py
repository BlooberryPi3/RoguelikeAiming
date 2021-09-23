from __future__ import annotations
from components.fighter import Fighter
from components.fighter import BodyParts

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Anatomy(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.fighter: List[BodyParts] = []