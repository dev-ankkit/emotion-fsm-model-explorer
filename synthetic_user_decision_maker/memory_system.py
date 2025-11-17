"""
Memory System Module
Implements short-term and long-term memory for synthetic users
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from collections import deque
import json


@dataclass
class MemoryItem:
    """A single memory item"""
    timestamp: datetime
    content: str
    memory_type: str  # 'action', 'observation', 'outcome', 'emotion'
    importance: float = 0.5  # How important this memory is (0-1)
    emotional_valence: float = 0.0  # Positive or negative (-1 to 1)
    context: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0  # How many times this memory was accessed
    decay_rate: float = 0.1  # How quickly this memory fades

    def access(self):
        """Record that this memory was accessed"""
        self.access_count += 1

    def get_strength(self, current_time: datetime) -> float:
        """
        Calculate memory strength based on recency, access count, and importance
        Returns value between 0 and 1
        """
        # Time decay
        time_diff = (current_time - self.timestamp).total_seconds() / 3600  # Hours
        time_factor = max(0.0, 1.0 - (time_diff * self.decay_rate))

        # Access reinforcement
        access_factor = min(1.0, 0.5 + (self.access_count * 0.1))

        # Combined strength
        strength = (time_factor * 0.5 + access_factor * 0.3 + self.importance * 0.2)

        return max(0.0, min(1.0, strength))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'content': self.content,
            'memory_type': self.memory_type,
            'importance': self.importance,
            'emotional_valence': self.emotional_valence,
            'context': self.context,
            'access_count': self.access_count
        }


class ShortTermMemory:
    """
    Short-term memory (working memory)
    Limited capacity, recent items, quickly accessible
    """

    def __init__(self, capacity: int = 7):
        """
        Initialize short-term memory
        Default capacity is 7 (based on Miller's law: 7±2 items)
        """
        self.capacity = capacity
        self.items: deque = deque(maxlen=capacity)

    def add(self, item: MemoryItem):
        """Add item to short-term memory"""
        self.items.append(item)

    def get_recent(self, n: int = None) -> List[MemoryItem]:
        """Get n most recent items (or all if n is None)"""
        if n is None:
            return list(self.items)
        return list(self.items)[-n:]

    def search(self, memory_type: str = None, keyword: str = None) -> List[MemoryItem]:
        """Search short-term memory"""
        results = list(self.items)

        if memory_type:
            results = [item for item in results if item.memory_type == memory_type]

        if keyword:
            results = [item for item in results if keyword.lower() in item.content.lower()]

        return results

    def clear(self):
        """Clear short-term memory"""
        self.items.clear()

    def __len__(self) -> int:
        return len(self.items)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'capacity': self.capacity,
            'current_size': len(self.items),
            'items': [item.to_dict() for item in self.items]
        }


class LongTermMemory:
    """
    Long-term memory
    Unlimited capacity, stores important experiences and patterns
    """

    def __init__(self, consolidation_threshold: float = 0.6):
        """
        Initialize long-term memory
        consolidation_threshold: Minimum importance for memory consolidation
        """
        self.consolidation_threshold = consolidation_threshold
        self.episodic_memory: List[MemoryItem] = []  # Specific experiences
        self.semantic_memory: Dict[str, Any] = {}  # General knowledge and patterns
        self.procedural_memory: Dict[str, float] = {}  # Learned skills/preferences

    def consolidate(self, item: MemoryItem):
        """
        Add item to long-term memory if it's important enough
        Returns True if consolidated, False otherwise
        """
        if item.importance >= self.consolidation_threshold:
            self.episodic_memory.append(item)
            return True
        return False

    def add_semantic_knowledge(self, key: str, value: Any):
        """Add general knowledge to semantic memory"""
        self.semantic_memory[key] = value

    def get_semantic_knowledge(self, key: str, default: Any = None) -> Any:
        """Retrieve semantic knowledge"""
        return self.semantic_memory.get(key, default)

    def update_procedural_memory(self, action: str, success: bool, learning_rate: float = 0.1):
        """
        Update learned preferences for actions
        Positive reinforcement for successful actions
        """
        if action not in self.procedural_memory:
            self.procedural_memory[action] = 0.5  # Start neutral

        # Update based on outcome
        adjustment = learning_rate if success else -learning_rate
        self.procedural_memory[action] += adjustment

        # Keep in bounds [0, 1]
        self.procedural_memory[action] = max(0.0, min(1.0, self.procedural_memory[action]))

    def get_action_preference(self, action: str) -> float:
        """Get learned preference for an action"""
        return self.procedural_memory.get(action, 0.5)

    def search_episodic(self, memory_type: str = None, keyword: str = None,
                       min_importance: float = 0.0,
                       limit: int = 10) -> List[MemoryItem]:
        """Search episodic memory"""
        current_time = datetime.now()

        # Filter by criteria
        results = self.episodic_memory

        if memory_type:
            results = [item for item in results if item.memory_type == memory_type]

        if keyword:
            results = [item for item in results if keyword.lower() in item.content.lower()]

        if min_importance > 0.0:
            results = [item for item in results if item.importance >= min_importance]

        # Sort by memory strength (recency + importance + access)
        results.sort(key=lambda x: x.get_strength(current_time), reverse=True)

        return results[:limit]

    def get_recent_outcomes(self, action_type: str = None, limit: int = 5) -> List[MemoryItem]:
        """Get recent action outcomes"""
        outcomes = [item for item in self.episodic_memory if item.memory_type == 'outcome']

        if action_type:
            outcomes = [item for item in outcomes if action_type in item.context.get('action', '')]

        return sorted(outcomes, key=lambda x: x.timestamp, reverse=True)[:limit]

    def decay_memories(self, current_time: datetime):
        """Remove weak memories (simulation of forgetting)"""
        threshold = 0.2  # Remove memories below this strength

        self.episodic_memory = [
            item for item in self.episodic_memory
            if item.get_strength(current_time) >= threshold
        ]

    def __len__(self) -> int:
        return len(self.episodic_memory)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'episodic_memory_size': len(self.episodic_memory),
            'semantic_memory_size': len(self.semantic_memory),
            'procedural_memory_size': len(self.procedural_memory),
            'recent_episodic': [item.to_dict() for item in self.episodic_memory[-5:]],
            'semantic_sample': dict(list(self.semantic_memory.items())[:5]),
            'procedural_sample': dict(list(self.procedural_memory.items())[:5])
        }


class MemorySystem:
    """
    Complete memory system combining short-term and long-term memory
    """

    def __init__(self, stm_capacity: int = 7, ltm_threshold: float = 0.6):
        self.short_term = ShortTermMemory(capacity=stm_capacity)
        self.long_term = LongTermMemory(consolidation_threshold=ltm_threshold)

    def add_memory(self, content: str, memory_type: str,
                   importance: float = 0.5,
                   emotional_valence: float = 0.0,
                   context: Dict[str, Any] = None):
        """Add a new memory to the system"""
        memory_item = MemoryItem(
            timestamp=datetime.now(),
            content=content,
            memory_type=memory_type,
            importance=importance,
            emotional_valence=emotional_valence,
            context=context or {}
        )

        # Add to short-term memory
        self.short_term.add(memory_item)

        # Consolidate to long-term if important enough
        self.long_term.consolidate(memory_item)

    def recall_similar_experiences(self, current_context: str,
                                   memory_type: str = None,
                                   limit: int = 3) -> List[MemoryItem]:
        """
        Recall similar past experiences from long-term memory
        """
        # Simple keyword-based similarity (could be enhanced with embeddings)
        keywords = current_context.lower().split()

        relevant_memories = []
        for keyword in keywords:
            memories = self.long_term.search_episodic(
                memory_type=memory_type,
                keyword=keyword,
                limit=limit
            )
            relevant_memories.extend(memories)

        # Remove duplicates and sort by strength
        unique_memories = list({id(m): m for m in relevant_memories}.values())
        current_time = datetime.now()
        unique_memories.sort(key=lambda x: x.get_strength(current_time), reverse=True)

        return unique_memories[:limit]

    def get_working_memory_context(self) -> str:
        """Get summary of current working memory"""
        recent = self.short_term.get_recent(5)
        if not recent:
            return "No recent memories"

        context = "Recent context:\n"
        for item in recent:
            context += f"- {item.content} ({item.memory_type})\n"

        return context

    def perform_memory_consolidation(self):
        """
        Periodic memory consolidation and cleanup
        Should be called periodically (e.g., after tasks or sessions)
        """
        current_time = datetime.now()
        self.long_term.decay_memories(current_time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entire memory system to dictionary"""
        return {
            'short_term_memory': self.short_term.to_dict(),
            'long_term_memory': self.long_term.to_dict()
        }
