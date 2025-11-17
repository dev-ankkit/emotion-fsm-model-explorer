# Quick Start Guide

## Installation

No installation required! The tool uses only Python standard library.

## 5-Minute Tutorial

### Step 1: Import the necessary components

```python
import sys
sys.path.insert(0, '/path/to/emotion-fsm-model-explorer')

from synthetic_user_decision_maker import (
    SyntheticUserDecisionMaker,
    UserPersona,
    WebElement,
    Goal
)
```

### Step 2: Create a user persona

```python
# Option 1: Random persona (for quick testing)
persona = UserPersona.create_random_persona("user_001")

# Option 2: Custom persona (for specific scenarios)
persona = UserPersona(
    persona_id="user_001",
    name="Sarah",
    cognitive=CognitiveAttributes(
        tech_savviness=0.8,
        product_familiarity=0.6
    )
)
```

### Step 3: Create the decision maker

```python
decision_maker = SyntheticUserDecisionMaker(persona)
```

### Step 4: Set a goal (optional but recommended)

```python
goal = Goal(
    goal_id="g1",
    description="Sign up for newsletter",
    priority=0.8,
    keywords=["signup", "newsletter", "subscribe"]
)
decision_maker.set_goal(goal)
```

### Step 5: Define webpage elements

```python
elements = [
    WebElement(
        element_id="btn_signup",
        element_type="button",
        text="Sign Up for Newsletter",
        position=(800, 400),  # (x, y)
        size=(200, 50),       # (width, height)
        visual_prominence=0.9,  # 0-1
        context_relevance=0.95, # 0-1
        semantic_meaning="subscribe to newsletter"
    ),
    WebElement(
        element_id="btn_close",
        element_type="button",
        text="Close",
        position=(1800, 100),
        size=(80, 40),
        visual_prominence=0.4,
        context_relevance=0.1,
        semantic_meaning="close dialog"
    )
]
```

### Step 6: Make a decision

```python
chosen_element, score = decision_maker.make_decision(elements)

print(f"Chosen: {chosen_element.text}")
print(f"Score: {score.total_score:.3f}")
print(f"Reasoning: {score.reasoning}")
```

### Step 7: Record the outcome (for learning)

```python
# If the action was successful
decision_maker.record_outcome(chosen_element, success=True)

# If the action failed
decision_maker.record_outcome(chosen_element, success=False)
```

## Common Scenarios

### Scenario 1: Testing Different Personas

```python
# Expert user
expert = UserPersona(
    persona_id="expert",
    cognitive=CognitiveAttributes(
        tech_savviness=0.9,
        product_familiarity=0.9
    )
)

# Novice user
novice = UserPersona(
    persona_id="novice",
    cognitive=CognitiveAttributes(
        tech_savviness=0.2,
        product_familiarity=0.1
    ),
    personality=PersonalityTraits(neuroticism=0.7)
)

# Compare their decisions
for persona in [expert, novice]:
    dm = SyntheticUserDecisionMaker(persona)
    dm.set_goal(goal)
    chosen, score = dm.make_decision(elements)
    print(f"{persona.name} chose: {chosen.text}")
```

### Scenario 2: Simulating a User Flow

```python
decision_maker = SyntheticUserDecisionMaker(persona)

# Step 1
goal1 = Goal(goal_id="g1", description="Add to cart", keywords=["cart", "add"])
decision_maker.set_goal(goal1)
chosen1, _ = decision_maker.make_decision(cart_page_elements)
decision_maker.record_outcome(chosen1, success=True)

# Step 2
goal2 = Goal(goal_id="g2", description="Checkout", keywords=["checkout", "pay"])
decision_maker.set_goal(goal2)
chosen2, _ = decision_maker.make_decision(checkout_elements)
decision_maker.record_outcome(chosen2, success=True)

# Check emotional state
summary = decision_maker.get_decision_summary()
print(f"User emotion: {summary['current_emotion']}")
print(f"Energy level: {summary['energy_level']}")
```

### Scenario 3: Handling Context Changes

```python
# User encounters a complex interface
decision_maker.update_context(
    interface_complexity=0.8,
    task_difficulty=0.7
)

# User experiences failures
decision_maker.update_context(recent_failure=True)

# This will affect their emotion and decisions
chosen, score = decision_maker.make_decision(elements)
```

## Tips

1. **Goal Keywords Matter**: Include relevant keywords in goals to help match elements
2. **Visual Prominence**: Higher values attract more attention, especially for confused users
3. **Context Relevance**: Set this high for elements that directly support the goal
4. **Semantic Meaning**: Clear descriptions help with memory and learning
5. **Energy Management**: Users get tired! Their decisions change as energy decreases

## Running Tests

```bash
python synthetic_user_decision_maker/test_basic.py
```

## Running Examples

```bash
# See test_basic.py for working examples
# Or check example_usage.py for comprehensive demonstrations
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore [example_usage.py](example_usage.py) for comprehensive examples
- Modify persona attributes to simulate different user types
- Experiment with emotion weights for different scenarios

## Troubleshooting

**Import Error**: Make sure to add the parent directory to your Python path:
```python
import sys
sys.path.insert(0, '/path/to/emotion-fsm-model-explorer')
```

**No element chosen**: Ensure elements have `is_visible=True` and `is_enabled=True`

**Low scores**: Check that elements have reasonable `visual_prominence` and `context_relevance` values

## Support

For issues or questions, check the README.md or examine the test files for working examples.
