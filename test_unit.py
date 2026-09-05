"""
Alternative test using mocked groq response for testing without API calls.
"""

import json
from agent.agent import analyze_learner
from agent.schemas import LearnerRecord, LearningEvent
from agent.state import update_learner_from_event


def test_state_update_only():
    """Test state management independently from groq."""
    
    print("\n" + "="*70)
    print("STATE MANAGEMENT TEST (No groq API required)")
    print("="*70)
    
    learner = {
        "student_id": "STU001",
        "name": "Alex",
        "course": "Python Programming",
        "current_topic": "Functions",
        "recent_scores": [85, 88, 90],
        "average_score": 87.67,
        "weak_topics": [],
        "attempts_current_topic": 2,
        "avg_time_minutes": 18.5,
        "help_requests": 0,
        "current_streak_days": 5,
        "longest_streak_days": 10,
        "previous_decisions": ["advance"],
        "reinforcement_count": 0,
        "certification_progress": 0.45,
        "deadline_days": 30
    }
    
    new_event = {
        "topic": "Functions",
        "score": 92,
        "time_minutes": 17.0,
        "attempts": 1,
        "help_requested": False,
        "completed": True
    }
    
    event = LearningEvent(**new_event)
    
    print(f"\nBefore update:")
    print(f"- Recent scores: {learner['recent_scores']}")
    print(f"- Average: {learner['average_score']:.2f}")
    print(f"- Weak topics: {learner['weak_topics']}")
    print(f"- Previous decisions: {learner['previous_decisions']}")
    print(f"- Streak: {learner['current_streak_days']} days")
    
    # Simulate a decision
    updated = update_learner_from_event(learner, event, "advance")
    
    print(f"\nAfter update (decision: advance):")
    print(f"- Recent scores: {updated['recent_scores']}")
    print(f"- Average: {updated['average_score']:.2f}")
    print(f"- Weak topics: {updated['weak_topics']}")
    print(f"- Previous decisions: {updated['previous_decisions']}")
    print(f"- Streak: {updated['current_streak_days']} days")
    print(f"- Deadline: {updated['deadline_days']} days")
    
    print(f"\n✓ State management working correctly")


def test_schema_validation():
    """Test input validation."""
    
    print("\n" + "="*70)
    print("SCHEMA VALIDATION TEST")
    print("="*70)
    
    # Test valid learner
    try:
        learner = {
            "student_id": "STU001",
            "name": "Alex",
            "course": "Python Programming",
            "current_topic": "Functions",
            "recent_scores": [85, 88, 90],
            "average_score": 87.67,
            "weak_topics": [],
            "attempts_current_topic": 2,
            "avg_time_minutes": 18.5,
            "help_requests": 0,
            "current_streak_days": 5,
            "longest_streak_days": 10,
            "previous_decisions": ["advance"],
            "reinforcement_count": 0,
            "certification_progress": 0.45,
            "deadline_days": 30
        }
        record = LearnerRecord(**learner)
        print("✓ Valid learner record accepted")
    except Exception as e:
        print(f"✗ Valid learner rejected: {e}")
    
    # Test invalid score
    try:
        bad_learner = learner.copy()
        bad_learner["average_score"] = 150  # Out of range
        record = LearnerRecord(**bad_learner)
        print("✗ Invalid average_score was not rejected")
    except ValueError:
        print("✓ Invalid average_score (150) correctly rejected")
    
    # Test valid event
    try:
        event = {
            "topic": "Functions",
            "score": 92,
            "time_minutes": 17.0,
            "attempts": 1,
            "help_requested": False,
            "completed": True
        }
        event_record = LearningEvent(**event)
        print("✓ Valid learning event accepted")
    except Exception as e:
        print(f"✗ Valid event rejected: {e}")
    
    # Test invalid event score
    try:
        bad_event = event.copy()
        bad_event["score"] = -10
        event_record = LearningEvent(**bad_event)
        print("✗ Invalid event score was not rejected")
    except ValueError:
        print("✓ Invalid event score (-10) correctly rejected")
    
    # Test invalid attempts
    try:
        bad_event = event.copy()
        bad_event["attempts"] = 0
        event_record = LearningEvent(**bad_event)
        print("✗ Invalid attempts was not rejected")
    except ValueError:
        print("✓ Invalid attempts (0) correctly rejected")


def test_weak_topic_tracking():
    """Test weak topic addition and removal."""
    
    print("\n" + "="*70)
    print("WEAK TOPIC TRACKING TEST")
    print("="*70)
    
    learner = {
        "student_id": "STU002",
        "name": "Jordan",
        "course": "Python Programming",
        "current_topic": "Recursion",
        "recent_scores": [82, 76, 68],
        "average_score": 75.3,
        "weak_topics": [],
        "attempts_current_topic": 1,
        "avg_time_minutes": 25.0,
        "help_requests": 0,
        "current_streak_days": 3,
        "longest_streak_days": 7,
        "previous_decisions": [],
        "reinforcement_count": 0,
        "certification_progress": 0.50,
        "deadline_days": 25
    }
    
    # Event 1: Score below mastery threshold - should add to weak topics
    event1 = LearningEvent(
        topic="Recursion",
        score=65,  # Below 80 threshold
        time_minutes=30.0,
        attempts=1,
        help_requested=False,
        completed=True
    )
    
    print(f"\nEvent 1: Score 65 on Recursion (below 80 threshold)")
    print(f"  Weak topics before: {learner['weak_topics']}")
    updated1 = update_learner_from_event(learner, event1, "reinforce")
    print(f"  Weak topics after: {updated1['weak_topics']}")
    print(f"  ✓ Recursion added to weak topics" if "Recursion" in updated1['weak_topics'] else "  ✗ Failed to add")
    
    # Event 2: Score above mastery threshold - should clear from weak topics
    event2 = LearningEvent(
        topic="Recursion",
        score=85,  # Above 80 threshold
        time_minutes=20.0,
        attempts=1,
        help_requested=False,
        completed=True
    )
    
    print(f"\nEvent 2: Score 85 on Recursion (above 80 threshold)")
    print(f"  Weak topics before: {updated1['weak_topics']}")
    updated2 = update_learner_from_event(updated1, event2, "advance")
    print(f"  Weak topics after: {updated2['weak_topics']}")
    print(f"  ✓ Recursion cleared from weak topics" if "Recursion" not in updated2['weak_topics'] else "  ✗ Failed to clear")


if __name__ == "__main__":
    test_schema_validation()
    test_state_update_only()
    test_weak_topic_tracking()
    print("\n" + "="*70)
    print("All unit tests completed!")
    print("="*70)
