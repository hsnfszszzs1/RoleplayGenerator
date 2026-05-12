"""
RoleplayGenerator v1.0 - Scenario Generator
Creates rich scenarios with mood, setting, and relationship dynamics.
"""

from core.parameters import RoleplayParameters
import random

class ScenarioGenerator:
    def __init__(self):
        self.moods = ["intense and seductive", "playful and teasing", "dark and mysterious", "romantic and slow", "tense and charged"]
        self.settings = ["rainy penthouse at midnight", "abandoned library", "luxury hotel suite", "quiet café at closing time", "private jet at 30,000 feet"]
        self.dynamics = ["enemies to lovers", "power imbalance", "friends with benefits", "forbidden attraction", "rivalry turning into obsession"]

    def generate_scenario(self, intensity: int = 70) -> dict:
        return {
            "setting": random.choice(self.settings),
            "mood": random.choice(self.moods),
            "relationship_dynamic": random.choice(self.dynamics),
            "intensity": intensity
        }

    def apply_to_params(self, params: RoleplayParameters, scenario: dict = None) -> RoleplayParameters:
        if scenario is None:
            scenario = self.generate_scenario()

        params.setting = scenario["setting"]
        params.mood = scenario["mood"]
        params.relationship_dynamic = scenario["relationship_dynamic"]
        params.emotional_intensity = f"{scenario['intensity']}%"
        return params