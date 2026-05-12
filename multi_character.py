"""
RoleplayGenerator v1.0 - Multi-Character System
Supports multiple characters in the same roleplay session.
"""

from typing import Dict, List, Optional
from core.parameters import RoleplayParameters
from core.roleplay_physics import RoleplayPhysics
from core.memory import MemorySystem

class MultiCharacterManager:
    def __init__(self):
        self.characters: Dict[str, RoleplayParameters] = {}
        self.active_character: Optional[str] = None
        self.physics = RoleplayPhysics()
        self.memory = MemorySystem()
        self.relationship_map = {}  # character_name -> relationship with others

    def add_character(self, name: str, params: RoleplayParameters):
        self.characters[name] = params
        if self.active_character is None:
            self.active_character = name
        print(f"[Multi-Character] Added: {name}")

    def switch_character(self, name: str):
        if name in self.characters:
            self.active_character = name
            print(f"[Multi-Character] Switched to: {name}")
        else:
            print(f"[Multi-Character] Character '{name}' not found!")

    def get_active(self) -> Optional[RoleplayParameters]:
        if self.active_character:
            return self.characters[self.active_character]
        return None

    def get_all_names(self) -> List[str]:
        return list(self.characters.keys())

    def set_relationship(self, char1: str, char2: str, dynamic: str):
        """Set relationship between two characters"""
        key = tuple(sorted([char1, char2]))
        self.relationship_map[key] = dynamic

    def get_relationship(self, char1: str, char2: str) -> str:
        key = tuple(sorted([char1, char2]))
        return self.relationship_map.get(key, "neutral")

    def generate_group_prompt(self) -> str:
        """Generate prompt when multiple characters are present"""
        lines = ["You are in a group roleplay with multiple characters.\n"]
        for name, params in self.characters.items():
            lines.append(f"--- {name} ---")
            lines.append(f"Personality: {params.personality_traits}")
            lines.append(f"Speech: {params.speech_style}")
            lines.append("")
        return "\n".join(lines)