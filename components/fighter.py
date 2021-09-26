from __future__ import annotations

from typing import TYPE_CHECKING

import color
from components.base_component import BaseComponent
from render_order import RenderOrder

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    parent: Actor

    def __init__(self, hpt: int, base_defense: int, base_attack: int):
        self.max_hp = hpt
        self._hp = hpt
        self.base_defense = base_defense
        self.base_power = base_attack

    @property
    def hpt(self) -> int:
        #max_total_ihp = sum(part.max_individual_hp for part in self.parent.bodyparts.values())
        #print(max_total_ihp)
        return self._hp

    @hpt.setter
    def hpt(self, value: int) -> None:
        hpthreshold = self.max_hp
        self._hp = sum(part.individual_hp for part in self.parent.bodyparts.values())
        print("HP", self._hp)
        if self._hp <= hpthreshold and self.parent.ai:
            self.die()

    @property
    def defense(self) -> int:
        return self.base_defense + self.defense_bonus

    @property
    def attack(self) -> int:
        return self.base_power #+ self.power_bonus

    @property
    def defense_bonus(self) -> int:
        if self.parent.equipment:
            return self.parent.equipment.defense_bonus
        else:
            return 0

    #@property
    #def power_bonus(self) -> int:
    #    if self.parent.equipment:
    #        return self.parent.equipment.power_bonus
    #    else:
    #        return 0

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
        

    def heal(self, amount: int) -> int:
        if self.hp == self.max_hp:
            return 0

        new_hp_value = self.hp + amount

        if new_hp_value > self.max_hp:
            new_hp_value = self.max_hp

        amount_recovered = new_hp_value - self.hp

        self.hp = new_hp_value

        return amount_recovered

    def take_damage(self, amount: int) -> None:
        self.hp -= amount
