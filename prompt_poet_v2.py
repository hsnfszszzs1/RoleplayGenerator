"""
RoleplayGenerator v1.2 - Enhanced Local Prompt Poet
Improved version with deep MemorySystem v1.2 integration.

Supports automatic injection of:
- Relevant memories (smart scoring)
- Relationship context
- Emotional summaries
- Lorebook
"""

from jinja2 import Template
from typing import Dict, Any, Optional
from memory import MemorySystem


class LocalPromptPoetV2:
    """
    Enhanced local Prompt Poet with better templating and memory awareness.
    """

    def __init__(self):
        self.templates: Dict[str, Template] = {}

    def register_template(self, name: str, template_str: str):
        self.templates[name] = Template(template_str, trim_blocks=True, lstrip_blocks=True)

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found.")
        return self.templates[template_name].render(**context)

    def create_advanced_roleplay_template(self) -> str:
        """Advanced roleplay template that works well with MemorySystem v1.2"""
        return """
You are {{ character_name }}.

{% if personality_traits %}Personality: {{ personality_traits }}{% endif %}
{% if speech_style %}Speech Style: {{ speech_style }}{% endif %}
{% if background %}Background: {{ background }}{% endif %}

SCENARIO: {{ scenario }}
SETTING: {{ setting }}
MOOD: {{ mood }}

{% if relationship_context %}
RELATIONSHIPS:
{{ relationship_context }}
{% endif %}

{% if emotional_summary %}
EMOTIONAL STATE: Dominant emotion is {{ emotional_summary.dominant_emotion }} (intensity: {{ emotional_summary.average_intensity }})
{% endif %}

{% if relevant_memories %}
RELEVANT MEMORIES:
{% for mem in relevant_memories %}
- {{ mem.content }} (Importance: {{ mem.importance }}, Emotion: {{ mem.emotion }})
{% endfor %}
{% endif %}

{% if lore_context %}
LORE / WORLD INFO:
{{ lore_context }}
{% endif %}

CURRENT STATE:
- Emotional Intensity: {{ emotional_intensity }}
- Tension: {{ tension }}
- Power Dynamic: {{ power_dynamic }}

Rules:
- Stay fully in character as {{ character_name }}
- Match the current emotional tone and intensity
- Use relationship context when relevant
- Reference memories naturally when they fit the situation
- Keep responses immersive and consistent

Respond only as {{ character_name }}:
"""


class MemoryAwarePromptBuilder:
    """
    Bridge between MemorySystem v1.2 and Prompt Poet.
    Automatically enriches prompts with memory, relationships, and emotional context.
    """

    def __init__(self, memory_system: MemorySystem, prompt_poet: LocalPromptPoetV2):
        self.memory = memory_system
        self.poet = prompt_poet
        self.poet.register_template("advanced_roleplay", self.poet.create_advanced_roleplay_template())

    def build_prompt(self, 
                     character_name: str,
                     user_input: str,
                     scenario: str = "",
                     setting: str = "",
                     mood: str = "neutral",
                     emotional_intensity: float = 5.0,
                     tension: float = 3.0,
                     power_dynamic: str = "balanced",
                     query_for_memories: str = "",
                     limit_memories: int = 5) -> str:
        """
        Build a rich, memory-aware prompt.
        """

        # Get enriched context from MemorySystem
        memory_context = self.memory.get_context_for_waidrin(query=query_for_memories, limit=limit_memories) if hasattr(self.memory, 'get_context_for_waidrin') else {}
        
        relevant_memories = self.memory.get_relevant_memories(query=query_for_memories, limit=limit_memories)
        relationship_context = self.memory.get_relationship_context(character_name)
        lore_context = self.memory.get_lore_context()
        emotional_summary = self.memory._get_emotional_summary() if hasattr(self.memory, '_get_emotional_summary') else {"dominant_emotion": "neutral", "average_intensity": 0.4}

        context = {
            "character_name": character_name,
            "user_input": user_input,
            "scenario": scenario,
            "setting": setting,
            "mood": mood,
            "emotional_intensity": emotional_intensity,
            "tension": tension,
            "power_dynamic": power_dynamic,
            "relevant_memories": relevant_memories,
            "relationship_context": relationship_context,
            "lore_context": lore_context,
            "emotional_summary": emotional_summary
        }

        return self.poet.render("advanced_roleplay", context)
