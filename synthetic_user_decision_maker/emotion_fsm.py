"""
Emotion FSM Module
Implements emotion state machine for synthetic users
Based on the emotion model from the main application
"""

from dataclasses import dataclass, field
from typing import Dict, Tuple
from enum import Enum


class EmotionState(Enum):
    """Possible emotion states for the user"""
    NEUTRAL = "neutral"
    CONFUSED = "confused"
    IN_CONTROL = "in_control"
    FRUSTRATED = "frustrated"
    CONFIDENT = "confident"
    OVERWHELMED = "overwhelmed"


@dataclass
class EmotionProfile:
    """User's emotion-related profile attributes"""
    product_familiarity: float = 0.1  # Familiarity with the product (0-1)
    cognitive_ability: float = 0.5  # Cognitive processing ability (0-1)
    ocean_neuroticism: float = 0.5  # Emotional stability (0-1)
    ocean_openness: float = 0.5  # Openness to experience (0-1)
    ocean_conscientiousness: float = 0.5  # Organization and discipline (0-1)


@dataclass
class EmotionContext:
    """Current situational context affecting emotions"""
    interface_complexity: float = 0.3  # How complex the current interface is (0-1)
    external_situation_pressure: float = 0.1  # External time/stress pressure (0-1)
    task_difficulty: float = 0.5  # Current task difficulty (0-1)
    recent_failures: int = 0  # Number of recent failed attempts
    recent_successes: int = 0  # Number of recent successes


@dataclass
class ConfusedWeights:
    """Weights for calculating confused state intensity"""
    base_intensity: float = 0.4
    neuroticism_weight: float = 0.5
    familiarity_weight: float = 0.2
    cognitive_ability_weight: float = 0.1
    openness_weight: float = 0.15
    interface_complexity_weight: float = 0.2
    task_difficulty_weight: float = 0.15


@dataclass
class InControlWeights:
    """Weights for calculating in-control state intensity"""
    base_intensity: float = 0.5
    conscientiousness_weight: float = 0.2
    familiarity_weight: float = 0.3
    openness_weight: float = 0.25
    external_pressure_weight: float = 0.1
    success_weight: float = 0.2


@dataclass
class NeutralWeights:
    """Weights for calculating neutral state intensity"""
    base_intensity: float = 0.1
    neuroticism_weight: float = 0.1
    openness_weight: float = 0.1


@dataclass
class FrustratedWeights:
    """Weights for calculating frustrated state intensity"""
    base_intensity: float = 0.2
    neuroticism_weight: float = 0.4
    failure_weight: float = 0.3
    patience_weight: float = 0.2
    pressure_weight: float = 0.15


@dataclass
class EmotionModelWeights:
    """All weights for the emotion model"""
    confused: ConfusedWeights = field(default_factory=ConfusedWeights)
    in_control: InControlWeights = field(default_factory=InControlWeights)
    neutral: NeutralWeights = field(default_factory=NeutralWeights)
    frustrated: FrustratedWeights = field(default_factory=FrustratedWeights)


