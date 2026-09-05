"""Build comprehensive context for groq decision-making."""

from typing import Dict, Any
from agent.schemas import LearnerRecord, LearningEvent


def build_learner_context(
    learner: Dict[str, Any],
    new_event: LearningEvent
) -> Dict[str, Any]:
    """
    Build comprehensive context for groq to analyze.
    
    This includes the learner's persistent state and the new event.
    
    Args:
        learner: Current learner record
        new_event: New learning event
    
    Returns:
        Context dictionary for groq
    """
    context = {
        "learner": {
            "identity": {
                "student_id": learner["student_id"],
                "name": learner["name"],
                "course": learner["course"],
                "current_topic": learner["current_topic"],
            },
            "performance": {
                "recent_scores": learner["recent_scores"],
                "average_score": learner["average_score"],
                "weak_topics": learner["weak_topics"],
            },
            "behavior": {
                "attempts_current_topic": learner["attempts_current_topic"],
                "avg_time_minutes": learner["avg_time_minutes"],
                "help_requests": learner["help_requests"],
            },
            "engagement": {
                "current_streak_days": learner["current_streak_days"],
                "longest_streak_days": learner["longest_streak_days"],
            },
            "adaptation": {
                "previous_decisions": learner["previous_decisions"],
                "reinforcement_count": learner["reinforcement_count"],
            },
            "goals": {
                "certification_progress": learner["certification_progress"],
                "deadline_days": learner["deadline_days"],
            },
        },
        "new_event": {
            "topic": new_event.topic,
            "score": new_event.score,
            "time_minutes": new_event.time_minutes,
            "attempts": new_event.attempts,
            "help_requested": new_event.help_requested,
            "completed": new_event.completed,
        },
    }
    return context


def format_context_for_prompt(context: Dict[str, Any]) -> str:
    """
    Format context dictionary into readable text for groq prompt.
    
    Args:
        context: Context dictionary from build_learner_context
    
    Returns:
        Formatted text representation
    """
    learner = context["learner"]
    event = context["new_event"]
    
    recent_scores_str = " → ".join(
        str(int(s)) for s in learner["performance"]["recent_scores"]
    ) if learner["performance"]["recent_scores"] else "No prior scores"
    
    formatted = f"""
LEARNER CONTEXT
===============

Identity:
- Student ID: {learner['identity']['student_id']}
- Name: {learner['identity']['name']}
- Course: {learner['identity']['course']}
- Current Topic: {learner['identity']['current_topic']}

Performance Trajectory:
- Recent scores: {recent_scores_str}
- Average score: {learner['performance']['average_score']:.1f}/100
- Weak topics: {', '.join(learner['performance']['weak_topics']) if learner['performance']['weak_topics'] else 'None identified'}

Learning Behavior:
- Attempts on current topic: {learner['behavior']['attempts_current_topic']}
- Average time per attempt: {learner['behavior']['avg_time_minutes']:.1f} minutes
- Total help requests: {learner['behavior']['help_requests']}

Engagement Pattern:
- Current streak: {learner['engagement']['current_streak_days']} days
- Best streak: {learner['engagement']['longest_streak_days']} days

Adaptive History:
- Previous decisions: {', '.join(learner['adaptation']['previous_decisions']) if learner['adaptation']['previous_decisions'] else 'First assessment'}
- Times reinforcement was applied: {learner['adaptation']['reinforcement_count']}

Goals & Deadlines:
- Certification progress: {learner['goals']['certification_progress']*100:.1f}%
- Days until deadline: {learner['goals']['deadline_days']}

NEW EVENT
=========
- Topic: {event['topic']}
- Score: {event['score']}/100
- Time taken: {event['time_minutes']} minutes
- Number of attempts: {event['attempts']}
- Help requested: {'Yes' if event['help_requested'] else 'No'}
- Activity completed: {'Yes' if event['completed'] else 'No'}
"""
    return formatted.strip()
