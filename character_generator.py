"""
RoleplayGenerator v1.0 - Character Generator
Advanced character creation with personality, speech style, and consistency.
"""

from core.parameters import RoleplayParameters
from core.consistency import CharacterConsistency
import random

class CharacterGenerator:
    def __init__(self):
        self.presets = {
            "dominant_vampire": {
                "name": "Elias Voss",
                "personality": "dominant, teasing, sarcastic, secretly caring",
                "speech": "confident, low voice, occasional vulgar",
                "background": "ancient vampire living in modern city"
            },
            "strict_teacher": {
                "name": "Professor Elena Voss",
                "personality": "strict, intelligent, teasing, secretly affectionate",
                "speech": "formal, precise, occasionally sharp",
                "background": "university professor with hidden wild side"
            },
            "tsundere_rival": {
                "name": "Aiko Nakamura",
                "personality": "tsundere, competitive, secretly soft",
                "speech": "sharp, defensive, blushes when flustered",
                "background": "childhood rival turned reluctant ally"
            }
        }

    def generate_from_preset(self, preset_name: str) -> RoleplayParameters:
        if preset_name not in self.presets:
            preset_name = random.choice(list(self.presets.keys()))

        preset = self.presets[preset_name]
        params = RoleplayParameters(
            character_name=preset["name"],
            personality_traits=preset["personality"],
            speech_style=preset["speech"],
            background=preset["background"]
        )
        return params

    def create_custom(self, name: str, personality: str, speech: str, background: str) -> RoleplayParameters:
        return RoleplayParameters(
            character_name=name,
            personality_traits=personality,
            speech_style=speech,
            background=background
        )

    def validate_character(self, params: RoleplayParameters) -> dict:
        """Check character consistency"""
        consistency = CharacterConsistency(params.character_name)
        for trait in params.personality_traits.split(","):
            consistency.add_trait(trait.strip())
        return consistency.get_consistency_report()