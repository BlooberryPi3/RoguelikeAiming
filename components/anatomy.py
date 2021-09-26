from __future__ import annotations
from components.bodyparts import BodyParts

from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Anatomy(BaseComponent):
    parent: Actor

    def __init__(self):
        self.fighter: List[BodyParts] = []