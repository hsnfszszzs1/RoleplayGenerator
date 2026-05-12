"""
RoleplayGenerator v1.2 - Advanced RoleplayEngine (Unified Core) v3

Central orchestrator integrating:
- MemorySystem v1.2
- AdvancedRoleplayPhysics
- MemoryAwarePromptBuilder
- WaidrinAdapterV2
- Behavior Tree System (with visualization)

Features:
- Plugin/Component system
- Event/Hook system
- Behavior Tree support + debugging
- Session management
"""

from typing import Optional, Dict, Any, Callable, List
from dataclasses import dataclass, field
import uuid

from memory import MemorySystem
from prompt_poet_v2 import MemoryAwarePromptBuilder, LocalPromptPoetV2
from waidrin_adapter_v2 import WaidrinAdapterV2


@dataclass
class RoleplayConfig:
    character_name: str = "Unknown"
    scenario: str = ""
    setting: str = ""
    mood: str = "neutral"
    max_memories_in_prompt: int = 6
    auto_save: bool = False
    save_path: str = "roleplay_session.json"
    debug: bool = False


class RoleplayEngine:
    """
    Advanced Unified Roleplay Engine v3
    """

    def __init__(self, config: RoleplayConfig):
        self.config = config
        self.session_id = str(uuid.uuid4())[:8]
        self.memory = MemorySystem()
        self.components: Dict[str, Any] = {}
        self.hooks: Dict[str, List[Callable]] = {}
        self.session_history: List[Dict] = []
        self.state: Dict[str, Any] = {"turn": 0}

        self._setup_default_components()
        self._initialize_session()

    def _setup_default_components(self):
        self.components["prompt_builder"] = MemoryAwarePromptBuilder(
            self.memory, LocalPromptPoetV2()
        )
        self.components["waidrin_adapter"] = WaidrinAdapterV2(self.memory)

    def _initialize_session(self):
        waidrin = self.components.get("waidrin_adapter")
        if waidrin:
            waidrin.initialize_session(self.config.character_name)
        if self.config.debug:
            print(f"[RoleplayEngine] Session {self.session_id} started")

    # ====================== PLUGIN SYSTEM ======================

    def register_component(self, name: str, component: Any):
        self.components[name] = component
        if self.config.debug:
            print(f"[RoleplayEngine] Component registered: {name}")

    def get_component(self, name: str) -> Any:
        return self.components.get(name)

    # ====================== BEHAVIOR TREE SUPPORT ======================

    def register_behavior_tree(self, name: str, behavior_tree):
        """Register a Behavior Tree"""
        self.components[f"bt_{name}"] = behavior_tree
        if self.config.debug:
            print(f"[RoleplayEngine] Behavior Tree registered: {name}")

    def run_behavior_tree(self, name: str, context: Dict = None, debug: bool = False):
        """Run a registered behavior tree"""
        bt = self.components.get(f"bt_{name}")
        if not bt:
            raise ValueError(f"Behavior Tree '{name}' not found")

        ctx = context or {"character": self.config.character_name}

        if debug:
            return bt.debug_tick(ctx, verbose=True)
        return bt.tick(ctx)

    def visualize_behavior_tree(self, name: str):
        """Print visual representation of a behavior tree"""
        bt = self.components.get(f"bt_{name}")
        if bt:
            print(f"\n=== Behavior Tree: {name} ===")
            bt.print_tree()
        else:
            print(f"Behavior Tree '{name}' not found")

    def get_behavior_tree_status(self, name: str):
        bt = self.components.get(f"bt_{name}")
        return bt.get_tree_status() if bt else None

    # ====================== HYBRID AI SUPPORT (Utility + Behavior Trees) ======================

    def register_hybrid_selector(self, name: str, utility_selector):
        """Register a UtilitySelector for hybrid decision making"""
        self.components[f"hybrid_{name}"] = utility_selector
        if self.config.debug:
            print(f"[RoleplayEngine] Hybrid Selector registered: {name}")

    def run_hybrid_decision(self, name: str, context: Dict = None, debug: bool = False):
        """Run hybrid decision making (Utility AI + optional Behavior Tree)"""
        selector = self.components.get(f"hybrid_{name}")
        if not selector:
            raise ValueError(f"Hybrid Selector '{name}' not found")

        ctx = context or {"character": self.config.character_name}
        from hybrid_ai import run_hybrid_decision as run_hybrid
        return run_hybrid(selector, ctx, debug=debug)

    # ====================== EVENT / HOOK SYSTEM ======================

    def on(self, event: str, callback: Callable):
        if event not in self.hooks:
            self.hooks[event] = []
        self.hooks[event].append(callback)

    def _emit(self, event: str, data: Any = None):
        for callback in self.hooks.get(event, []):
            callback(self, data)

    # ====================== CORE METHODS ======================

    def add_memory(self, content: str, importance: float = 5.0,
                   emotion: str = "neutral", intensity: float = 0.5,
                   tags: List[str] = None, memory_type: str = "event"):
        entry = self.memory.add_memory(
            content=content,
            importance=importance,
            emotion=emotion,
            emotional_intensity=intensity,
            tags=tags or [],
            memory_type=memory_type,
            character=self.config.character_name
        )
        self._emit("memory_added", entry)
        return entry

    def update_relationship(self, other_character: str, **kwargs):
        self.memory.update_relationship(self.config.character_name, other_character, **kwargs)

    def step(self, user_input: str, use_waidrin: bool = False) -> Dict[str, Any]:
        self.state["turn"] += 1
        self.add_memory(content=f"User: {user_input}", importance=4.0)

        prompt_builder = self.components["prompt_builder"]
        prompt = prompt_builder.build_prompt(
            character_name=self.config.character_name,
            user_input=user_input,
            scenario=self.config.scenario,
            setting=self.config.setting,
            mood=self.config.mood,
            query_for_memories=user_input,
            limit_memories=self.config.max_memories_in_prompt
        )

        if use_waidrin:
            waidrin = self.components.get("waidrin_adapter")
            context = waidrin.get_context_for_waidrin(user_input) if waidrin else {}
            response = f"[Waidrin response with {len(context.get('memories', []))} memories]"
        else:
            response = f"[{self.config.character_name}] {user_input}... (response)"

        turn_result = {
            "turn": self.state["turn"],
            "user_input": user_input,
            "response": response
        }
        self.session_history.append(turn_result)
        self._emit("turn_complete", turn_result)
        return turn_result

    def get_context(self) -> Dict:
        return {
            "session_id": self.session_id,
            "config": self.config,
            "state": self.state,
            "memory": self.memory.to_dict(),
            "components": list(self.components.keys()),
            "turns": len(self.session_history)
        }

    def save(self, path: Optional[str] = None):
        path = path or self.config.save_path
        self.memory.save(path)

    def load(self, path: Optional[str] = None):
        path = path or self.config.save_path
        self.memory.load(path)

    def __repr__(self):
        return f"<RoleplayEngine id={self.session_id} turns={len(self.session_history)}>"