class EmotionFSM:
    """
    Finite State Machine for user emotions
    Calculates emotion intensities and determines dominant emotion state
    """

    def __init__(self, profile: EmotionProfile, weights: EmotionModelWeights = None):
        self.profile = profile
        self.weights = weights or EmotionModelWeights()
        self.current_state = EmotionState.NEUTRAL
        self.state_history = [EmotionState.NEUTRAL]
        self.intensities = {}

    def calculate_confused_intensity(self, context: EmotionContext) -> float:
        """Calculate intensity for confused state"""
        intensity = self.weights.confused.base_intensity

        # Intrinsic factors
        intensity += self.profile.ocean_neuroticism * self.weights.confused.neuroticism_weight
        intensity += (1.0 - self.profile.product_familiarity) * self.weights.confused.familiarity_weight
        intensity -= self.profile.cognitive_ability * self.weights.confused.cognitive_ability_weight
        intensity -= self.profile.ocean_openness * self.weights.confused.openness_weight

        # Extrinsic factors
        intensity += context.interface_complexity * self.weights.confused.interface_complexity_weight
        intensity += context.task_difficulty * self.weights.confused.task_difficulty_weight

        return max(0.0, min(1.0, intensity))

    def calculate_incontrol_intensity(self, context: EmotionContext) -> float:
        """Calculate intensity for in-control state"""
        intensity = self.weights.in_control.base_intensity

        # Intrinsic factors
        intensity += self.profile.ocean_conscientiousness * self.weights.in_control.conscientiousness_weight
        intensity += self.profile.product_familiarity * self.weights.in_control.familiarity_weight
        intensity += self.profile.ocean_openness * self.weights.in_control.openness_weight

        # Extrinsic factors
        intensity += context.external_situation_pressure * self.weights.in_control.external_pressure_weight

        # Success reinforcement
        if context.recent_successes > 0:
            intensity += min(0.3, context.recent_successes * 0.1) * self.weights.in_control.success_weight

        return max(0.0, min(1.0, intensity))

    def calculate_neutral_intensity(self, context: EmotionContext) -> float:
        """Calculate intensity for neutral state"""
        intensity = self.weights.neutral.base_intensity

        # Intrinsic factors
        intensity += self.profile.ocean_neuroticism * self.weights.neutral.neuroticism_weight
        intensity += self.profile.ocean_openness * self.weights.neutral.openness_weight

        return max(0.0, min(1.0, intensity))

    def calculate_frustrated_intensity(self, context: EmotionContext, patience: float = 0.5) -> float:
        """Calculate intensity for frustrated state"""
        intensity = self.weights.frustrated.base_intensity

        # Intrinsic factors
        intensity += self.profile.ocean_neuroticism * self.weights.frustrated.neuroticism_weight
        intensity += (1.0 - patience) * self.weights.frustrated.patience_weight

        # Extrinsic factors - failures increase frustration
        if context.recent_failures > 0:
            intensity += min(0.4, context.recent_failures * 0.15) * self.weights.frustrated.failure_weight

        intensity += context.external_situation_pressure * self.weights.frustrated.pressure_weight

        return max(0.0, min(1.0, intensity))

    def update_state(self, context: EmotionContext, patience: float = 0.5) -> Tuple[EmotionState, Dict[str, float]]:
        """
        Update emotion state based on current context
        Returns: (dominant_state, all_intensities)
        """
        # Calculate all intensities
        intensities = {
            EmotionState.CONFUSED: self.calculate_confused_intensity(context),
            EmotionState.IN_CONTROL: self.calculate_incontrol_intensity(context),
            EmotionState.NEUTRAL: self.calculate_neutral_intensity(context),
            EmotionState.FRUSTRATED: self.calculate_frustrated_intensity(context, patience)
        }

        self.intensities = intensities

        # Determine dominant state
        dominant_state = max(intensities.items(), key=lambda x: x[1])[0]

        # Update state
        self.current_state = dominant_state
        self.state_history.append(dominant_state)

        return dominant_state, intensities

    def get_current_state(self) -> EmotionState:
        """Get current emotion state"""
        return self.current_state

    def get_state_intensity(self, state: EmotionState) -> float:
        """Get intensity of a specific state"""
        return self.intensities.get(state, 0.0)

    def get_all_intensities(self) -> Dict[str, float]:
        """Get all current emotion intensities"""
        return {state.value: intensity for state, intensity in self.intensities.items()}

    def is_negative_emotion(self) -> bool:
        """Check if current state is a negative emotion"""
        negative_states = {EmotionState.CONFUSED, EmotionState.FRUSTRATED, EmotionState.OVERWHELMED}
        return self.current_state in negative_states

    def is_positive_emotion(self) -> bool:
        """Check if current state is a positive emotion"""
        positive_states = {EmotionState.IN_CONTROL, EmotionState.CONFIDENT}
        return self.current_state in positive_states

    def reset(self):
        """Reset to neutral state"""
        self.current_state = EmotionState.NEUTRAL
        self.state_history = [EmotionState.NEUTRAL]
        self.intensities = {}
