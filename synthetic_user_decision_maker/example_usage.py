"""
Example Usage of Synthetic User Decision Maker
Demonstrates how to use the tool to simulate user decisions
"""

from synthetic_user_decision_maker import (
    SyntheticUserDecisionMaker,
    UserPersona,
    WebElement,
    Goal,
    PersonalityTraits,
    CognitiveAttributes
)


def example_basic_usage():
    """Basic example: Create a user and make a simple decision"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60)

    # Create a user persona
    persona = UserPersona(
        persona_id="user_001",
        name="Tech-Savvy Sarah",
        personality=PersonalityTraits(
            openness=0.8,
            conscientiousness=0.7,
            extraversion=0.6,
            agreeableness=0.7,
            neuroticism=0.3
        ),
        cognitive=CognitiveAttributes(
            cognitive_ability=0.8,
            tech_savviness=0.9,
            product_familiarity=0.6
        )
    )

    # Create decision maker
    decision_maker = SyntheticUserDecisionMaker(persona)

    # Set a goal
    goal = Goal(
        goal_id="g1",
        description="Sign up for the newsletter",
        priority=0.8,
        keywords=["sign", "signup", "newsletter", "subscribe"]
    )
    decision_maker.set_goal(goal)

    # Define webpage elements
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
            text="Learn More About Our Products",
            position=(600, 600),
            size=(180, 30),
            visual_prominence=0.5,
            context_relevance=0.3,
            semantic_meaning="navigate to product information"
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
        ),
        WebElement(
            element_id="input_email",
            element_type="input",
            text="Enter your email",
            position=(700, 300),
            size=(300, 40),
            visual_prominence=0.7,
            context_relevance=0.8,
            semantic_meaning="email input field"
        )
    ]

    # Make decision
    chosen_element, score_breakdown = decision_maker.make_decision(elements)

    # Display results
    print(f"\nUser: {persona.name}")
    print(f"Goal: {goal.description}")
    print(f"\nChosen Element: {chosen_element.text}")
    print(f"Element Type: {chosen_element.element_type}")
    print(f"Total Score: {score_breakdown.total_score:.3f}")
    print(f"Reasoning: {score_breakdown.reasoning}")
    print(f"\nScore Breakdown:")
    for component, score in score_breakdown.component_scores.items():
        print(f"  {component}: {score:.3f}")

    # Record outcome (successful interaction)
    decision_maker.record_outcome(chosen_element, success=True)

    print("\n" + "=" * 60 + "\n")


def example_confused_user():
    """Example with a confused, novice user"""
    print("=" * 60)
    print("EXAMPLE 2: Confused Novice User")
    print("=" * 60)

    # Create a novice persona
    persona = UserPersona(
        persona_id="user_002",
        name="Confused Carl",
        personality=PersonalityTraits(
            openness=0.3,
            conscientiousness=0.5,
            neuroticism=0.7  # High neuroticism
        ),
        cognitive=CognitiveAttributes(
            cognitive_ability=0.5,
            tech_savviness=0.2,  # Low tech savviness
            product_familiarity=0.1  # Very unfamiliar
        )
    )

    decision_maker = SyntheticUserDecisionMaker(persona)

    # Set goal
    goal = Goal(
        goal_id="g2",
        description="Find help documentation",
        priority=0.9,
        urgency=0.8,
        keywords=["help", "support", "guide", "tutorial"]
    )
    decision_maker.set_goal(goal)

    # Update context - complex interface
    decision_maker.update_context(
        interface_complexity=0.8,
        external_pressure=0.6,
        task_difficulty=0.7
    )

    # Define elements
    elements = [
        WebElement(
            element_id="btn_help",
            element_type="button",
            text="Help",
            position=(100, 100),
            size=(100, 40),
            visual_prominence=0.9,
            context_relevance=0.95,
            semantic_meaning="access help documentation"
        ),
        WebElement(
            element_id="menu_advanced",
            element_type="dropdown",
            text="Advanced Settings",
            position=(500, 150),
            size=(200, 40),
            visual_prominence=0.6,
            context_relevance=0.2,
            semantic_meaning="open advanced configuration menu"
        ),
        WebElement(
            element_id="link_api",
            element_type="link",
            text="API Documentation",
            position=(800, 700),
            size=(150, 25),
            visual_prominence=0.3,
            context_relevance=0.1,
            semantic_meaning="view API documentation"
        )
    ]

    # Rank all elements to see the reasoning
    ranked_elements = decision_maker.rank_elements(elements)

    print(f"\nUser: {persona.name}")
    print(f"Tech Savviness: {persona.cognitive.tech_savviness:.2f}")
    print(f"Product Familiarity: {persona.cognitive.product_familiarity:.2f}")
    print(f"Neuroticism: {persona.personality.neuroticism:.2f}")
    print(f"Goal: {goal.description}")

    # Display current emotion
    summary = decision_maker.get_decision_summary()
    print(f"\nCurrent Emotion: {summary['current_emotion']}")
    print(f"Emotion Intensities:")
    for emotion, intensity in summary['emotion_intensities'].items():
        print(f"  {emotion}: {intensity:.3f}")

    print(f"\n--- Element Rankings ---")
    for i, score in enumerate(ranked_elements, 1):
        print(f"\n{i}. {score.element.text}")
        print(f"   Score: {score.total_score:.3f}")
        print(f"   Reasoning: {score.reasoning}")

    print("\n" + "=" * 60 + "\n")


def example_multiple_interactions():
    """Example showing learning over multiple interactions"""
    print("=" * 60)
    print("EXAMPLE 3: Learning Over Multiple Interactions")
    print("=" * 60)

    # Create persona
    persona = UserPersona.create_random_persona("user_003")
    decision_maker = SyntheticUserDecisionMaker(persona)

    # Set goal
    goal = Goal(
        goal_id="g3",
        description="Complete checkout process",
        priority=0.9,
        keywords=["checkout", "pay", "purchase", "buy"]
    )
    decision_maker.set_goal(goal)

    # Simulate multiple steps in checkout
    steps = [
        # Step 1: Add to cart
        {
            'elements': [
                WebElement("btn_add_cart", "button", "Add to Cart",
                          (500, 400), (150, 50), visual_prominence=0.9,
                          context_relevance=0.9, semantic_meaning="add item to shopping cart"),
                WebElement("btn_wishlist", "button", "Add to Wishlist",
                          (700, 400), (150, 50), visual_prominence=0.6,
                          context_relevance=0.3, semantic_meaning="save item for later"),
            ],
            'expected': 'btn_add_cart'
        },
        # Step 2: Proceed to checkout
        {
            'elements': [
                WebElement("btn_checkout", "button", "Proceed to Checkout",
                          (600, 500), (200, 60), visual_prominence=0.9,
                          context_relevance=0.95, semantic_meaning="begin checkout process"),
                WebElement("btn_continue_shopping", "button", "Continue Shopping",
                          (400, 500), (180, 50), visual_prominence=0.5,
                          context_relevance=0.2, semantic_meaning="return to shopping"),
            ],
            'expected': 'btn_checkout'
        },
        # Step 3: Complete payment
        {
            'elements': [
                WebElement("btn_pay_now", "button", "Pay Now",
                          (700, 600), (150, 60), visual_prominence=0.9,
                          context_relevance=0.95, semantic_meaning="submit payment"),
                WebElement("link_cancel", "link", "Cancel Order",
                          (500, 650), (120, 30), visual_prominence=0.4,
                          context_relevance=0.1, semantic_meaning="cancel transaction"),
            ],
            'expected': 'btn_pay_now'
        }
    ]

    print(f"\nUser: {persona.name}")
    print(f"Simulating checkout process...\n")

    for step_num, step_data in enumerate(steps, 1):
        print(f"--- Step {step_num} ---")

        # Make decision
        chosen, score = decision_maker.make_decision(step_data['elements'])

        print(f"Chosen: {chosen.text}")
        print(f"Score: {score.total_score:.3f}")

        # Check if correct choice
        is_correct = (chosen.element_id == step_data['expected'])
        print(f"Correct: {is_correct}")

        # Record outcome
        decision_maker.record_outcome(chosen, success=is_correct)

        # Display emotion after each step
        summary = decision_maker.get_decision_summary()
        print(f"Emotion: {summary['current_emotion']}")
        print(f"Energy: {summary['energy_level']:.2f}")
        print()

    # Final summary
    print("\n--- Final Summary ---")
    final_summary = decision_maker.get_decision_summary()
    print(f"Total Interactions: {final_summary['interaction_count']}")
    print(f"Final Emotion: {final_summary['current_emotion']}")
    print(f"Final Energy: {final_summary['energy_level']:.2f}")

    print("\n" + "=" * 60 + "\n")


def example_comparison_different_personas():
    """Compare how different personas make decisions"""
    print("=" * 60)
    print("EXAMPLE 4: Comparing Different Personas")
    print("=" * 60)

    # Create different personas
    personas = [
        UserPersona(
            persona_id="expert",
            name="Expert Emma",
            cognitive=CognitiveAttributes(
                cognitive_ability=0.9,
                tech_savviness=0.95,
                product_familiarity=0.9
            )
        ),
        UserPersona(
            persona_id="novice",
            name="Novice Nick",
            cognitive=CognitiveAttributes(
                cognitive_ability=0.5,
                tech_savviness=0.3,
                product_familiarity=0.2
            ),
            personality=PersonalityTraits(neuroticism=0.7)
        ),
        UserPersona(
            persona_id="impatient",
            name="Impatient Iris",
            cognitive=CognitiveAttributes(
                cognitive_ability=0.7,
                tech_savviness=0.7,
                product_familiarity=0.6
            ),
            behavioral=BehavioralTraits(patience=0.2, impulsivity=0.8)
        )
    ]

    # Same goal for all
    goal = Goal(
        goal_id="g4",
        description="Configure advanced settings",
        priority=0.7,
        keywords=["settings", "configure", "advanced", "options"]
    )

    # Same elements for all
    elements = [
        WebElement("btn_quick_setup", "button", "Quick Setup Wizard",
                  (400, 300), (200, 60), visual_prominence=0.9,
                  context_relevance=0.6, semantic_meaning="guided setup process"),
        WebElement("btn_advanced", "button", "Advanced Configuration",
                  (650, 300), (200, 60), visual_prominence=0.7,
                  context_relevance=0.9, semantic_meaning="manual advanced configuration"),
        WebElement("link_help", "link", "Help & Documentation",
                  (100, 100), (150, 30), visual_prominence=0.5,
                  context_relevance=0.4, semantic_meaning="access help resources"),
    ]

    print("\nSame Goal: Configure advanced settings")
    print("Same Elements available\n")

    # Compare decisions
    for persona in personas:
        decision_maker = SyntheticUserDecisionMaker(persona)
        decision_maker.set_goal(goal)

        chosen, score = decision_maker.make_decision(elements)

        summary = decision_maker.get_decision_summary()

        print(f"--- {persona.name} ---")
        print(f"Tech Savviness: {persona.cognitive.tech_savviness:.2f}")
        print(f"Product Familiarity: {persona.cognitive.product_familiarity:.2f}")
        print(f"Emotion: {summary['current_emotion']}")
        print(f"Chose: {chosen.text}")
        print(f"Score: {score.total_score:.3f}")
        print(f"Top Reason: {score.reasoning}")
        print()

    print("=" * 60 + "\n")


if __name__ == "__main__":
    # Run all examples
    example_basic_usage()
    example_confused_user()
    example_multiple_interactions()
    example_comparison_different_personas()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
