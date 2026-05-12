"""
RoleplayGenerator v1.2 - Advanced Memory & Lorebook System
With Emotional Tagging, Relationship Graph, Clustering & Enhanced Retrieval
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Literal, Tuple
from datetime import datetime
import json
import os


MemoryType = Literal["event", "fact", "emotion", "relationship", "observation"]
Emotion = Literal["neutral", "joy", "anger", "sadness", "fear", "desire", "trust", "surprise", "disgust"]


@dataclass
class MemoryEntry:
    timestamp: str
    content: str
    importance: float = 5.0
    tags: List[str] = field(default_factory=list)
    memory_type: MemoryType = "event"
    character: Optional[str] = None
    emotion: Emotion = "neutral"
    emotional_intensity: float = 0.5
    decay_rate: float = 0.98

    def age_in_minutes(self) -> float:
        try:
            return (datetime.now() - datetime.fromisoformat(self.timestamp)).total_seconds() / 60
        except:
            return 0.0

    def apply_decay(self):
        age_hours = self.age_in_minutes() / 60
        effective_decay = self.decay_rate ** (age_hours * (1.0 - self.emotional_intensity * 0.5))
        self.importance = max(1.0, self.importance * effective_decay)


@dataclass
class Relationship:
    character_a: str
    character_b: str
    trust: float = 0.5
    affection: float = 0.0
    tension: float = 0.0
    notes: str = ""


class RelationshipTracker:
    def __init__(self):
        self.relationships: Dict[Tuple[str, str], Relationship] = {}

    def update_relationship(self, char_a: str, char_b: str, 
                            trust_delta: float = 0.0, 
                            affection_delta: float = 0.0,
                            tension_delta: float = 0.0,
                            note: str = ""):
        key = tuple(sorted([char_a, char_b]))
        if key not in self.relationships:
            self.relationships[key] = Relationship(char_a, char_b)
        
        rel = self.relationships[key]
        rel.trust = max(0.0, min(1.0, rel.trust + trust_delta))
        rel.affection = max(-1.0, min(1.0, rel.affection + affection_delta))
        rel.tension = max(0.0, min(1.0, rel.tension + tension_delta))
        if note:
            rel.notes += f" | {note}"

    def get_relationship_context(self, character: str) -> str:
        context_lines = []
        for (a, b), rel in self.relationships.items():
            if character in (a, b):
                other = b if a == character else a
                context_lines.append(
                    f"{character} & {other}: Trust={rel.trust:.1f}, Affection={rel.affection:.1f}, Tension={rel.tension:.1f}"
                )
        return "\n".join(context_lines) if context_lines else ""


class MemorySystem:
    def __init__(self, max_short_term: int = 12, max_long_term: int = 60, decay_enabled: bool = True):
        self.short_term: List[MemoryEntry] = []
        self.long_term: List[MemoryEntry] = []
        self.lorebook: Dict[str, Dict] = {}
        self.relationships = RelationshipTracker()
        self.max_short_term = max_short_term
        self.max_long_term = max_long_term
        self.decay_enabled = decay_enabled

    def add_memory(self, content: str, importance: float = 5.0,
                   tags: Optional[List[str]] = None,
                   memory_type: MemoryType = "event",
                   character: Optional[str] = None,
                   emotion: Emotion = "neutral",
                   emotional_intensity: float = 0.5) -> MemoryEntry:

        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            content=content,
            importance=importance,
            tags=tags or [],
            memory_type=memory_type,
            character=character,
            emotion=emotion,
            emotional_intensity=emotional_intensity
        )
        self.short_term.append(entry)

        if importance >= 7.0:
            self.long_term.append(entry)
            if len(self.long_term) > self.max_long_term:
                self.long_term.pop(0)

        if len(self.short_term) > self.max_short_term:
            self.short_term.pop(0)

        return entry

    def add_lore(self, key: str, content: str, tags: List[str] = None, category: str = "general"):
        self.lorebook[key] = {
            "content": content,
            "tags": tags or [],
            "category": category,
            "timestamp": datetime.now().isoformat()
        }

    def _score_memory(self, memory: MemoryEntry, query: str) -> float:
        score = 0.0
        q = query.lower()
        if q in memory.content.lower():
            score += 5.0
        for tag in memory.tags:
            if tag.lower() in q:
                score += 3.5
                break
        if memory.emotion != "neutral":
            score += memory.emotional_intensity * 2.0
        age = memory.age_in_minutes()
        score += max(0, 3.0 - (age / 90))
        score += memory.importance * 0.7
        return score

    def get_relevant_memories(self, query: str = "", limit: int = 6, 
                              character: Optional[str] = None) -> List[Dict]:
        if self.decay_enabled:
            for m in self.short_term + self.long_term:
                m.apply_decay()

        memories = self.short_term + self.long_term
        if character:
            memories = [m for m in memories if m.character == character or m.character is None]

        if not query:
            memories.sort(key=lambda m: (m.importance, -m.age_in_minutes()), reverse=True)
        else:
            scored = [(m, self._score_memory(m, query)) for m in memories]
            scored.sort(key=lambda x: x[1], reverse=True)
            memories = [m for m, s in scored if s > 0.3]

        return [
            {
                "content": m.content,
                "importance": round(m.importance, 1),
                "emotion": m.emotion,
                "intensity": m.emotional_intensity,
                "type": m.memory_type,
                "character": m.character,
                "tags": m.tags
            }
            for m in memories[:limit]
        ]

    def get_memories_by_emotion(self, emotion: Emotion, limit: int = 5) -> List[Dict]:
        memories = [m for m in (self.short_term + self.long_term) if m.emotion == emotion]
        memories.sort(key=lambda m: m.emotional_intensity, reverse=True)
        return [{"content": m.content, "intensity": m.emotional_intensity} for m in memories[:limit]]

    def update_relationship(self, char_a: str, char_b: str, **kwargs):
        self.relationships.update_relationship(char_a, char_b, **kwargs)

    def get_relationship_context(self, character: str) -> str:
        return self.relationships.get_relationship_context(character)

    def cluster_memories(self, similarity_threshold: float = 0.6) -> List[List[MemoryEntry]]:
        clusters = []
        used = set()
        for i, mem1 in enumerate(self.short_term):
            if i in used: continue
            cluster = [mem1]
            used.add(i)
            for j, mem2 in enumerate(self.short_term):
                if j in used or i == j: continue
                common_words = set(mem1.content.lower().split()) & set(mem2.content.lower().split())
                if len(common_words) >= 3:
                    cluster.append(mem2)
                    used.add(j)
            if len(cluster) > 1:
                clusters.append(cluster)
        return clusters

    def save(self, filepath: str = "memory_state.json"):
        data = {
            "short_term": [asdict(m) for m in self.short_term],
            "long_term": [asdict(m) for m in self.long_term],
            "lorebook": self.lorebook
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[MemorySystem v1.2] Saved to {filepath}")

    def load(self, filepath: str = "memory_state.json"):
        if not os.path.exists(filepath):
            print("[MemorySystem v1.2] No save file found.")
            return
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.short_term = [MemoryEntry(**m) for m in data.get("short_term", [])]
        self.long_term = [MemoryEntry(**m) for m in data.get("long_term", [])]
        self.lorebook = data.get("lorebook", {})
        print(f"[MemorySystem v1.2] Loaded from {filepath}")

    def to_dict(self) -> Dict:
        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term),
            "lorebook_count": len(self.lorebook),
            "relationships_tracked": len(self.relationships.relationships)
                            }
