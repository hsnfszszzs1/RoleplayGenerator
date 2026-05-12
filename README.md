# 🎭 RoleplayGenerator v1.0

**Advanced Custom Roleplay Generator**  
**Model:** Custom Precision Mode (inspired by HumanBodyRemodeler v1.9)  
**Base Framework:** p-e-w/waidrin (state machine + LLM)

## Features
- User-defined parameters (Character, Scenario, Style, Dynamics)
- Support for % and fixed deltas
- "Roleplay Physics" (Emotional Intensity, Tension, Pacing, Power Dynamic)
- Advanced Hair/Skin Physics analog for roleplay
- Web control panel (HTML/JS)
- CLI support
- Ready for integration with waidrin / Risuai / custom LLM

## Quick Start

```bash
# Basic mode
python cli.py

# With Waidrin integration (recommended)
python cli.py --use-waidrin

# Using generators
python -c "
from generators.character_generator import CharacterGenerator
from generators.dialogue_generator import DialogueGenerator
cg = CharacterGenerator()
params = cg.generate_from_preset('dominant_vampire')
dg = DialogueGenerator(params)
print(dg.generate_response('Hello Elias...'))
"
```

## Recommended GitHub Repos (2026)
- **p-e-w/waidrin** → https://github.com/p-e-w/waidrin (Best core engine - state machine)
- **kwaroran/Risuai** → https://github.com/kwaroran/Risuai (Best frontend)
- **character-ai/prompt-poet** → https://github.com/character-ai/prompt-poet (Dynamic prompts)
- **UKPLab/llm-roleplay** → https://github.com/UKPLab/llm-roleplay (Persona-based dialogues)
- **InteractiveNLP-Team/RoleLLM-public** → https://github.com/InteractiveNLP-Team/RoleLLM-public (Advanced roleplay framework)