from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType
from weapon_types import WeaponType

if TYPE_CHECKING:
    from entity import Actor, Item


class Equipment(BaseComponent):
    parent: Actor

    def __init__(self,

    weapon: Optional[Item] = None,
    ranged: Optional[Item] = None,
    melee: Optional[Item] = None,
    range: Optional[Item] = None,

    armor: Optional[Item] = None, 
    accessory: Optional[Item] = None,
    ):
        self.weapon = weapon
        self.ranged = ranged
        self.melee = melee

        self.armor = armor
        self.accessory = accessory

    @property
    def attack_value(self) -> int:
        wep_attack = 0

        if self.weapon is not None and self.weapon.equippablewep is not None:
            wep_attack += self.weapon.equippablewep.attack_value

    @property
    def defense_bonus(self) -> int:
        bonus = 0

        if self.armor is not None and self.armor.equippable is not None:
            bonus += self.armor.equippable.defense_bonus

        if self.accessory is not None and self.accessory.equippable is not None:
            bonus += self.accessory.equippable.defense_bonus

        return bonus

    def item_is_equipped(self, item: Item) -> bool:
        return self.weapon == item or self.armor == item or self.accessory == item

    def unequip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You remove the {item_name}."
        )

    def equip_message(self, item_name: str) -> None:
        self.parent.gamemap.engine.message_log.add_message(
            f"You equip the {item_name}."
        )

    def equip_to_slot(self, slot: str, item: Item, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if current_item is not None:
            self.unequip_from_slot(slot, add_message)

        setattr(self, slot, item)

        if add_message:
            self.equip_message(item.name)

    def unequip_from_slot(self, slot: str, add_message: bool) -> None:
        current_item = getattr(self, slot)

        if add_message:
            self.unequip_message(current_item.name)

        setattr(self, slot, None)

    def toggle_equip(self, equippable_item: Item, add_message: bool = True) -> None:
        if (
            equippable_item.equippablewep
            and equippable_item.equippablewep.equipment_type == EquipmentType.WEAPON
        ):
            slot = "weapon"
        elif (
            equippable_item.equippable
            and equippable_item.equippable.equipment_type == EquipmentType.ARMOR
        ):
            slot = "armor"
        else:
            slot = "accessory"

        if getattr(self, slot) == equippable_item:
            self.unequip_from_slot(slot, add_message)
        else:
            self.equip_to_slot(slot, equippable_item, add_message)