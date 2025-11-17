# Synthetic User Decision Maker

A comprehensive tool for simulating human-like decision making in web interfaces. This tool creates synthetic users with realistic characteristics who make decisions based on their persona, emotional state, memory, and goals.

## Features

### 1. Human-like User Personas
- **OCEAN Personality Traits**: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism
- **Cognitive Attributes**: Cognitive ability, attention span, tech savviness, product familiarity
- **Behavioral Traits**: Impulsivity, risk tolerance, patience, exploration tendency
- **Demographic Profile**: Age group, education level, tech background
- **Energy & Fatigue**: Dynamic energy levels that affect decision making

### 2. Emotion Finite State Machine (FSM)
Based on psychological research, the emotion FSM tracks:
- **States**: Neutral, Confused, In Control, Frustrated
- **Dynamic Updates**: Emotions change based on context and experiences
- **Intensity Calculation**: Each emotion has a calculated intensity (0-1)
- **Influence on Decisions**: Current emotion affects element preferences

### 3. Memory Systems

#### Short-Term Memory (Working Memory)
- Limited capacity (7±2 items, based on Miller's Law)
- Stores recent interactions and observations
- Quickly accessible for immediate decisions

#### Long-Term Memory
- **Episodic Memory**: Specific experiences and events
- **Semantic Memory**: General knowledge and patterns
- **Procedural Memory**: Learned preferences and skills
- **Memory Consolidation**: Important memories transfer to long-term storage
- **Forgetting**: Weak memories naturally decay over time

### 4. Goal-Oriented Decision Making
- Define explicit user goals with priorities and urgency
- Decisions align with current goals
- Multiple goals can be managed

### 5. Element Ranking System
Ranks webpage elements based on:
- **Goal Alignment**: How well element matches current goal
- **Visual Prominence**: How noticeable the element is
- **Cognitive Load**: Complexity vs user's cognitive capacity
- **Familiarity**: Past experiences with similar elements
- **Emotion Preference**: Preferences based on current emotional state
- **Position**: Reading patterns and spatial positioning
- **Learned Preference**: Reinforcement learning from outcomes
- **Context Relevance**: Relevance to current task

## Installation

```python
# The tool is self-contained in this directory
# No external dependencies required (uses Python standard library)
```

## Quick Start

```python
from synthetic_user_decision_maker import (
    SyntheticUserDecisionMaker,
    UserPersona,
    WebElement,
    Goal
)

# 1. Create a user persona
persona = UserPersona.create_random_persona("user_001")

# Or create a custom persona
persona = UserPersona(
    persona_id="user_001",
    name="Tech-Savvy Sarah",
    personality=PersonalityTraits(
        openness=0.8,
        conscientiousness=0.7,
        neuroticism=0.3
    ),
    cognitive=CognitiveAttributes(
        cognitive_ability=0.8,
        tech_savviness=0.9,
        product_familiarity=0.6
    )
)

# 2. Create decision maker
decision_maker = SyntheticUserDecisionMaker(persona)

# 3. Set a goal
goal = Goal(
    goal_id="g1",
    description="Sign up for newsletter",
    priority=0.8,
    keywords=["sign", "signup", "newsletter", "subscribe"]
)
decision_maker.set_goal(goal)

# 4. Define webpage elements
elements = [
    WebElement(
        element_id="btn_signup",
        element_type="button",
        text="Sign Up for Newsletter",
        position=(800, 400),
        size=(200, 50),
        visual_prominence=0.9,
        context_relevance=0.95,
        semantic_meaning="subscribe to newsletter"
    ),
    WebElement(
        element_id="link_learn_more",
        element_type="link",
        text="Learn More",
        position=(600, 600),
        size=(180, 30),
        visual_prominence=0.5,
        context_relevance=0.3,
        semantic_meaning="navigate to information"
    )
]

# 5. Make decision
chosen_element, score_breakdown = decision_maker.make_decision(elements)

print(f"Chosen: {chosen_element.text}")
print(f"Score: {score_breakdown.total_score:.3f}")
print(f"Reasoning: {score_breakdown.reasoning}")

# 6. Record outcome (for learning)
decision_maker.record_outcome(chosen_element, success=True)
```

## Architecture

```
SyntheticUserDecisionMaker
├── UserPersona
│   ├── PersonalityTraits (OCEAN model)
│   ├── CognitiveAttributes
│   ├── DemographicProfile
│   ├── BehavioralTraits
│   └── Energy/Fatigue system
│
├── EmotionFSM
│   ├── EmotionProfile
│   ├── EmotionContext
│   ├── State calculation (Confused, In Control, Neutral, Frustrated)
│   └── Dynamic state transitions
│
├── MemorySystem
│   ├── ShortTermMemory (working memory)
│   └── LongTermMemory
│       ├── Episodic (experiences)
│       ├── Semantic (knowledge)
│       └── Procedural (learned skills)
│
└── Decision Logic
    ├── Element scoring (8 dimensions)
    ├── Emotion-based weight adjustment
    ├── Human-like randomness
    └── Ranking and selection
```

## Use Cases

### 1. User Experience Testing
Simulate different user types interacting with your interface:
- Novice users vs experts
- Stressed users vs relaxed users
- Different personality types

### 2. A/B Testing Simulation
Test interface designs with synthetic users before real testing:
- Element positioning optimization
- Button text and visual prominence
- Navigation flow testing

### 3. Accessibility Evaluation
Evaluate interface usability for users with:
- Low cognitive ability
- Low tech savviness
- High confusion states

### 4. User Flow Optimization
Identify potential friction points:
- Where do users get confused?
- Which elements are overlooked?
- How does fatigue affect decisions?

### 5. Personalization Research
Understand how different personas respond to:
- Different UI/UX patterns
- Various call-to-action styles
- Content presentation methods

## Examples

### Example 1: Basic Usage
```python
# See example_usage.py - example_basic_usage()
```

### Example 2: Confused User
```python
# See example_usage.py - example_confused_user()
```

### Example 3: Learning Over Time
```python
# See example_usage.py - example_multiple_interactions()
```

### Example 4: Persona Comparison
```python
# See example_usage.py - example_comparison_different_personas()
```

## API Reference

### UserPersona
Represents a synthetic user with human-like characteristics.

**Attributes:**
- `persona_id`: Unique identifier
- `personality`: PersonalityTraits (OCEAN model)
- `cognitive`: CognitiveAttributes
- `demographic`: DemographicProfile
- `behavioral`: BehavioralTraits
- `energy_level`: Current energy (0-1)

**Methods:**
- `apply_fatigue(task_complexity)`: Reduce energy based on task
- `rest(amount)`: Restore energy
- `get_current_state_modifiers()`: Get state-based modifiers

### EmotionFSM
Manages emotion states and transitions.

**Methods:**
- `update_state(context, patience)`: Update emotion based on context
- `get_current_state()`: Get current emotion state
- `get_all_intensities()`: Get all emotion intensities
- `is_negative_emotion()`: Check if negative state
- `is_positive_emotion()`: Check if positive state

### MemorySystem
Manages short-term and long-term memory.

**Methods:**
- `add_memory(content, memory_type, importance, emotional_valence, context)`
- `recall_similar_experiences(current_context, memory_type, limit)`
- `get_working_memory_context()`: Get recent memory summary
- `perform_memory_consolidation()`: Cleanup weak memories

### SyntheticUserDecisionMaker
Main decision maker integrating all components.

**Methods:**
- `set_goal(goal)`: Set current user goal
- `update_context(...)`: Update situational context
- `rank_elements(elements)`: Rank all elements with scores
- `make_decision(elements)`: Choose best element
- `record_outcome(element, success)`: Record action outcome
- `get_decision_summary()`: Get current state summary

### WebElement
Represents an actionable webpage element.

**Attributes:**
- `element_id`: Unique identifier
- `element_type`: Type (button, link, input, etc.)
- `text`: Visible text
- `position`: (x, y) coordinates
- `size`: (width, height)
- `visual_prominence`: How prominent (0-1)
- `context_relevance`: Relevance to task (0-1)
- `semantic_meaning`: What the element does

### Goal
Represents a user goal.

**Attributes:**
- `goal_id`: Unique identifier
- `description`: Goal description
- `priority`: Importance (0-1)
- `urgency`: Time pressure (0-1)
- `progress`: Completion progress (0-1)
- `keywords`: Related keywords for matching

## Advanced Usage

### Custom Emotion Weights
```python
from synthetic_user_decision_maker import EmotionModelWeights, ConfusedWeights

custom_weights = EmotionModelWeights(
    confused=ConfusedWeights(
        base_intensity=0.5,
        neuroticism_weight=0.6,
        familiarity_weight=0.3
    )
)

decision_maker = SyntheticUserDecisionMaker(persona, custom_weights)
```

### Context Updates
```python
# Increase interface complexity
decision_maker.update_context(
    interface_complexity=0.8,
    external_pressure=0.6,
    task_difficulty=0.7
)

# Record failures
decision_maker.update_context(recent_failure=True)
```

### Memory Queries
```python
# Get similar past experiences
similar = decision_maker.memory.recall_similar_experiences(
    current_context="checkout button",
    memory_type="action",
    limit=5
)

# Check learned preferences
preference = decision_maker.memory.long_term.get_action_preference(
    "button:submit_payment"
)
```

## Theoretical Foundation

### Emotion Model
Based on cognitive appraisal theory:
- Emotions arise from cognitive evaluation of situations
- Intrinsic factors (personality, abilities)
- Extrinsic factors (context, environment)

### Memory Model
Based on Atkinson-Shiffrin memory model:
- Short-term (working) memory with limited capacity
- Long-term memory with unlimited capacity
- Memory consolidation based on importance
- Forgetting through decay and interference

### Decision Making
Based on bounded rationality and heuristics:
- Limited cognitive resources
- Satisficing rather than optimizing
- Emotion-influenced preferences
- Learning from experience

## Contributing

This is a research tool. Contributions and improvements are welcome:
- Enhanced emotion models
- Additional personality frameworks
- Better memory consolidation algorithms
- More sophisticated element scoring

## License

MIT License - Free to use and modify

## Citation

If you use this tool in research, please cite:
```
Synthetic User Decision Maker v1.0
A tool for simulating human-like decision making in web interfaces
Based on OCEAN personality model, emotion FSM, and dual-process memory
```

## Contact

For questions, issues, or collaboration opportunities, please open an issue in the repository.
