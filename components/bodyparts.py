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
        #max_hp = sum(part.max_individual_hp for part in self.parent.bodyparts.values())

    @property
    def ihp(self) -> int:
        return self.individual_hp

    def settotal(self) -> None:
        def wrapper():
            if not wrapper.has_run:
                max_hp = sum(part.max_individual_hp for part in self.parent.bodyparts.values())
                wrapper.has_run = True
                return
        wrapper.has_run = False
        return

    @ihp.setter
    def ihp(self, value: int) -> None:
        hpt = self.parent.fighter.hpt
        self.individual_hp = max(0, min(value, self.max_individual_hp))
        if self.individual_hp == 0 and self.parent.ai:
            self.disabled()
        if sum(part.individual_hp for part in self.parent.bodyparts.values()) <= hpt and self.parent.ai:
            self.die()

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

    def heal(self, amount: int) -> int:
        if self.ihp == self.max_individual_hp:
            return 0

        new_ihp_value = self.ihp + amount

        if new_ihp_value > self.max_individual_hp:
            new_ihp_value = self.max_individual_hp

        amount_recovered = new_ihp_value - self.ihp

        self.ihp = new_ihp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.ihp -= amount

    def die(self) -> None:
        if self.engine.player is self.parent:
            death_message = "You died!"
            death_message_color = color.player_die
        else:
            death_message = f"{self.parent.name} is dead!"
            death_message_color = color.enemy_die

        self.parent.char = "%"
        self.parent.color = (191, 0, 0)
        self.parent.blocks_movement = False
        self.parent.ai = None
        self.parent.name = f"remains of {self.parent.name}"
        self.parent.render_order = RenderOrder.CORPSE

        self.engine.message_log.add_message(death_message, death_message_color)

        self.engine.player.level.add_xp(self.parent.level.xp_given)