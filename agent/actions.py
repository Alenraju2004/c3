"""Execute actions based on adaptive learning decisions."""

from typing import Dict, Any


def execute_reinforce_action(topic: str, learner_name: str, context: Dict[str, Any]) -> str:
    """
    Generate reinforcement practice material.
    
    Args:
        topic: The topic to reinforce
        learner_name: Name of the learner
        context: Full learner context
    
    Returns:
        Generated reinforcement content
    """
    avg_score = context["learner"]["performance"]["average_score"]
    attempts = context["learner"]["behavior"]["attempts_current_topic"]
    
    content = f"""
**Reinforcement Practice: {topic}**

- Review the core concepts and one worked example.
- Complete 3 targeted practice problems, increasing in difficulty.
- Check each solution and note one mistake to avoid next time.

Current average: **{avg_score:.1f}%** · Attempts: **{attempts}**
"""
    return content.strip()


def execute_advance_action(topic: str, learner_name: str, context: Dict[str, Any]) -> str:
    """
    Generate advanced challenge material.
    
    Args:
        topic: The current topic
        learner_name: Name of the learner
        context: Full learner context
    
    Returns:
        Generated advanced content
    """
    avg_score = context["learner"]["performance"]["average_score"]
    certification = context["learner"]["goals"]["certification_progress"]
    
    content = f"""
**Advanced Challenge: {topic}**

- Apply {topic} to one realistic, multi-step problem.
- Test two edge cases and explain your design choices.
- Summarize how this connects to the next topic.

Average: **{avg_score:.1f}%** · Certification progress: **{certification*100:.0f}%**
"""
    return content.strip()


def execute_mentor_action(topic: str, learner_name: str, context: Dict[str, Any]) -> str:
    """
    Generate personalized mentor intervention.
    
    Args:
        topic: The problematic topic
        learner_name: Name of the learner
        context: Full learner context
    
    Returns:
        Generated mentor message
    """
    avg_score = context["learner"]["performance"]["average_score"]
    help_requests = context["learner"]["behavior"]["help_requests"]
    reinforcement_count = context["learner"]["adaptation"]["reinforcement_count"]
    recent_scores = context["learner"]["performance"]["recent_scores"]
    weak_topics = context["learner"]["performance"]["weak_topics"]
    
    # Determine what type of struggle
    score_declining = (
        len(recent_scores) > 1 and recent_scores[-1] < recent_scores[-2]
    )
    
    recent_scores_desc = " → ".join(str(int(s)) for s in recent_scores[-3:])
    
    content = f"""
**Mentor Check-In: {topic}**

- Recent scores: **{recent_scores_desc}**; current average: **{avg_score:.1f}%**.
- Help requests: **{help_requests}**; reinforcement sessions: **{reinforcement_count}**.
- Next step: meet with a mentor to isolate the blocker and work through one example.

{_get_mentor_diagnosis(context)}
"""
    return content.strip()


def _get_mentor_diagnosis(context: Dict[str, Any]) -> str:
    """
    Generate a personalized diagnosis message based on learner context.
    
    Args:
        context: Full learner context
    
    Returns:
        Diagnosis text
    """
    recent_scores = context["learner"]["performance"]["recent_scores"]
    avg_score = context["learner"]["performance"]["average_score"]
    help_requests = context["learner"]["behavior"]["help_requests"]
    attempts = context["learner"]["behavior"]["attempts_current_topic"]
    current_streak = context["learner"]["engagement"]["current_streak_days"]
    reinforcement_count = context["learner"]["adaptation"]["reinforcement_count"]
    weak_topics = context["learner"]["performance"]["weak_topics"]
    current_event_score = context["new_event"]["score"]
    
    diagnoses = []
    
    # Score trajectory
    if len(recent_scores) > 1:
        if recent_scores[-1] < recent_scores[-2]:
            diagnoses.append(
                f"Your scores are trending downward, which suggests the material "
                f"may be getting harder faster than your understanding is keeping up."
            )
        elif recent_scores[-1] < avg_score:
            diagnoses.append(
                f"Your latest score ({current_event_score}) is below your average ({avg_score:.1f}), "
                f"indicating inconsistency or a difficult concept."
            )
    
    # Help requests
    if help_requests > 2:
        diagnoses.append(
            f"You've requested help {help_requests} times, which suggests you're looking "
            f"for guidance. That's good—it means you're aware of gaps."
        )
    
    # Reinforcement history
    if reinforcement_count > 1:
        diagnoses.append(
            f"We've provided reinforcement {reinforcement_count} times, but improvement "
            f"hasn't been consistent. This might mean we need a different approach."
        )
    
    # Multiple attempts
    if attempts > 3:
        diagnoses.append(
            f"You've taken {attempts} attempts at this topic. This could mean it's complex, "
            f"or that the current approach isn't working for you."
        )
    
    # Engagement
    if current_streak < 3:
        diagnoses.append(
            f"Your engagement streak is short right now. Sometimes a break helps, "
            f"but let's make sure you have the support you need to stay on track."
        )
    
    # Default if no specific diagnosis
    if not diagnoses:
        diagnoses.append(
            "Your recent performance suggests you're facing a challenge that deserves "
            "personal attention and support."
        )
    
    return "\n- ".join(diagnoses)


def get_action_execution_result(decision: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute the appropriate action based on decision.
    
    Args:
        decision: The decision from groq
        context: Structured learner and event context
    
    Returns:
        Dictionary with action_type and generated_content
    """
    action = decision["action"]
    action_type = action.get("type", "")
    learner_context = context["learner"]
    topic = action.get("topic", learner_context["identity"]["current_topic"])
    learner_name = learner_context["identity"]["name"]
    
    # Execute appropriate action
    if "reinforce" in action_type.lower():
        content = execute_reinforce_action(topic, learner_name, context)
    elif "advance" in action_type.lower():
        content = execute_advance_action(topic, learner_name, context)
    elif "mentor" in action_type.lower():
        content = execute_mentor_action(topic, learner_name, context)
    else:
        content = decision.get("generated_content", "")
    
    return {
        "action_type": action_type,
        "generated_content": content
    }
