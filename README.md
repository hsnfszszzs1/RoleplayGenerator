# RoleplayGenerator v1.2

**Advanced Modular Roleplay Engine** with Memory, Emotional Physics, Behavior Trees, and Hybrid AI.

A powerful Python framework for building deep, emotionally aware, and dynamic roleplay experiences.

## ✨ Key Features (v1.2)

- **MemorySystem v1.2** — Emotional tagging, relationship tracking, decay, clustering, and smart retrieval
- **RoleplayEngine v3** — Central orchestrator with plugin system, hooks, and component registry
- **Advanced Roleplay Physics** — Emotional state (tension, intensity, arousal), relationship influence
- **Behavior Trees** — Structured NPC behaviors with visualization & debugging tools
- **Hybrid AI** — Utility-based decision making + Behavior Tree execution
- **MemoryAware Prompt Builder** — Automatic injection of memories, relationships, and emotional state
- **WaidrinAdapter v2** — Deep integration support for p-e-w/waidrin

## Architecture
RoleplayGenerator/
├── RoleplayEngine          ← Central orchestrator (v3)
├── MemorySystem v1.2       ← Emotional + relational memory
├── AdvancedRoleplayPhysics ← Emotional & relationship dynamics
├── BehaviorTree            ← Structured execution
├── Hybrid AI               ← Utility AI + Behavior Trees
├── MemoryAwarePromptBuilder
└── WaidrinAdapter v2
## Quick Start

```python
from roleplay_engine import RoleplayEngine, RoleplayConfig

config = RoleplayConfig(
    character_name="Elara",
    scenario="A mysterious encounter in a fantasy tavern",
    debug=True
)

engine = RoleplayEngine(config)

# Add important memory
engine.add_memory("Elara is suspicious of strangers", importance=7.0, emotion="suspicion")

# Run interaction
result = engine.step("Hello there, stranger...")
print(result["response"])
Project Structure
File
Purpose
memory.py
MemorySystem v1.2
roleplay_engine.py
Main unified engine
behavior_tree.py
Behavior Tree system
hybrid_ai.py
Hybrid AI (Utility + BT)
waidrin_adapter_v2.py
Waidrin integration
prompt_poet_v2.py
Enhanced prompt builder
Recommended Ecosystem
p-e-w/waidrin — Primary state machine engine
character-ai/prompt-poet — Prompt templating inspiration
Status
Version: v1.2 (Major Architecture Upgrade)
Date: May 2026
