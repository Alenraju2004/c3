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
REINFORCEMENT PRACTICE - {topic.upper()}
{'='*50}

Hi {learner_name},

I notice you're working on **{topic}** and could use some additional practice to build confidence and mastery.

Your current performance:
- Your average score on this topic: {avg_score:.1f}%
- Attempts so far: {attempts}

Here's what we'll focus on:

1. **Core Concepts Review**
   Review the fundamental principles of {topic}
   - Start with the most basic examples
   - Work through step-by-step explanations
   - Connect to real-world applications

2. **Guided Practice**
   Work through 3-5 problems with detailed solutions
   - Each problem increases slightly in difficulty
   - Explanations provided at each step
   - Identify common mistakes to avoid

3. **Self-Check Exercises**
   Practice problems with immediate feedback
   - Try to solve independently first
   - Get instant feedback on your approach
   - Review any incorrect attempts

Take your time with these exercises. The goal is understanding, not speed.
Remember: asking questions and making mistakes is part of learning!

Ready to begin? Let's master {topic} together.
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
ADVANCED CHALLENGE - {topic.upper()}
{'='*50}

Congratulations, {learner_name}!

Your strong performance on **{topic}** shows you're ready for the next level.
You're making excellent progress toward your certification goal ({certification*100:.1f}% complete).

Here's your advanced challenge:

1. **Deep Dive Concept**
   Extend your understanding of {topic} to advanced applications
   - Real-world problem scenarios
   - Edge cases and advanced techniques
   - Connection to related topics

2. **Complex Problem Set**
   Tackle 3-5 challenging problems
   - Multi-step solutions required
   - Application of multiple concepts
   - Critical thinking and synthesis

3. **Project-Based Learning**
   Work on a mini-project that uses {topic}
   - Design and implement a solution
   - Test edge cases
   - Reflect on your approach

4. **Next Steps**
   Prepare for the next topic in the sequence
   - Overview of what comes next
   - How {topic} connects to future learning
   - Preview of key concepts

Your recent scores ({avg_score:.1f}% average) show you have the foundation to succeed here.
This challenge will deepen your expertise and prepare you for more advanced material.

Let's push your learning forward!
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
PERSONALIZED MENTOR CHECK-IN - {topic.upper()}
{'='*50}

Hi {learner_name},

I wanted to reach out personally. I've been following your progress in **{topic}**, 
and I think we should talk about what's going on.

What I'm observing:
- Your recent scores: {recent_scores_desc}
- Current average: {avg_score:.1f}%
- Help requests: {help_requests}
- Times we've provided practice support: {reinforcement_count}

Here's what I think might be happening:

{_get_mentor_diagnosis(context)}

Let's work together on this:

1. **Let's Understand the Block**
   - What part of {topic} is most confusing?
   - Are there prerequisites you'd like to review?
   - What would help you most right now?

2. **Personalized Support Plan**
   - One-on-one explanation of key concepts
   - Work through problems together
   - Build confidence step by step

3. **Check-In Schedule**
   - Regular check-ins (not just after struggling)
   - Celebrate small wins
   - Adjust strategy as needed

4. **Resources & Alternatives**
   - Different learning approaches
   - Supplementary materials
   - Peer study options

You're not behind. Sometimes learning has plateaus, and that's completely normal.
What matters is that we address it together.

I'm here for you. Let's figure this out.

What would be most helpful right now? Feel free to tell me what you need.
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
