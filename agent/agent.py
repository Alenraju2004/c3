"""Main orchestration for Adaptive Learning Coach agent."""

import copy
from typing import Dict, Any
from agent.schemas import LearnerRecord, LearningEvent
from agent.context import build_learner_context, format_context_for_prompt
from agent.llm import get_adaptive_decision, validate_groq_decision
from agent.state import update_learner_from_event, get_learner_context_summary
from agent.actions import get_action_execution_result


def analyze_learner(learner: Dict[str, Any], new_event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main public API for the Adaptive Learning Coach agent.
    
    Analyzes the learner's persistent state and new learning event,
    uses groq to determine the best strategy, executes that strategy,
    and returns the updated learner state with recommendations.
    
    Args:
        learner: Learner record dictionary with persistent state
        new_event: New learning event dictionary
    
    Returns:
        Agent result with decision, reasons, actions, and updated learner state
    
    Raises:
        ValueError: If input validation fails
        Exception: If groq API call fails
    """
    
    # Step 1: Validate inputs
    try:
        learner_record = LearnerRecord(**learner)
    except Exception as e:
        raise ValueError(f"Invalid learner record: {str(e)}")
    
    try:
        event_record = LearningEvent(**new_event)
    except Exception as e:
        raise ValueError(f"Invalid learning event: {str(e)}")
    
    # Make a copy to avoid mutating the input
    learner = copy.deepcopy(learner)
    
    # Step 2: Build context for groq
    context = build_learner_context(learner, event_record)
    context_text = format_context_for_prompt(context)
    
    # Step 3: Get decision from groq
    try:
        decision = get_adaptive_decision(context_text)
    except Exception as e:
        raise Exception(f"Failed to get decision from groq: {str(e)}")
    
    # Step 4: Validate groq's response
    try:
        validate_groq_decision(decision)
    except ValueError as e:
        raise ValueError(f"Invalid decision from groq: {str(e)}")
    
    # Step 5: Update learner state based on the event
    updated_learner = update_learner_from_event(learner, event_record, decision["decision"])
    
    # Step 6: Execute action and generate content
    action_context = build_learner_context(updated_learner, event_record)
    action_result = get_action_execution_result(decision, action_context)
    
    # Step 7: Build final result
    result = {
        "decision": decision["decision"],
        "confidence": decision["confidence"],
        "reasons": decision["reasons"],
        "action": decision["action"],
        "generated_content": action_result["generated_content"],
        "updated_learner": updated_learner
    }
    
    return result


def get_learner_summary(learner: Dict[str, Any]) -> str:
    """
    Get a human-readable summary of learner state.
    
    Args:
        learner: Learner record dictionary
    
    Returns:
        Formatted summary string
    """
    return get_learner_context_summary(learner)
