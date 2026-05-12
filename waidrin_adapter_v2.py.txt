"""
RoleplayGenerator v1.2 - Waidrin Adapter (Enhanced)
Deep integration with p-e-w/waidrin using the new MemorySystem v1.2

This adapter allows RoleplayGenerator's advanced Memory, Relationships,
and emotional tracking to work alongside Waidrin's state machine.
"""

from typing import Optional, Dict, Any
from memory import MemorySystem


class WaidrinAdapterV2:
    """
    Enhanced adapter for deep integration with Waidrin.
    Uses MemorySystem v1.2 for rich context, relationships, and emotional memory.
    """

    def __init__(self, memory_system: MemorySystem):
        self.memory = memory_system
        self.session_state: Dict[str, Any] = {}
        self.current_character: Optional[str] = None

    def initialize_session(self, character_name: str, initial_lore: Dict[str, str] = None):
        """Initialize a new roleplay session with Waidrin"""
        self.current_character = character_name
        self.session_state = {
            "character": character_name,
            "active_memories": [],
            "relationships": {},
            "emotional_state": {},
            "turn_count": 0
        }

        if initial_lore:
            for key, content in initial_lore.items():
                self.memory.add_lore(key, content)

        print(f"[WaidrinAdapter v2] Session initialized for {character_name}")

    def add_memory_from_event(self, content: str, importance: float = 5.0,
                              emotion: str = "neutral", intensity: float = 0.5,
                              tags: list = None, memory_type: str = "event"):
        """Add a memory coming from Waidrin events"""
        self.memory.add_memory(
            content=content,
            importance=importance,
            emotion=emotion,
            emotional_intensity=intensity,
            tags=tags or [],
            memory_type=memory_type,
            character=self.current_character
        )

    def update_character_relationship(self, other_character: str, 
                                      trust_delta: float = 0.0,
                                      affection_delta: float = 0.0,
                                      tension_delta: float = 0.0,
                                      note: str = ""):
        """Update relationship between current character and another"""
        if self.current_character:
            self.memory.update_relationship(
                self.current_character, 
                other_character,
                trust_delta=trust_delta,
                affection_delta=affection_delta,
                tension_delta=tension_delta,
                note=note
            )

    def get_context_for_waidrin(self, query: str = "", limit: int = 6) -> Dict[str, Any]:
        """
        Get enriched context to send to Waidrin's state machine or prompt.
        This is the main integration point.
        """
        relevant_memories = self.memory.get_relevant_memories(query=query, limit=limit)
        relationship_context = self.memory.get_relationship_context(self.current_character or "")
        lore_context = self.memory.get_lore_context()

        context = {
            "memories": relevant_memories,
            "relationships": relationship_context,
            "lore": lore_context,
            "emotional_summary": self._get_emotional_summary(),
            "session_state": self.session_state
        }
        return context

    def _get_emotional_summary(self) -> Dict:
        """Simple emotional summary from recent memories"""
        recent = self.memory.get_relevant_memories(limit=5)
        if not recent:
            return {"dominant_emotion": "neutral", "average_intensity": 0.3}

        from collections import Counter
        emotions = [m.get("emotion", "neutral") for m in recent]
        intensities = [m.get("intensity", 0.5) for m in recent]

        dominant = Counter(emotions).most_common(1)[0][0]
        avg_intensity = sum(intensities) / len(intensities)

        return {
            "dominant_emotion": dominant,
            "average_intensity": round(avg_intensity, 2)
        }

    def process_waidrin_event(self, event: Dict):
        """
        Process an event coming from Waidrin and update memory accordingly.
        This enables bidirectional integration.
        """
        content = event.get("description", "")
        importance = event.get("importance", 5.0)
        emotion = event.get("emotion", "neutral")
        intensity = event.get("intensity", 0.5)

        self.add_memory_from_event(
            content=content,
            importance=importance,
            emotion=emotion,
            intensity=intensity,
            tags=event.get("tags", []),
            memory_type=event.get("type", "event")
        )

        self.session_state["turn_count"] += 1
        self.session_state["last_event"] = event

    def get_full_state_for_waidrin(self) -> Dict:
        """Return complete state ready to be consumed by Waidrin"""
        return {
            "session": self.session_state,
            "memory_context": self.get_context_for_waidrin(),
        }

    def save_session(self, filepath: str = "waidrin_session.json"):
        self.memory.save(filepath)
        print(f"[WaidrinAdapter v2] Session + Memory saved to {filepath}")

    def load_session(self, filepath: str = "waidrin_session.json"):
        self.memory.load(filepath)
        print(f"[WaidrinAdapter v2] Session loaded from {filepath}")
