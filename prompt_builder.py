"""
RoleplayGenerator v1.0 - Prompt Builder
Inspired by character-ai/prompt-poet (YAML + Jinja2 style)
"""

from core.parameters import RoleplayParameters
from core.roleplay_physics import RoleplayPhysics
from core.memory import MemorySystem
from core.consistency import CharacterConsistency

class PromptBuilder:
    def __init__(self, params: RoleplayParameters, physics: RoleplayPhysics,
                 memory: MemorySystem = None, consistency: CharacterConsistency = None):
        self.params = params
        self.physics = physics
        self.memory = memory
        self.consistency = consistency

    def build_system_prompt(self) -> str:
        """Main system prompt for the LLM"""
        memory_context = ""
        if self.memory and self.params.enable_memory:
            memory_context = f"\nRELEVANT MEMORIES:\n" + "\n".join(self.memory.get_relevant_memories(limit=4))
            lore = self.memory.get_lore_context()
            if lore:
                memory_context += f"\nLOREBOOK:\n{lore}\n"

        consistency_note = ""
        if self.consistency and self.params.enable_consistency:
            consistency_note = f"\nCHARACTER CONSISTENCY TARGET: {self.params.consistency_target}% (stay in character!)"

        # Use Local Prompt Poet for final rendering
        context = {
            "character_name": self.params.character_name,
            "personality_traits": self.params.personality_traits,
            "speech_style": self.params.speech_style,
            "background": self.params.background,
            "scenario_description": self.params.scenario_description,
            "setting": self.params.setting,
            "mood": self.params.mood,
            "relationship_dynamic": self.params.relationship_dynamic,
            "emotional_intensity": self.params.emotional_intensity,
            "sexual_tension": self.params.sexual_tension,
            "power_dynamic": self.params.power_dynamic,
            "response_length": self.params.response_length,
            "memories": self.memory.get_relevant_memories(limit=4) if self.memory and self.params.enable_memory else [],
            "lorebook": self.memory.lorebook if self.memory and self.params.enable_memory else {}
        }

        return self.poet.render("roleplay", context)

    def build_user_prompt(self, user_input: str) -> str:
        """User message with context"""
        return f"""[Current Scene: {self.params.setting} | Mood: {self.params.mood}]

User: {user_input}

Respond as {self.params.character_name} with appropriate emotional intensity ({self.params.emotional_intensity})."""