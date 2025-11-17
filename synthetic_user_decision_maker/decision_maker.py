"""
Decision Maker Module
Main module that integrates persona, emotion FSM, and memory to make decisions
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
import random
import math

from .user_persona import UserPersona
from .emotion_fsm import (
    EmotionFSM, EmotionProfile, EmotionContext,
    EmotionState, EmotionModelWeights
)
from .memory_system import MemorySystem


@dataclass
class WebElement:
    """Represents an actionable element on a webpage"""
    element_id: str
    element_type: str  # button, link, input, dropdown, etc.
    text: str  # Visible text or label
    position: Tuple[int, int]  # (x, y) position on page
    size: Tuple[int, int]  # (width, height)
    is_visible: bool = True
    is_enabled: bool = True
    semantic_meaning: str = ""  # What this element does
    visual_prominence: float = 0.5  # How visually prominent (0-1)
    context_relevance: float = 0.5  # Relevance to current task (0-1)
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class Goal:
    """User's current goal"""
    goal_id: str
    description: str
    priority: float = 0.5  # How important is this goal (0-1)
    urgency: float = 0.5  # How urgent is this goal (0-1)
    progress: float = 0.0  # How much progress made (0-1)
    keywords: List[str] = None  # Keywords related to the goal

    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []


@dataclass
class ElementScore:
    """Score breakdown for an element"""
    element: WebElement
    total_score: float
    component_scores: Dict[str, float]  # Breakdown of score components
    reasoning: str  # Human-readable explanation


