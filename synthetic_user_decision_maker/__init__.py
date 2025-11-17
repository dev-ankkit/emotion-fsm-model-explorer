"""
Synthetic User Decision Maker
A tool for simulating human-like decision making in web interfaces

This package provides:
- User personas with human-like characteristics
- Emotion state machine (FSM) integration
- Short-term and long-term memory systems
- Goal-oriented decision making
- Element ranking and selection logic
"""

from .user_persona import (
    UserPersona,
    PersonalityTraits,
    CognitiveAttributes,
    DemographicProfile,
    BehavioralTraits
)

from .emotion_fsm import (
    EmotionFSM,
    EmotionProfile,
    EmotionContext,
    EmotionState,
    EmotionModelWeights
)

from .memory_system import (
    MemorySystem,
    MemoryItem,
    ShortTermMemory,
    LongTermMemory
)

from .decision_maker import (
    SyntheticUserDecisionMaker,
    WebElement,
    Goal,
    ElementScore
)

__version__ = "1.0.0"
__author__ = "Synthetic User Decision Maker Team"

__all__ = [
    # User Persona
    'UserPersona',
    'PersonalityTraits',
    'CognitiveAttributes',
    'DemographicProfile',
    'BehavioralTraits',

    # Emotion FSM
    'EmotionFSM',
    'EmotionProfile',
    'EmotionContext',
    'EmotionState',
    'EmotionModelWeights',

    # Memory System
    'MemorySystem',
    'MemoryItem',
    'ShortTermMemory',
    'LongTermMemory',

    # Decision Maker
    'SyntheticUserDecisionMaker',
    'WebElement',
    'Goal',
    'ElementScore'
]
