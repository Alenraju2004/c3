"""Test scenarios for Adaptive Learning Coach agent."""

import os
import json
from agent.agent import analyze_learner, get_learner_summary


# Test Scenario 1: Strong learner ready to advance
def test_strong_learner_advance():
    """
    Strong learner with:
    - High scores
    - Improving trajectory
    - Low attempts
    - Good engagement
    
    Expected: advance
    """
    learner = {
        "student_id": "STU001",
        "name": "Alex",
        "course": "Python Programming",
        "current_topic": "Functions",
        "recent_scores": [85, 88, 90, 92],
        "average_score": 88.75,
        "weak_topics": [],
        "attempts_current_topic": 1,
        "avg_time_minutes": 18.5,
        "help_requests": 0,
        "current_streak_days": 7,
        "longest_streak_days": 14,
        "previous_decisions": ["advance"],
        "reinforcement_count": 0,
        "certification_progress": 0.45,
        "deadline_days": 30
    }
    
    new_event = {
        "topic": "Functions",
        "score": 95,
        "time_minutes": 16.0,
        "attempts": 1,
        "help_requested": False,
        "completed": True
    }
    
    print("\n" + "="*70)
    print("TEST 1: STRONG LEARNER - EXPECT ADVANCE")
    print("="*70)
    print(f"\nLearner: {learner['name']} ({learner['student_id']})")
    print(f"Course: {learner['course']} | Topic: {learner['current_topic']}")
    print(f"\nPre-event context:")
    print(f"- Recent scores: {' → '.join(str(int(s)) for s in learner['recent_scores'])}")
    print(f"- Average: {learner['average_score']:.1f}/100")
    print(f"- Attempts: {learner['attempts_current_topic']}")
    print(f"- Streak: {learner['current_streak_days']} days")
    print(f"- Help requests: {learner['help_requests']}")
    
    print(f"\nNew event:")
    print(f"- Score: {new_event['score']}")
    print(f"- Time: {new_event['time_minutes']} min")
    print(f"- Completed: {new_event['completed']}")
    
    return learner, new_event


# Test Scenario 2: Struggling learner needing reinforcement
def test_struggling_learner_reinforce():
    """
    Struggling learner with:
    - Declining scores
    - Weak on current topic
    - Multiple attempts
    - Increased time spent
    
    Expected: reinforce
    """
    learner = {
        "student_id": "STU002",
        "name": "Jordan",
        "course": "Python Programming",
        "current_topic": "Recursion",
        "recent_scores": [82, 76, 68],
        "average_score": 75.3,
        "weak_topics": ["Recursion"],
        "attempts_current_topic": 3,
        "avg_time_minutes": 28.5,
        "help_requests": 2,
        "current_streak_days": 2,
        "longest_streak_days": 10,
        "previous_decisions": ["advance"],
        "reinforcement_count": 0,
        "certification_progress": 0.55,
        "deadline_days": 25
    }
    
    new_event = {
        "topic": "Recursion",
        "score": 62,
        "time_minutes": 35.0,
        "attempts": 1,
        "help_requested": True,
        "completed": True
    }
    
    print("\n" + "="*70)
    print("TEST 2: STRUGGLING LEARNER - EXPECT REINFORCE")
    print("="*70)
    print(f"\nLearner: {learner['name']} ({learner['student_id']})")
    print(f"Course: {learner['course']} | Topic: {learner['current_topic']}")
    print(f"\nPre-event context:")
    print(f"- Recent scores: {' → '.join(str(int(s)) for s in learner['recent_scores'])}")
    print(f"- Average: {learner['average_score']:.1f}/100")
    print(f"- Weak topics: {', '.join(learner['weak_topics'])}")
    print(f"- Attempts: {learner['attempts_current_topic']}")
    print(f"- Avg time: {learner['avg_time_minutes']:.1f} min")
    print(f"- Help requests: {learner['help_requests']}")
    
    print(f"\nNew event:")
    print(f"- Score: {new_event['score']}")
    print(f"- Time: {new_event['time_minutes']} min")
    print(f"- Attempts: {new_event['attempts']}")
    print(f"- Help requested: {new_event['help_requested']}")
    
    return learner, new_event


# Test Scenario 3: At-risk learner needing mentor intervention
def test_atrisk_learner_mentor():
    """
    At-risk learner with:
    - Repeated poor performance
    - Previous reinforcement without improvement
    - Multiple help requests
    - Deadline pressure
    
    Expected: mentor
    """
    learner = {
        "student_id": "STU003",
        "name": "Casey",
        "course": "Python Programming",
        "current_topic": "Trees",
        "recent_scores": [55, 62, 48, 51],
        "average_score": 54.0,
        "weak_topics": ["Recursion", "Trees"],
        "attempts_current_topic": 4,
        "avg_time_minutes": 40.0,
        "help_requests": 5,
        "current_streak_days": 1,
        "longest_streak_days": 8,
        "previous_decisions": ["advance", "reinforce", "reinforce"],
        "reinforcement_count": 2,
        "certification_progress": 0.35,
        "deadline_days": 10
    }
    
    new_event = {
        "topic": "Trees",
        "score": 45,
        "time_minutes": 45.0,
        "attempts": 1,
        "help_requested": True,
        "completed": True
    }
    
    print("\n" + "="*70)
    print("TEST 3: AT-RISK LEARNER - EXPECT MENTOR")
    print("="*70)
    print(f"\nLearner: {learner['name']} ({learner['student_id']})")
    print(f"Course: {learner['course']} | Topic: {learner['current_topic']}")
    print(f"\nPre-event context:")
    print(f"- Recent scores: {' → '.join(str(int(s)) for s in learner['recent_scores'])}")
    print(f"- Average: {learner['average_score']:.1f}/100")
    print(f"- Weak topics: {', '.join(learner['weak_topics'])}")
    print(f"- Attempts: {learner['attempts_current_topic']}")
    print(f"- Avg time: {learner['avg_time_minutes']:.1f} min")
    print(f"- Help requests: {learner['help_requests']}")
    print(f"- Previous interventions: {', '.join(learner['previous_decisions'])}")
    print(f"- Reinforcement count: {learner['reinforcement_count']}")
    print(f"- Days to deadline: {learner['deadline_days']}")
    
    print(f"\nNew event:")
    print(f"- Score: {new_event['score']}")
    print(f"- Time: {new_event['time_minutes']} min")
    print(f"- Help requested: {new_event['help_requested']}")
    
    return learner, new_event


