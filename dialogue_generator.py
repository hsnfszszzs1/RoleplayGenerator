"""
RoleplayGenerator v1.0 - Dialogue Generator
Advanced dialogue generation with emotional physics and consistency.
"""

from core.parameters import RoleplayParameters
from core.roleplay_physics import RoleplayPhysics
from core.memory import MemorySystem
from core.consistency import CharacterConsistency
from core.prompt_builder import PromptBuilder
from core.multi_character import MultiCharacterManager

class DialogueGenerator:
    def __init__(self, params: RoleplayParameters, physics: RoleplayPhysics = None,
                 memory: MemorySystem = None, consistency: CharacterConsistency = None,
                 multi_char: MultiCharacterManager = None):
        self.params = params
        self.physics = physics or RoleplayPhysics()
        self.memory = memory or MemorySystem()
        self.consistency = consistency or CharacterConsistency(params.character_name)
        self.multi_char = multi_char
        self.builder = PromptBuilder(params, self.physics, self.memory, self.consistency)

    def generate_response(self, user_input: str, use_waidrin: bool = False) -> str:
        """Generate a response using the full system"""
        if self.multi_char and self.multi_char.active_character:
            # Multi-character mode
            active = self.multi_char.get_active()
            if active:
                self.builder.params = active

        if use_waidrin:
            from integrations.waidrin_adapter import WaidrinAdapter
            adapter = WaidrinAdapter(self.params, self.physics)
            adapter.initialize_session()
            return adapter.send_message(user_input)
        else:
            prompt = self.builder.build_system_prompt()
            return f"[Generated Response for: {user_input}]\n(Using full system: Memory + Consistency + Physics + Prompt Poet)"

    def update_after_response(self, response: str, user_input: str):
        """Update memory and consistency after a response"""
        self.memory.add_memory(f"User: {user_input}", importance=4)
        self.memory.add_memory(f"{self.params.character_name}: {response[:100]}...", importance=5)
        self.consistency.check_response(response)

    def get_status(self) -> dict:
        status = {
            "emotional_state": self.physics.emotional_state,
            "consistency": self.consistency.get_consistency_report(),
            "memory_count": len(self.memory.short_term) + len(self.memory.long_term)
        }
        if self.multi_char:
            status["active_character"] = self.multi_char.active_character
            status["all_characters"] = self.multi_char.get_all_names()
        return status