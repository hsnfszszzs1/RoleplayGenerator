"""
RoleplayGenerator v1.2 - Complex Behavior Tree System

Integrates with:
- MemorySystem v1.2
- AdvancedRoleplayPhysics
- RoleplayEngine

Features:
- Full node types (Sequence, Selector, Parallel, Decorator, Action, Condition)
- Blackboard for shared state
- Memory and Physics aware nodes
- Extensible design
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional
from abc import ABC, abstractmethod
import time


class NodeStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class Blackboard:
    """Shared memory between behavior tree nodes"""
    def __init__(self):
        self.data: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def has(self, key: str) -> bool:
        return key in self.data


class BTNode(ABC):
    """Base class for all behavior tree nodes"""
    def __init__(self, name: str = ""):
        self.name = name or self.__class__.__name__
        self.status = NodeStatus.FAILURE

    @abstractmethod
    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        pass

    def reset(self):
        self.status = NodeStatus.FAILURE


class Composite(BTNode):
    """Base class for composite nodes"""
    def __init__(self, name: str = "", children: List[BTNode] = None):
        super().__init__(name)
        self.children = children or []

    def add_child(self, child: BTNode):
        self.children.append(child)


class Sequence(Composite):
    """Executes children in order. Fails if any child fails."""
    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard, context)
            if status != NodeStatus.SUCCESS:
                self.status = status
                return status
        self.status = NodeStatus.SUCCESS
        return NodeStatus.SUCCESS


class Selector(Composite):
    """Tries children until one succeeds."""
    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        for child in self.children:
            status = child.tick(blackboard, context)
            if status == NodeStatus.SUCCESS:
                self.status = NodeStatus.SUCCESS
                return NodeStatus.SUCCESS
        self.status = NodeStatus.FAILURE
        return NodeStatus.FAILURE


class Parallel(Composite):
    """Runs all children. Succeeds if all succeed."""
    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        results = [child.tick(blackboard, context) for child in self.children]
        if all(r == NodeStatus.SUCCESS for r in results):
            self.status = NodeStatus.SUCCESS
            return NodeStatus.SUCCESS
        if any(r == NodeStatus.FAILURE for r in results):
            self.status = NodeStatus.FAILURE
            return NodeStatus.FAILURE
        self.status = NodeStatus.RUNNING
        return NodeStatus.RUNNING


class Decorator(BTNode):
    """Wraps a single child node"""
    def __init__(self, child: BTNode, name: str = ""):
        super().__init__(name)
        self.child = child

    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        return self.child.tick(blackboard, context)


class Inverter(Decorator):
    """Inverts the result of the child"""
    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        status = self.child.tick(blackboard, context)
        if status == NodeStatus.SUCCESS:
            return NodeStatus.FAILURE
        if status == NodeStatus.FAILURE:
            return NodeStatus.SUCCESS
        return status


class Action(BTNode):
    """Leaf node that performs an action"""
    def __init__(self, name: str, action_func: Callable[[Blackboard, Dict], NodeStatus]):
        super().__init__(name)
        self.action_func = action_func

    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        self.status = self.action_func(blackboard, context)
        return self.status


class Condition(BTNode):
    """Leaf node that checks a condition"""
    def __init__(self, name: str, condition_func: Callable[[Blackboard, Dict], bool]):
        super().__init__(name)
        self.condition_func = condition_func

    def tick(self, blackboard: Blackboard, context: Dict) -> NodeStatus:
        result = self.condition_func(blackboard, context)
        self.status = NodeStatus.SUCCESS if result else NodeStatus.FAILURE
        return self.status


class BehaviorTree:
    """Main Behavior Tree class"""
    def __init__(self, root: BTNode, name: str = "BehaviorTree"):
        self.root = root
        self.name = name
        self.blackboard = Blackboard()

    def tick(self, context: Dict = None) -> NodeStatus:
        if context is None:
            context = {}
        return self.root.tick(self.blackboard, context)

    def reset(self):
        self.blackboard = Blackboard()


# ====================== ROLEPLAY-SPECIFIC NODES ======================

def create_memory_condition(memory_system, query: str, min_importance: float = 4.0):
    """Returns a Condition node that checks for relevant memories"""
    def check(blackboard, context):
        memories = memory_system.get_relevant_memories(query=query, limit=3)
        return any(m.get("importance", 0) >= min_importance for m in memories)
    return Condition(f"HasMemory({query})", check)


def create_physics_action(physics, shift_dict: Dict):
    """Returns an Action that modifies emotional physics"""
    def action(blackboard, context):
        physics.apply_shift(**shift_dict)
        return NodeStatus.SUCCESS
    return Action("ApplyEmotionalShift", action)


def create_memory_action(memory_system, content: str, importance: float = 5.0, emotion: str = "neutral"):
    """Returns an Action that adds a memory"""
    def action(blackboard, context):
        memory_system.add_memory(content=content, importance=importance, emotion=emotion)
        return NodeStatus.SUCCESS
    return Action("AddMemory", action)


# Example: Create a simple NPC behavior tree
def create_example_npc_tree(memory_system, physics):
    """Example behavior tree for an NPC"""
    root = Selector("Root")

    # High priority: React to strong emotions in memory
    emotional_reaction = Sequence("EmotionalReaction")
    emotional_reaction.add_child(create_memory_condition(memory_system, "angry OR tension", min_importance=6))
    emotional_reaction.add_child(create_physics_action(physics, {"tension": +2, "intensity": +1}))

    # Default: Idle / Observe
    idle = Sequence("IdleBehavior")
    idle.add_child(create_memory_action(memory_system, "NPC is observing the situation", importance=2.0))
    idle.add_child(create_physics_action(physics, {"tension": -0.5}))

    root.add_child(emotional_reaction)
    root.add_child(idle)

    return BehaviorTree(root, name="ExampleNPCBehavior")
