from __future__ import annotations

from typing import TYPE_CHECKING

import color
import components.ai
from components.base_component import BaseComponent
from render_order import RenderOrder
from limb_types import LimbType

if TYPE_CHECKING:
    from entity import Actor

class BodyParts(BaseComponent):
    parent: Actor

    def __init__(
        self, 
        ihp: int,
        LimbType: LimbType,
        name: str = "<Unnamed>",
        ):
        self.max_individual_hp = ihp
        self.individual_hp = ihp
        self.name = name

    @property
    def ihp(self) -> int:
        return self.individual_hp

    @ihp.setter
    def ihp(self, value: int) -> None:
        self.individual_hp = max(0, min(value, self.max_individual_hp))
        if self.individual_hp == 0 and self.parent.ai:
            self.disabled()

    def disabled(self) -> None:
        if self.engine.player is self.parent:
            disabled_message = f"Your {self.name} has been disabled!"
            disabled_message_color = color.player_disabled
        else:
            disabled_message = f"The {self.parent.name}s {self.name} has been disabled!"
            disabled_message_color = color.enemy_disabled

        if LimbType.HEAD:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )

        if LimbType.LEFT_ARM:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )
        
        if LimbType.RIGHT_ARM:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )
        
        if LimbType.LEFT_LEG:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )
        
        if LimbType.RIGHT_LEG:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )
        
        if LimbType.EYES:
            self.parent.ai = components.ai.ConfusedEnemy(
            entity=self.parent, previous_ai=self.parent.ai, turns_remaining=1,
            )

        self.engine.message_log.add_message(disabled_message, disabled_message_color)