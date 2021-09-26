from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType
from weapon_types import WeaponType

if TYPE_CHECKING:
    from entity import Item


class EquippableWep(BaseComponent):
    parent: Item

    def __init__(
        self,
        equipment_type: EquipmentType,
        weapon_type: WeaponType,
        weapon_range: int = 0,
        attack_value: int = 0,
    ):
        self.equipment_type = equipment_type
        self.weapon_type = weapon_type
        self.weapon_range = weapon_range
        self.attack_value = attack_value

class Knife(EquippableWep):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            weapon_type=WeaponType.MELEE, 
            weapon_range=1,
            attack_value=1,
            )

class Sword(EquippableWep):
    def __init__(self) -> None:
        super().__init__(
            equipment_type=EquipmentType.WEAPON, 
            weapon_type=WeaponType.MELEE, 
            weapon_range=2,
            attack_value=3,
            )