"""
Basic tests for the Synthetic User Decision Maker
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from synthetic_user_decision_maker import (
    SyntheticUserDecisionMaker,
    UserPersona,
    WebElement,
    Goal,
    PersonalityTraits,
    CognitiveAttributes,
    EmotionState
)


def test_persona_creation():
    """Test creating a user persona"""
    print("Test 1: Persona Creation")

    persona = UserPersona(
        persona_id="test_001",
        name="Test User",
        personality=PersonalityTraits(openness=0.8),
        cognitive=CognitiveAttributes(tech_savviness=0.7)
    )

    assert persona.persona_id == "test_001"
    assert persona.personality.openness == 0.8
    assert persona.cognitive.tech_savviness == 0.7

    print("✓ Persona creation successful")
    print(f"  Created: {persona.name}")
    print(f"  Openness: {persona.personality.openness}")
    print(f"  Tech Savviness: {persona.cognitive.tech_savviness}")
    return True


def test_random_persona():
    """Test creating random persona"""
    print("\nTest 2: Random Persona Creation")

    persona = UserPersona.create_random_persona()

    assert persona.persona_id is not None
    assert 0 <= persona.personality.openness <= 1
    assert 0 <= persona.cognitive.cognitive_ability <= 1

    print("✓ Random persona creation successful")
    print(f"  ID: {persona.persona_id}")
    print(f"  Name: {persona.name}")
    return True


def test_decision_maker_initialization():
    """Test initializing the decision maker"""
    print("\nTest 3: Decision Maker Initialization")

    persona = UserPersona.create_random_persona("test_002")
    decision_maker = SyntheticUserDecisionMaker(persona)

    assert decision_maker.persona == persona
    assert decision_maker.emotion_fsm is not None
    assert decision_maker.memory is not None
    assert decision_maker.interaction_count == 0

    print("✓ Decision maker initialization successful")
    print(f"  Persona: {persona.name}")
    print(f"  Emotion FSM: Initialized")
    print(f"  Memory System: Initialized")
    return True


def test_goal_setting():
    """Test setting a goal"""
    print("\nTest 4: Goal Setting")

    persona = UserPersona.create_random_persona("test_003")
    decision_maker = SyntheticUserDecisionMaker(persona)

    goal = Goal(
        goal_id="g1",
        description="Test goal",
        priority=0.8,
        keywords=["test", "goal"]
    )

    decision_maker.set_goal(goal)

    assert decision_maker.current_goal == goal
    assert decision_maker.current_goal.description == "Test goal"

    print("✓ Goal setting successful")
    print(f"  Goal: {goal.description}")
    print(f"  Priority: {goal.priority}")
    return True


def test_element_ranking():
    """Test ranking elements"""
    print("\nTest 5: Element Ranking")

    persona = UserPersona(
        persona_id="test_004",
        name="Test User",
        cognitive=CognitiveAttributes(tech_savviness=0.8)
    )
    decision_maker = SyntheticUserDecisionMaker(persona)

    goal = Goal(
        goal_id="g1",
        description="Click submit button",
        priority=0.9,
        keywords=["submit", "send", "confirm"]
    )
    decision_maker.set_goal(goal)

    elements = [
        WebElement(
            element_id="btn_submit",
            element_type="button",
            text="Submit Form",
            position=(500, 400),
            size=(150, 50),
            visual_prominence=0.9,
            context_relevance=0.95,
            semantic_meaning="submit form data"
        ),
        WebElement(
            element_id="btn_cancel",
            element_type="button",
            text="Cancel",
            position=(700, 400),
            size=(150, 50),
            visual_prominence=0.6,
            context_relevance=0.3,
            semantic_meaning="cancel operation"
        ),
        WebElement(
            element_id="link_help",
            element_type="link",
            text="Help",
            position=(100, 100),
            size=(80, 30),
            visual_prominence=0.4,
            context_relevance=0.2,
            semantic_meaning="access help"
        )
    ]

    ranked = decision_maker.rank_elements(elements)

    assert len(ranked) == 3
    assert all(hasattr(score, 'total_score') for score in ranked)
    assert ranked[0].total_score >= ranked[1].total_score
    assert ranked[1].total_score >= ranked[2].total_score

    print("✓ Element ranking successful")
    print(f"  Total elements: {len(ranked)}")
    print(f"  Top choice: {ranked[0].element.text} (score: {ranked[0].total_score:.3f})")
    print(f"  2nd choice: {ranked[1].element.text} (score: {ranked[1].total_score:.3f})")
    print(f"  3rd choice: {ranked[2].element.text} (score: {ranked[2].total_score:.3f})")
    return True


def test_decision_making():
    """Test making a decision"""
    print("\nTest 6: Decision Making")

    persona = UserPersona.create_random_persona("test_005")
    decision_maker = SyntheticUserDecisionMaker(persona)

    goal = Goal(
        goal_id="g1",
        description="Sign up",
        priority=0.8,
        keywords=["signup", "register", "join"]
    )
    decision_maker.set_goal(goal)

    elements = [
        WebElement(
            element_id="btn_signup",
            element_type="button",
            text="Sign Up Now",
            position=(500, 400),
            size=(150, 50),
            visual_prominence=0.9,
            context_relevance=0.95,
            semantic_meaning="create new account"
        ),
        WebElement(
            element_id="link_login",
            element_type="link",
            text="Already have account? Login",
            position=(500, 500),
            size=(200, 30),
            visual_prominence=0.5,
            context_relevance=0.4,
            semantic_meaning="login to existing account"
        )
    ]

    chosen, score = decision_maker.make_decision(elements)

    assert chosen is not None
    assert chosen in [e.element for e in decision_maker.rank_elements(elements)]
    assert score.total_score >= 0
    assert decision_maker.interaction_count == 1

    print("✓ Decision making successful")
    print(f"  Chosen element: {chosen.text}")
    print(f"  Score: {score.total_score:.3f}")
    print(f"  Reasoning: {score.reasoning}")
    return True


def test_outcome_recording():
    """Test recording outcomes and learning"""
    print("\nTest 7: Outcome Recording & Learning")

    persona = UserPersona.create_random_persona("test_006")
    decision_maker = SyntheticUserDecisionMaker(persona)

    element = WebElement(
        element_id="btn_test",
        element_type="button",
        text="Test Button",
        position=(500, 400),
        size=(150, 50),
        semantic_meaning="test action"
    )

    # Record successful outcome
    decision_maker.record_outcome(element, success=True)

    # Check that memory was updated
    assert len(decision_maker.memory.short_term) > 0

    # Check procedural memory
    action_key = f"{element.element_type}:{element.semantic_meaning}"
    preference = decision_maker.memory.long_term.get_action_preference(action_key)

    assert preference > 0.5  # Should be positive after success

    print("✓ Outcome recording successful")
    print(f"  Outcome recorded: Success")
    print(f"  Learned preference: {preference:.3f}")
    print(f"  Short-term memory items: {len(decision_maker.memory.short_term)}")
    return True


def test_emotion_state_updates():
    """Test emotion state updates"""
    print("\nTest 8: Emotion State Updates")

    persona = UserPersona(
        persona_id="test_007",
        personality=PersonalityTraits(neuroticism=0.7),
        cognitive=CognitiveAttributes(product_familiarity=0.2)
    )
    decision_maker = SyntheticUserDecisionMaker(persona)

    # Update context to be stressful
    decision_maker.update_context(
        interface_complexity=0.8,
        external_pressure=0.7,
        task_difficulty=0.8
    )

    # Force emotion update by ranking elements
    elements = [
        WebElement("test", "button", "Test", (100, 100), (50, 50))
    ]
    decision_maker.rank_elements(elements)

    current_emotion = decision_maker.emotion_fsm.get_current_state()

    assert current_emotion in EmotionState
    assert decision_maker.emotion_fsm.intensities is not None

    print("✓ Emotion state update successful")
    print(f"  Current emotion: {current_emotion.value}")

    intensities = decision_maker.emotion_fsm.get_all_intensities()
    for emotion, intensity in intensities.items():
        print(f"  {emotion}: {intensity:.3f}")

    return True


def test_memory_system():
    """Test memory system"""
    print("\nTest 9: Memory System")

    persona = UserPersona.create_random_persona("test_008")
    decision_maker = SyntheticUserDecisionMaker(persona)

    # Add memories
    decision_maker.memory.add_memory(
        content="Clicked submit button",
        memory_type="action",
        importance=0.7,
        emotional_valence=0.5
    )

    decision_maker.memory.add_memory(
        content="Form submission succeeded",
        memory_type="outcome",
        importance=0.8,
        emotional_valence=0.8
    )

    # Check short-term memory
    assert len(decision_maker.memory.short_term) == 2

    # Check long-term consolidation (importance >= threshold)
    assert len(decision_maker.memory.long_term) >= 1

    # Test recall
    similar = decision_maker.memory.recall_similar_experiences(
        current_context="submit button",
        limit=2
    )

    print("✓ Memory system working correctly")
    print(f"  Short-term memory: {len(decision_maker.memory.short_term)} items")
    print(f"  Long-term memory: {len(decision_maker.memory.long_term)} items")
    print(f"  Recalled memories: {len(similar)}")
    return True


def test_fatigue_system():
    """Test energy and fatigue system"""
    print("\nTest 10: Energy & Fatigue System")

    persona = UserPersona.create_random_persona("test_009")
    initial_energy = persona.energy_level

    # Apply fatigue
    persona.apply_fatigue(task_complexity=0.8)

    assert persona.energy_level < initial_energy

    # Rest
    persona.rest(amount=0.3)

    assert persona.energy_level > initial_energy - 0.8

    print("✓ Fatigue system working correctly")
    print(f"  Initial energy: {initial_energy:.3f}")
    print(f"  After fatigue: {persona.energy_level:.3f}")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("SYNTHETIC USER DECISION MAKER - TEST SUITE")
    print("=" * 60)

    tests = [
        test_persona_creation,
        test_random_persona,
        test_decision_maker_initialization,
        test_goal_setting,
        test_element_ranking,
        test_decision_making,
        test_outcome_recording,
        test_emotion_state_updates,
        test_memory_system,
        test_fatigue_system
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(("PASS", test.__name__))
        except Exception as e:
            results.append(("FAIL", test.__name__, str(e)))
            print(f"✗ Test failed: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r[0] == "PASS")
    total = len(results)

    for result in results:
        if result[0] == "PASS":
            print(f"✓ {result[1]}")
        else:
            print(f"✗ {result[1]}: {result[2]}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        return True
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