# Test Scenario 4: Learner clearing a weak topic
def test_learner_clearing_weak_topic():
    """
    Learner who previously struggled but is now mastering the topic.
    
    Weak topic should be removed from weak_topics after clearing.
    May advance if performance is consistently strong.
    
    Expected: advance or reinforce with confidence that topic is cleared
    """
    learner = {
        "student_id": "STU004",
        "name": "Morgan",
        "course": "Python Programming",
        "current_topic": "Loops",
        "recent_scores": [65, 70, 75, 78],
        "average_score": 72.0,
        "weak_topics": ["Loops"],
        "attempts_current_topic": 3,
        "avg_time_minutes": 22.0,
        "help_requests": 1,
        "current_streak_days": 4,
        "longest_streak_days": 7,
        "previous_decisions": ["reinforce", "reinforce"],
        "reinforcement_count": 2,
        "certification_progress": 0.50,
        "deadline_days": 20
    }
    
    new_event = {
        "topic": "Loops",
        "score": 85,
        "time_minutes": 18.0,
        "attempts": 1,
        "help_requested": False,
        "completed": True
    }
    
    print("\n" + "="*70)
    print("TEST 4: LEARNER CLEARING WEAK TOPIC")
    print("="*70)
    print(f"\nLearner: {learner['name']} ({learner['student_id']})")
    print(f"Course: {learner['course']} | Topic: {learner['current_topic']}")
    print(f"\nPre-event context:")
    print(f"- Recent scores: {' → '.join(str(int(s)) for s in learner['recent_scores'])}")
    print(f"- Average: {learner['average_score']:.1f}/100")
    print(f"- Weak topics: {', '.join(learner['weak_topics'])}")
    print(f"- Previous interventions: {', '.join(learner['previous_decisions'])}")
    print(f"- Reinforcement count: {learner['reinforcement_count']}")
    print(f"- Streak: {learner['current_streak_days']} days (improving)")
    
    print(f"\nNew event:")
    print(f"- Score: {new_event['score']} (ABOVE MASTERY THRESHOLD of 80)")
    print(f"- Time: {new_event['time_minutes']} min (efficient)")
    print(f"- This should clear 'Loops' from weak_topics")
    
    return learner, new_event


def run_all_tests():
    """Run all test scenarios."""
    tests = [
        ("Strong Learner (Advance)", test_strong_learner_advance),
        ("Struggling Learner (Reinforce)", test_struggling_learner_reinforce),
        ("At-Risk Learner (Mentor)", test_atrisk_learner_mentor),
        ("Clearing Weak Topic", test_learner_clearing_weak_topic),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            learner, new_event = test_func()
            
            print(f"\n→ Calling analyze_learner()...")
            result = analyze_learner(learner, new_event)
            
            print(f"\n✓ DECISION: {result['decision'].upper()}")
            print(f"  Confidence: {result['confidence']:.2f}")
            print(f"\n  Reasons:")
            for reason in result['reasons']:
                print(f"  - {reason}")
            
            print(f"\n  Action: {result['action']['type']} on {result['action'].get('topic', 'N/A')}")
            
            print(f"\n  Generated Content Preview:")
            content_preview = result['generated_content'][:200].replace('\n', ' ')
            print(f"  {content_preview}...")
            
            updated = result['updated_learner']
            print(f"\n  Updated Learner State:")
            print(f"  - Recent scores: {' → '.join(str(int(s)) for s in updated['recent_scores'][-5:])}")
            print(f"  - Average: {updated['average_score']:.1f}/100")
            print(f"  - Weak topics: {', '.join(updated['weak_topics']) if updated['weak_topics'] else 'None'}")
            print(f"  - Previous decisions: {', '.join(updated['previous_decisions'])}")
            
            results.append({
                "test": test_name,
                "status": "PASS",
                "decision": result['decision']
            })
            
        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            results.append({
                "test": test_name,
                "status": "FAIL",
                "error": str(e)
            })
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    for r in results:
        status_symbol = "✓" if r['status'] == "PASS" else "✗"
        decision_or_error = r.get('decision', r.get('error', 'Unknown'))
        print(f"{status_symbol} {r['test']:40} [{decision_or_error}]")


if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY environment variable not set.")
        print("Please set it before running tests:")
        print("  $env:GROQ_API_KEY='your-api-key'  # PowerShell")
        print("  set GROQ_API_KEY=your-api-key     # Command Prompt")
        exit(1)
    
    run_all_tests()
