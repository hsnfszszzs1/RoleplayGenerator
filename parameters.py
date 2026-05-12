"""
RoleplayGenerator v1.0 - Parameters System
Inspired by HumanBodyRemodeler Custom Precision Mode v1.9
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Union

@dataclass
class RoleplayParameters:
    # === Character Parameters ===
    character_name: str = "Unknown"
    personality_traits: str = "mysterious, teasing, dominant"
    speech_style: str = "casual with sarcastic undertones"
    background: str = "ancient vampire living in modern city"

    # === Scenario Parameters ===
    setting: str = "modern night club"
    mood: str = "intense and seductive"
    relationship_dynamic: str = "enemies to lovers"
    scenario_description: str = "First meeting after years of rivalry"

    # === Roleplay Physics (analog to Skin/Hair Physics) ===
    emotional_intensity: Union[int, str] = 75          # 0-100 or "+15%"
    sexual_tension: Union[int, str] = 60
    power_dynamic: str = "dominant leans slightly submissive"
    pacing: str = "slow burn with sudden spikes"
    plot_progression_speed: Union[int, str] = 40

    # === Style & Constraints ===
    dialogue_style: str = "teasing, confident, occasionally vulgar"
    response_length: str = "medium (2-4 paragraphs)"
    keep_in_character: bool = True
    avoid_ooc: bool = True

    # === Advanced (like % and fixed deltas) ===
    intensity_modifier: str = "+10%"   # Can be "+15%" or fixed like "85"

    # === New Systems (Memory + Consistency) ===
    enable_memory: bool = True
    enable_consistency: bool = True
    consistency_target: int = 90       # Target consistency score

    # === Multi-Character ===
    is_multi_character: bool = False
    active_character_name: str = ""

    def update(self, **kwargs):
        """Update parameters (supports both % and fixed values)"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}

    def get_prompt_context(self) -> str:
        """Generate context string for LLM prompt"""
        return f"""
Character: {self.character_name}
Personality: {self.personality_traits}
Speech: {self.speech_style}
Setting: {self.setting}
Mood: {self.mood}
Relationship: {self.relationship_dynamic}
Emotional Intensity: {self.emotional_intensity}
Sexual Tension: {self.sexual_tension}
Power Dynamic: {self.power_dynamic}
Pacing: {self.pacing}
"""