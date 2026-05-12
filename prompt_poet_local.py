"""
RoleplayGenerator v1.0 - Local Prompt Poet Implementation
Inspired by character-ai/prompt-poet (https://github.com/character-ai/prompt-poet)

This is a lightweight local version using Jinja2 + YAML-style templates.
No external dependencies needed beyond what's already installed.
"""

from jinja2 import Template
from typing import Dict, Any

class LocalPromptPoet:
    """
    Local implementation of Prompt Poet style prompt building.
    Uses Jinja2 templating with YAML-like structure.
    """

    def __init__(self):
        self.templates = {}

    def register_template(self, name: str, template_str: str):
        """Register a new prompt template"""
        self.templates[name] = Template(template_str)

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with given context"""
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        return self.templates[template_name].render(**context)

    def create_roleplay_template(self) -> str:
        """Default roleplay template (Prompt Poet style)"""
        return """You are {{ character_name }}.

{% if personality_traits %}PERSONALITY: {{ personality_traits }}{% endif %}
{% if speech_style %}SPEECH STYLE: {{ speech_style }}{% endif %}
{% if background %}BACKGROUND: {{ background }}{% endif %}

SCENARIO: {{ scenario_description }}
SETTING: {{ setting }}
MOOD: {{ mood }}
RELATIONSHIP: {{ relationship_dynamic }}

CURRENT STATE:
- Emotional Intensity: {{ emotional_intensity }}
- Sexual Tension: {{ sexual_tension }}
- Power Dynamic: {{ power_dynamic }}

{% if memories %}RELEVANT MEMORIES:
{% for mem in memories %}- {{ mem }}
{% endfor %}{% endif %}

{% if lorebook %}LOREBOOK:
{% for key, value in lorebook.items() %}[{{ key }}]: {{ value }}
{% endfor %}{% endif %}

RULES:
- Stay 100% in character
- Never break character
- Match current emotional intensity and tension
- Response length: {{ response_length }}

Respond only as {{ character_name }}."""


# Example usage
if __name__ == "__main__":
    poet = LocalPromptPoet()
    poet.register_template("roleplay", poet.create_roleplay_template())

    context = {
        "character_name": "Elias Voss",
        "personality_traits": "dominant, teasing, sarcastic",
        "speech_style": "confident, low voice",
        "setting": "rainy penthouse",
        "mood": "intense and seductive",
        "emotional_intensity": "75%",
        "sexual_tension": 70,
        "power_dynamic": "dominant",
        "response_length": "medium"
    }

    prompt = poet.render("roleplay", context)
    print(prompt)