class SyntheticUserDecisionMaker:
    """
    Main decision maker that simulates human-like decision making
    Integrates persona, emotion state, memory, and goals
    """

    def __init__(self, persona: UserPersona,
                 emotion_weights: EmotionModelWeights = None):
        self.persona = persona

        # Initialize emotion FSM from persona
        emotion_profile = EmotionProfile(
            product_familiarity=persona.cognitive.product_familiarity,
            cognitive_ability=persona.cognitive.cognitive_ability,
            ocean_neuroticism=persona.personality.neuroticism,
            ocean_openness=persona.personality.openness,
            ocean_conscientiousness=persona.personality.conscientiousness
        )

        self.emotion_fsm = EmotionFSM(emotion_profile, emotion_weights)
        self.memory = MemorySystem()

        # Current state
        self.current_goal: Optional[Goal] = None
        self.current_context = EmotionContext()
        self.interaction_count = 0
        self.recent_actions: List[str] = []

    def set_goal(self, goal: Goal):
        """Set the current goal"""
        self.current_goal = goal
        self.memory.add_memory(
            content=f"New goal: {goal.description}",
            memory_type="observation",
            importance=0.7,
            context={"goal_id": goal.goal_id}
        )

    def update_context(self, interface_complexity: float = None,
                      external_pressure: float = None,
                      task_difficulty: float = None,
                      recent_failure: bool = False,
                      recent_success: bool = False):
        """Update the current situational context"""
        if interface_complexity is not None:
            self.current_context.interface_complexity = interface_complexity
        if external_pressure is not None:
            self.current_context.external_situation_pressure = external_pressure
        if task_difficulty is not None:
            self.current_context.task_difficulty = task_difficulty

        if recent_failure:
            self.current_context.recent_failures += 1
        if recent_success:
            self.current_context.recent_successes += 1

    def rank_elements(self, elements: List[WebElement],
                     verbose: bool = False) -> List[ElementScore]:
        """
        Rank all elements based on persona, emotion, memory, and goals
        Returns list of ElementScore objects sorted by score (highest first)
        """
        # Update emotion state
        emotion_state, emotion_intensities = self.emotion_fsm.update_state(
            self.current_context,
            patience=self.persona.behavioral.patience
        )

        # Get current modifiers based on energy/fatigue
        state_modifiers = self.persona.get_current_state_modifiers()

        scored_elements = []

        for element in elements:
            if not element.is_visible or not element.is_enabled:
                continue  # Skip non-actionable elements

            # Calculate score components
            scores = self._calculate_element_scores(
                element, emotion_state, state_modifiers
            )

            # Combine scores with weights
            total_score = self._combine_scores(scores, emotion_state)

            # Add human-like randomness
            randomness = self.persona.decision_randomness
            noise = random.gauss(0, randomness)
            total_score = max(0.0, total_score + noise)

            # Create reasoning
            reasoning = self._generate_reasoning(element, scores, emotion_state)

            scored_elements.append(ElementScore(
                element=element,
                total_score=total_score,
                component_scores=scores,
                reasoning=reasoning
            ))

        # Sort by score (highest first)
        scored_elements.sort(key=lambda x: x.total_score, reverse=True)

        return scored_elements

    def _calculate_element_scores(self, element: WebElement,
                                  emotion_state: EmotionState,
                                  state_modifiers: Dict[str, float]) -> Dict[str, float]:
        """Calculate individual score components for an element"""
        scores = {}

        # 1. Goal alignment score
        scores['goal_alignment'] = self._score_goal_alignment(element)

        # 2. Visual prominence score
        scores['visual_prominence'] = self._score_visual_prominence(element)

        # 3. Cognitive load score (affected by cognitive ability and energy)
        scores['cognitive_load'] = self._score_cognitive_load(element, state_modifiers)

        # 4. Familiarity score (from memory)
        scores['familiarity'] = self._score_familiarity(element)

        # 5. Emotion-based preference
        scores['emotion_preference'] = self._score_emotion_preference(element, emotion_state)

        # 6. Spatial/position score
        scores['position'] = self._score_position(element)

        # 7. Learned preference (from procedural memory)
        scores['learned_preference'] = self._score_learned_preference(element)

        # 8. Context relevance
        scores['context_relevance'] = element.context_relevance

        return scores

    def _score_goal_alignment(self, element: WebElement) -> float:
        """Score how well element aligns with current goal"""
        if not self.current_goal:
            return 0.5  # Neutral if no goal

        score = 0.0

        # Check if element text matches goal keywords
        element_text_lower = element.text.lower()
        semantic_lower = element.semantic_meaning.lower()

        for keyword in self.current_goal.keywords:
            if keyword.lower() in element_text_lower or keyword.lower() in semantic_lower:
                score += 0.3

        # Adjust by goal priority
        score *= self.current_goal.priority

        return min(1.0, score)

    def _score_visual_prominence(self, element: WebElement) -> float:
        """Score based on visual prominence"""
        # High visual prominence helps users with low attention or high confusion
        prominence_score = element.visual_prominence

        # Modulate by attention span
        if self.persona.cognitive.attention_span < 0.5:
            prominence_score *= 1.5  # Prefer prominent elements when attention is low

        return min(1.0, prominence_score)

    def _score_cognitive_load(self, element: WebElement, state_modifiers: Dict[str, float]) -> float:
        """Score based on cognitive load (simpler elements preferred when tired/confused)"""
        # Estimate cognitive load of the element
        element_complexity = 0.3  # Base complexity

        if element.element_type in ['dropdown', 'multi-select', 'form']:
            element_complexity += 0.3
        elif element.element_type in ['button', 'link']:
            element_complexity += 0.1

        # Text length increases complexity
        text_length_factor = min(0.4, len(element.text) / 100)
        element_complexity += text_length_factor

        # User's cognitive ability and current state
        cognitive_capacity = (
            self.persona.cognitive.cognitive_ability *
            state_modifiers['cognitive_modifier']
        )

        # Score is better when complexity matches capacity
        if element_complexity <= cognitive_capacity:
            return 1.0 - (element_complexity * 0.5)  # Prefer simpler when possible
        else:
            # Penalty for too complex
            return max(0.0, 1.0 - (element_complexity - cognitive_capacity))

    def _score_familiarity(self, element: WebElement) -> float:
        """Score based on past interactions (memory)"""
        # Check if we've interacted with similar elements
        similar_memories = self.memory.recall_similar_experiences(
            current_context=f"{element.element_type} {element.text}",
            memory_type="action",
            limit=3
        )

        if not similar_memories:
            # No memory - score based on product familiarity
            return self.persona.cognitive.product_familiarity

        # Calculate average emotional valence of memories
        avg_valence = sum(m.emotional_valence for m in similar_memories) / len(similar_memories)

        # Positive memories increase score
        familiarity_score = 0.5 + (avg_valence * 0.5)

        return max(0.0, min(1.0, familiarity_score))

    def _score_emotion_preference(self, element: WebElement, emotion_state: EmotionState) -> float:
        """Score based on current emotion state"""
        score = 0.5  # Neutral base

        if emotion_state == EmotionState.CONFUSED:
            # Prefer clear, simple, prominent elements
            if element.element_type in ['button', 'link']:
                score += 0.2
            if element.visual_prominence > 0.7:
                score += 0.2
            if 'help' in element.text.lower() or 'guide' in element.text.lower():
                score += 0.3

        elif emotion_state == EmotionState.FRUSTRATED:
            # Want quick solutions, shortcuts
            if 'skip' in element.text.lower() or 'close' in element.text.lower():
                score += 0.3
            if element.element_type == 'button':
                score += 0.2
            # Avoid complex interactions
            if element.element_type in ['form', 'multi-select']:
                score -= 0.3

        elif emotion_state == EmotionState.IN_CONTROL:
            # More willing to explore and engage with complex elements
            score += 0.1
            if element.element_type in ['dropdown', 'form']:
                score += 0.1

        return max(0.0, min(1.0, score))

    def _score_position(self, element: WebElement) -> float:
        """Score based on element position (reading patterns)"""
        x, y = element.position

        # Western reading pattern: top-left to bottom-right
        # Normalize position (assuming 1920x1080 screen)
        norm_x = x / 1920
        norm_y = y / 1080

        # Prefer top-left quadrant, with decay toward bottom-right
        position_score = 1.0 - (norm_x * 0.3 + norm_y * 0.4)

        # Center elements also get boost (eye naturally drawn to center)
        center_x, center_y = 0.5, 0.5
        distance_from_center = math.sqrt((norm_x - center_x)**2 + (norm_y - center_y)**2)
        center_boost = max(0, 0.2 - distance_from_center * 0.2)

        return max(0.0, min(1.0, position_score + center_boost))

    def _score_learned_preference(self, element: WebElement) -> float:
        """Score based on learned preferences from procedural memory"""
        action_key = f"{element.element_type}:{element.semantic_meaning}"
        return self.memory.long_term.get_action_preference(action_key)

    def _combine_scores(self, scores: Dict[str, float], emotion_state: EmotionState) -> float:
        """Combine component scores with emotion-dependent weights"""
        # Base weights
        weights = {
            'goal_alignment': 0.25,
            'visual_prominence': 0.10,
            'cognitive_load': 0.15,
            'familiarity': 0.10,
            'emotion_preference': 0.15,
            'position': 0.10,
            'learned_preference': 0.10,
            'context_relevance': 0.05
        }

        # Adjust weights based on emotion state
        if emotion_state == EmotionState.CONFUSED:
            weights['visual_prominence'] = 0.20
            weights['cognitive_load'] = 0.20
            weights['goal_alignment'] = 0.15

        elif emotion_state == EmotionState.FRUSTRATED:
            weights['emotion_preference'] = 0.25
            weights['learned_preference'] = 0.15
            weights['goal_alignment'] = 0.20

        elif emotion_state == EmotionState.IN_CONTROL:
            weights['goal_alignment'] = 0.30
            weights['context_relevance'] = 0.15

        # Calculate weighted sum
        total = sum(scores[key] * weights[key] for key in scores.keys())

        return total

    def _generate_reasoning(self, element: WebElement,
                           scores: Dict[str, float],
                           emotion_state: EmotionState) -> str:
        """Generate human-readable reasoning for the decision"""
        reasoning_parts = []

        # Top contributing factors
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_factors = sorted_scores[:3]

        reasoning_parts.append(f"Emotion: {emotion_state.value}")

        for factor, score in top_factors:
            if score > 0.6:
                reasoning_parts.append(f"High {factor} ({score:.2f})")

        if self.current_goal:
            reasoning_parts.append(f"Goal: {self.current_goal.description[:30]}...")

        return " | ".join(reasoning_parts)

    def make_decision(self, elements: List[WebElement],
                     verbose: bool = False) -> Tuple[WebElement, ElementScore]:
        """
        Make a decision: choose the best element to interact with
        Returns: (chosen_element, score_breakdown)
        """
        # Rank all elements
        ranked_elements = self.rank_elements(elements, verbose)

        if not ranked_elements:
            raise ValueError("No actionable elements provided")

        # Choose top element
        best_choice = ranked_elements[0]

        # Apply fatigue
        self.persona.apply_fatigue(task_complexity=0.3)

        # Record decision in memory
        self.memory.add_memory(
            content=f"Chose {best_choice.element.element_type}: {best_choice.element.text}",
            memory_type="action",
            importance=0.5,
            emotional_valence=0.1,
            context={
                'element_id': best_choice.element.element_id,
                'emotion_state': self.emotion_fsm.current_state.value,
                'score': best_choice.total_score
            }
        )

        self.interaction_count += 1
        self.recent_actions.append(best_choice.element.element_id)

        return best_choice.element, best_choice

    def record_outcome(self, element: WebElement, success: bool,
                      emotional_valence: float = None):
        """
        Record the outcome of an action
        This updates learning and memory
        """
        if emotional_valence is None:
            emotional_valence = 0.5 if success else -0.5

        # Update context
        self.update_context(recent_success=success, recent_failure=not success)

        # Update procedural memory (learning)
        action_key = f"{element.element_type}:{element.semantic_meaning}"
        self.memory.long_term.update_procedural_memory(action_key, success)

        # Record in episodic memory
        self.memory.add_memory(
            content=f"{'Success' if success else 'Failure'}: {element.text}",
            memory_type="outcome",
            importance=0.7,
            emotional_valence=emotional_valence,
            context={
                'element_id': element.element_id,
                'success': success,
                'emotion_state': self.emotion_fsm.current_state.value
            }
        )

    def get_decision_summary(self) -> Dict[str, Any]:
        """Get summary of decision maker's current state"""
        return {
            'persona_id': self.persona.persona_id,
            'current_emotion': self.emotion_fsm.current_state.value,
            'emotion_intensities': self.emotion_fsm.get_all_intensities(),
            'energy_level': self.persona.energy_level,
            'interaction_count': self.interaction_count,
            'current_goal': self.current_goal.description if self.current_goal else None,
            'memory_stats': self.memory.to_dict()
        }
