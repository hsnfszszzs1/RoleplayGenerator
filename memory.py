"""
RoleplayGenerator v1.0 - Memory & Lorebook System
"""

from typing import List, Dict
from dataclasses import dataclass, field

@dataclass
class MemoryEntry:
    timestamp: str
    content: str
    importance: int = 5          # 1-10
    tags: List[str] = field(default_factory=list)

class MemorySystem:
    def __init__(self, max_short_term: int = 10, max_long_term: int = 50):
        self.short_term: List[MemoryEntry] = []      # Recent messages
        self.long_term: List[MemoryEntry] = []       # Important memories
        self.lorebook: Dict[str, str] = {}           # World info / character facts
        self.max_short_term = max_short_term
        self.max_long_term = max_long_term

    def add_memory(self, content: str, importance: int = 5, tags: List[str] = None):
        entry = MemoryEntry(
            timestamp="now",
            content=content,
            importance=importance,
            tags=tags or []
        )
        self.short_term.append(entry)

        # Move important memories to long-term
        if importance >= 7:
            self.long_term.append(entry)
            if len(self.long_term) > self.max_long_term:
                self.long_term.pop(0)

        # Keep short-term limited
        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)

    def add_lore(self, key: str, content: str):
        """Add world info or character fact"""
        self.lorebook[key] = content

    def get_relevant_memories(self, query: str = "", limit: int = 5) -> List[str]:
        """Return most relevant memories (simple keyword match for now)"""
        all_memories = self.short_term + self.long_term
        if not query:
            return [m.content for m in all_memories[-limit:]]

        relevant = []
        for mem in all_memories:
            if any(tag.lower() in query.lower() for tag in mem.tags) or query.lower() in mem.content.lower():
                relevant.append(mem.content)
        return relevant[-limit:] if relevant else [m.content for m in all_memories[-limit:]]

    def get_lore_context(self) -> str:
        if not self.lorebook:
            return ""
        return "\n".join([f"[{k}]: {v}" for k, v in self.lorebook.items()])

    def to_dict(self) -> Dict:
        return {
            "short_term": [m.content for m in self.short_term],
            "long_term": [m.content for m in self.long_term],
            "lorebook": self.lorebook
        }