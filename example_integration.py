"""
Example integration showing how Streamlit UI would use the Adaptive Learning Coach agent.
This file demonstrates the intended data flow and API usage.
"""

from agent.agent import analyze_learner, get_learner_summary
from agent.schemas import LearnerRecord, LearningEvent


def example_ui_workflow():
    """
    Demonstrates a typical Streamlit UI workflow.
    
    In Streamlit, this would be triggered by a form submission
    or button click after a learner completes an activity.
    """
    
    print("="*70)
    print("ADAPTIVE LEARNING COACH - STREAMLIT INTEGRATION EXAMPLE")
    print("="*70)
    
    # Step 1: UI collects learner data (typically from database/session state)
    print("\n[1] Streamlit UI loads learner from database/state...")
    
    learner = {
        "student_id": "STU001",
        "name": "Alex",
        "course": "Python Programming",
        "current_topic": "Functions",
        "recent_scores": [82, 88, 85, 90],
        "average_score": 86.25,
        "weak_topics": [],
        "attempts_current_topic": 2,
        "avg_time_minutes": 18.5,
        "help_requests": 0,
        "current_streak_days": 7,
        "longest_streak_days": 14,
        "previous_decisions": ["advance"],
        "reinforcement_count": 0,
        "certification_progress": 0.50,
        "deadline_days": 30
    }
    
    print(f"   Loaded: {learner['name']} ({learner['student_id']})")
    print(f"   Course: {learner['course']}")
    print(f"   Current topic: {learner['current_topic']}")
    
    # Step 2: UI collects new event data from learner's quiz/activity
    print("\n[2] Learner completes an activity...")
    
    new_event = {
        "topic": "Functions",
        "score": 92,
        "time_minutes": 16.0,
        "attempts": 1,
        "help_requested": False,
        "completed": True
    }
    
    print(f"   Activity completed: {new_event['topic']}")
    print(f"   Score: {new_event['score']}/100")
    print(f"   Time: {new_event['time_minutes']} minutes")
    
    # Step 3: Call the agent
    print("\n[3] Calling analyze_learner()...")
    
    try:
        result = analyze_learner(learner, new_event)
    except Exception as e:
        print(f"   ERROR: {e}")
        return
    
    # Step 4: Display results in UI
    print("\n[4] Streamlit UI displays results...\n")
    
    print("   " + "="*60)
    print(f"   ADAPTIVE LEARNING RECOMMENDATION")
    print("   " + "="*60)
    
    decision = result['decision'].upper()
    confidence_pct = result['confidence'] * 100
    
    # Color coding for different decisions
    decision_emoji = {
        "ADVANCE": "🚀",
        "REINFORCE": "📚",
        "MENTOR": "🤝"
    }
    emoji = decision_emoji.get(decision, "•")
    
    print(f"\n   {emoji} DECISION: {decision}")
    print(f"   Confidence: {confidence_pct:.0f}%")
    
    print(f"\n   WHY THIS RECOMMENDATION:")
    for i, reason in enumerate(result['reasons'], 1):
        print(f"   {i}. {reason}")
    
    print(f"\n   WHAT'S NEXT:")
    action_type = result['action']['type']
    action_type_nice = action_type.replace('_', ' ').title()
    print(f"   • {action_type_nice}")
    
    print(f"\n   PERSONALIZED MESSAGE:")
    print("   " + "-"*60)
    
    # Display first 500 chars of generated content
    content = result['generated_content']
    if len(content) > 500:
        print(f"   {content[:500]}...")
        print(f"   [... {len(content) - 500} more characters ...]")
    else:
        print(f"   {content}")
    
    print("   " + "-"*60)
    
    # Step 5: Update learner state in database
    print("\n[5] Updating learner state in database...")
    
    updated_learner = result['updated_learner']
    
    print(f"   Updated stats:")
    print(f"   • Recent scores: {' → '.join(str(int(s)) for s in updated_learner['recent_scores'][-4:])}")
    print(f"   • Average: {updated_learner['average_score']:.1f}/100")
    print(f"   • Weak topics: {', '.join(updated_learner['weak_topics']) if updated_learner['weak_topics'] else 'None'}")
    print(f"   • Current streak: {updated_learner['current_streak_days']} days")
    print(f"   • Previous decisions: {', '.join(updated_learner['previous_decisions'])}")
    print(f"   • Reinforcement count: {updated_learner['reinforcement_count']}")
    
    print("\n   ✓ Learner state saved to database")
    
    # Step 6: Show learner summary
    print("\n[6] Learner Summary (for admin panel):")
    print("\n" + get_learner_summary(updated_learner))
    
    return result


def example_streamlit_code_snippet():
    """
    Shows what actual Streamlit code might look like.
    """
    
    code = '''
# Example Streamlit app code using Adaptive Learning Coach

import streamlit as st
from agent.agent import analyze_learner

# App title
st.title("Adaptive Learning Coach")

# Load learner from session state
if "learner" not in st.session_state:
    # Load from database
    st.session_state.learner = load_learner_from_db(student_id)

# Quiz completed - show recommendation
if quiz_completed:
    # Collect event data
    new_event = {
        "topic": st.session_state.learner["current_topic"],
        "score": quiz_score,
        "time_minutes": quiz_duration / 60,
        "attempts": quiz_attempts,
        "help_requested": help_was_requested,
        "completed": quiz_was_completed
    }
    
    # Get recommendation
    result = analyze_learner(st.session_state.learner, new_event)
    
    # Display decision
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Decision", result['decision'].upper())
    with col2:
        st.metric("Confidence", f"{result['confidence']:.0%}")
    
    # Display reasons
    st.subheader("Why this recommendation?")
    for reason in result['reasons']:
        st.write(f"• {reason}")
    
    # Display personalized content
    st.subheader("Next Steps")
    st.info(result['generated_content'])
    
    # Update learner state
    st.session_state.learner = result['updated_learner']
    save_learner_to_db(st.session_state.learner)
    
    # Button for next activity
    if st.button("Continue to next activity"):
        navigate_to_next_activity()
'''
    
    print("\n" + "="*70)
    print("EXAMPLE STREAMLIT CODE")
    print("="*70)
    print(code)


if __name__ == "__main__":
    # Run the example workflow
    result = example_ui_workflow()
    
    # Show code example
    example_streamlit_code_snippet()
    
    print("\n" + "="*70)
    print("INTEGRATION SUMMARY")
    print("="*70)
    print("""
The Adaptive Learning Coach agent provides:

1. Clean Python API:
   from agent.agent import analyze_learner
   result = analyze_learner(learner, new_event)

2. Structured output:
   - decision: "advance" | "reinforce" | "mentor"
   - confidence: 0.0 to 1.0
   - reasons: list of explanation strings
   - action: dict with type and topic
   - generated_content: personalized message
   - updated_learner: complete updated state

3. No external dependencies required:
   - No vector DB
   - No RAG
   - No complex authentication
   - Just groq API key

4. Easy state management:
   - Validate inputs with Pydantic
   - Update learner state deterministically
   - Track weak topics persistently
   - Update streaks and engagement metrics

Streamlit can:
- Call analyze_learner() after each quiz
- Display the recommendation with reasons
- Show the personalized content
- Update the database with new learner state
- Track progress over time

No other changes needed to the Streamlit UI!
""")
