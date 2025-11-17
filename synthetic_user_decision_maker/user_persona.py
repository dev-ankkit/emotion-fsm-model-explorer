"""
User Persona Module
Defines the synthetic user persona with human-like characteristics
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import random


@dataclass
class PersonalityTraits:
    """OCEAN personality model traits"""
    openness: float = 0.5  # Willingness to try new things (0-1)
    conscientiousness: float = 0.5  # Organization and goal-oriented behavior (0-1)
    extraversion: float = 0.5  # Social engagement level (0-1)
    agreeableness: float = 0.5  # Cooperation and empathy (0-1)
    neuroticism: float = 0.5  # Emotional stability (0-1)

    def to_dict(self) -> Dict[str, float]:
        return {
            'openness': self.openness,
            'conscientiousness': self.conscientiousness,
            'extraversion': self.extraversion,
            'agreeableness': self.agreeableness,
            'neuroticism': self.neuroticism
        }


@dataclass
class CognitiveAttributes:
    """Cognitive abilities and preferences"""
    cognitive_ability: float = 0.5  # General intelligence and problem-solving (0-1)
    attention_span: float = 0.5  # Ability to focus on tasks (0-1)
    tech_savviness: float = 0.5  # Technical proficiency (0-1)
    product_familiarity: float = 0.1  # Familiarity with the current product (0-1)
    reading_speed: float = 0.5  # How quickly they process text (0-1)
    visual_preference: float = 0.5  # Preference for visual vs text content (0-1)

    def to_dict(self) -> Dict[str, float]:
        return {
            'cognitive_ability': self.cognitive_ability,
            'attention_span': self.attention_span,
            'tech_savviness': self.tech_savviness,
            'product_familiarity': self.product_familiarity,
            'reading_speed': self.reading_speed,
            'visual_preference': self.visual_preference
        }


@dataclass
class DemographicProfile:
    """Demographic information"""
    age_group: str = "adult"  # child, teen, adult, senior
    education_level: str = "bachelor"  # high_school, bachelor, master, phd
    tech_background: str = "moderate"  # novice, moderate, expert
    primary_language: str = "english"

    def to_dict(self) -> Dict[str, str]:
        return {
            'age_group': self.age_group,
            'education_level': self.education_level,
            'tech_background': self.tech_background,
            'primary_language': self.primary_language
        }


@dataclass
class BehavioralTraits:
    """Behavioral patterns and tendencies"""
    impulsivity: float = 0.5  # Tendency to act without thinking (0-1)
    risk_tolerance: float = 0.5  # Willingness to take risks (0-1)
    patience: float = 0.5  # Tolerance for delays and complexity (0-1)
    exploration_tendency: float = 0.5  # Tendency to explore vs exploit (0-1)
    help_seeking_tendency: float = 0.5  # Likelihood to seek help (0-1)

    def to_dict(self) -> Dict[str, float]:
        return {
            'impulsivity': self.impulsivity,
            'risk_tolerance': self.risk_tolerance,
            'patience': self.patience,
            'exploration_tendency': self.exploration_tendency,
            'help_seeking_tendency': self.help_seeking_tendency
        }


@dataclass
class UserPersona:
    """
    Complete user persona with human-like characteristics
    This represents a synthetic user with realistic attributes
    """
    persona_id: str = "user_001"
    name: str = "Synthetic User"

    # Core attributes
    personality: PersonalityTraits = field(default_factory=PersonalityTraits)
    cognitive: CognitiveAttributes = field(default_factory=CognitiveAttributes)
    demographic: DemographicProfile = field(default_factory=DemographicProfile)
    behavioral: BehavioralTraits = field(default_factory=BehavioralTraits)

    # Energy and fatigue (affects decision making over time)
    energy_level: float = 0.8  # Current energy (0-1)
    fatigue_accumulation_rate: float = 0.01  # How quickly they get tired

    # Variability in behavior (makes it more human-like)
    decision_randomness: float = 0.1  # Random variation in decisions (0-1)

    def apply_fatigue(self, task_complexity: float = 0.5):
        """Reduce energy based on task complexity"""
        fatigue = task_complexity * self.fatigue_accumulation_rate
        self.energy_level = max(0.0, self.energy_level - fatigue)

    def rest(self, amount: float = 0.2):
        """Restore energy"""
        self.energy_level = min(1.0, self.energy_level + amount)

    def get_current_state_modifiers(self) -> Dict[str, float]:
        """
        Get modifiers based on current state (energy, fatigue)
        Low energy reduces cognitive abilities and patience
        """
        energy_factor = self.energy_level

        return {
            'cognitive_modifier': energy_factor,
            'patience_modifier': energy_factor,
            'attention_modifier': energy_factor,
            'impulsivity_modifier': 1.0 - energy_factor  # More impulsive when tired
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary"""
        return {
            'persona_id': self.persona_id,
            'name': self.name,
            'personality': self.personality.to_dict(),
            'cognitive': self.cognitive.to_dict(),
            'demographic': self.demographic.to_dict(),
            'behavioral': self.behavioral.to_dict(),
            'energy_level': self.energy_level,
            'fatigue_accumulation_rate': self.fatigue_accumulation_rate,
            'decision_randomness': self.decision_randomness
        }

    @classmethod
    def create_random_persona(cls, persona_id: str = None) -> 'UserPersona':
        """Create a random persona for testing"""
        if persona_id is None:
            persona_id = f"user_{random.randint(1000, 9999)}"

        return cls(
            persona_id=persona_id,
            name=f"Synthetic User {persona_id}",
            personality=PersonalityTraits(
                openness=random.uniform(0.2, 0.9),
                conscientiousness=random.uniform(0.2, 0.9),
                extraversion=random.uniform(0.2, 0.9),
                agreeableness=random.uniform(0.2, 0.9),
                neuroticism=random.uniform(0.2, 0.9)
            ),
            cognitive=CognitiveAttributes(
                cognitive_ability=random.uniform(0.3, 0.9),
                attention_span=random.uniform(0.3, 0.9),
                tech_savviness=random.uniform(0.2, 0.9),
                product_familiarity=random.uniform(0.1, 0.7),
                reading_speed=random.uniform(0.3, 0.9),
                visual_preference=random.uniform(0.3, 0.8)
            ),
            behavioral=BehavioralTraits(
                impulsivity=random.uniform(0.2, 0.8),
                risk_tolerance=random.uniform(0.2, 0.8),
                patience=random.uniform(0.2, 0.8),
                exploration_tendency=random.uniform(0.2, 0.8),
                help_seeking_tendency=random.uniform(0.2, 0.8)
            ),
            energy_level=random.uniform(0.6, 1.0),
            decision_randomness=random.uniform(0.05, 0.2)
        )
