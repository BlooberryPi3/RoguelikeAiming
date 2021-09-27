from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import actions
import color
import components.inventory
import components.ai
from components.base_component import BaseComponent
from exceptions import Impossible
from input_handlers import (
    ActionOrHandler,
    AreaRangedAttackHandler,
    SingleRangedAttackHandler,
    TargetingEventHandler,
    InventoryActivateHandler,
)

if TYPE_CHECKING:
    from entity import Entity, Actor
    from engine import Engine

class Attack(BaseComponent):
    parent: Actor

    def activate(self, action: actions.TargetingAction) -> None:
        attacker = action.entity
        target = action.target_actor

        if attacker.equipment.weapon:
            range = attacker.equipment.weapon.equippablewep.weapon_range
        else:
            range = 1
        if target:
            distance = attacker.distance(target.x, target.y)


        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You cannot target an area that you cannot see.")
        if not target:
            raise Impossible("You must select an enemy to target.")
        if not distance <= range:
            raise Impossible(f"Your target is {distance - range} units out of range!")
        if target is attacker:
            raise Impossible("You cannot attack yourself!")
        if target:
            self.engine.message_log.add_message(
                f"You strike at the {target.name}"
            )
            
            self.targetingact(attacker, target)
    
    def targetingact(self, attacker: Actor, target: Actor) -> TargetingEventHandler:
        self.engine.message_log.add_message(
            "Select a target location.", color.needs_target
        )
        TargetingEventHandler()