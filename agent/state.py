"""Deterministic learner state management and updates."""

from typing import Dict, Any, List
from agent.schemas import LearnerRecord, LearningEvent


# Configurable mastery threshold
MASTERY_THRESHOLD = 80.0


def calculate_average_score(scores: List[float]) -> float:
    """Calculate average of recent scores."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def update_weak_topics(
    learner: Dict[str, Any],
    new_event: LearningEvent,
    cleared: bool = False
) -> None:
    """
    Update weak_topics list based on event outcome.
    
    Args:
        learner: Learner dictionary to update
        new_event: The learning event
        cleared: Whether the learner cleared/mastered the topic
    """
    topic = new_event.topic
    
    if cleared:
        # Remove topic from weak_topics if present
        if topic in learner["weak_topics"]:
            learner["weak_topics"].remove(topic)
    else:
        # Add topic to weak_topics if score is below mastery threshold
        # and not already in the list
        if new_event.score < MASTERY_THRESHOLD and topic not in learner["weak_topics"]:
            learner["weak_topics"].append(topic)


def update_streak(learner: Dict[str, Any], event_completed: bool) -> None:
    """
    Update current and longest streak based on event completion.
    
    Args:
        learner: Learner dictionary to update
        event_completed: Whether the event was completed
    """
    if event_completed:
        learner["current_streak_days"] += 1
        if learner["current_streak_days"] > learner["longest_streak_days"]:
            learner["longest_streak_days"] = learner["current_streak_days"]
    else:
        learner["current_streak_days"] = 0


def update_learner_from_event(
    learner: Dict[str, Any],
    new_event: LearningEvent,
    decision: str
) -> Dict[str, Any]:
    """
    Apply all deterministic updates to learner state.
    
    Args:
        learner: Learner record
        new_event: New learning event
        decision: The groq decision (reinforce/advance/mentor)
    
    Returns:
        Updated learner dictionary
    """
    # Append score to recent_scores
    learner["recent_scores"].append(new_event.score)
    
    # Update average score
    learner["average_score"] = calculate_average_score(learner["recent_scores"])
    
    # Update current topic if different
    if new_event.topic != learner["current_topic"]:
        learner["current_topic"] = new_event.topic
        learner["attempts_current_topic"] = new_event.attempts
    else:
        learner["attempts_current_topic"] = new_event.attempts
    
    # Update average time
    if learner["avg_time_minutes"] == 0.0:
        learner["avg_time_minutes"] = new_event.time_minutes
    else:
        # Simple rolling average (could be more sophisticated)
        learner["avg_time_minutes"] = (
            (learner["avg_time_minutes"] + new_event.time_minutes) / 2
        )
    
    # Update help requests
    if new_event.help_requested:
        learner["help_requests"] += 1
    
    # Determine if topic was cleared (score above mastery threshold)
    topic_cleared = new_event.score >= MASTERY_THRESHOLD
    
    # Update weak topics
    update_weak_topics(learner, new_event, cleared=topic_cleared)
    
    # Update streak
    update_streak(learner, new_event.completed)
    
    # Record the decision
    learner["previous_decisions"].append(decision)
    
    # Update decision-specific counters
    if decision == "reinforce":
        learner["reinforcement_count"] += 1
    
    # Decrement deadline if applicable
    if learner["deadline_days"] > 0:
        learner["deadline_days"] -= 1
    
    return learner


def get_learner_context_summary(learner: Dict[str, Any]) -> str:
    """
    Create a summary of learner context for display/debugging.
    
    Args:
        learner: Learner record
    
    Returns:
        Formatted summary string
    """
    recent_scores_str = " → ".join(
        str(int(s)) for s in learner["recent_scores"][-5:]
    ) if learner["recent_scores"] else "No scores"
    
    summary = f"""
Learner: {learner['name']} ({learner['student_id']})
Course: {learner['course']}
Current Topic: {learner['current_topic']}

Performance:
- Recent scores: {recent_scores_str}
- Average: {learner['average_score']:.1f}
- Weak topics: {', '.join(learner['weak_topics']) if learner['weak_topics'] else 'None'}

Behavior:
- Attempts (current topic): {learner['attempts_current_topic']}
- Avg time: {learner['avg_time_minutes']:.1f} minutes
- Help requests: {learner['help_requests']}

Engagement:
- Current streak: {learner['current_streak_days']} days
- Longest streak: {learner['longest_streak_days']} days

Adaptation:
- Reinforcement count: {learner['reinforcement_count']}
- Previous decisions: {', '.join(learner['previous_decisions']) if learner['previous_decisions'] else 'None'}

Progress:
- Certification: {learner['certification_progress']*100:.1f}%
- Days to deadline: {learner['deadline_days']}
"""
    return summary.strip()
