"""groq LLM integration for adaptive learning decisions."""

import json
import os
from typing import Dict, Any
from groq import Groq
from agent.prompts import SYSTEM_PROMPT, DECISION_PROMPT_TEMPLATE
from agent.context import format_context_for_prompt


def _get_groq_client():
    """Initialize groq client with API key from environment."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable not set. "
            "Please set it before running the agent."
        )
    return Groq(api_key=api_key)


def _get_model():
    """Get the model name from environment or use default."""
    return os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")


def get_adaptive_decision(context_summary: str) -> Dict[str, Any]:
    """
    Call groq to get an adaptive learning decision.
    
    Args:
        context_summary: Formatted context string for groq
    
    Returns:
        Structured decision dictionary
    
    Raises:
        ValueError: If groq returns invalid or malformed response
        Exception: If groq API call fails
    """
    client = _get_groq_client()
    model = _get_model()
    
    # Prepare the prompt
    prompt = DECISION_PROMPT_TEMPLATE.format(context=context_summary)
    
    # Call groq
    try:
        response = client.chat.completions.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
    except Exception as e:
        raise Exception(f"groq API call failed: {str(e)}")
    
    # Extract response text
    response_text = response.choices[0].message.content or ""
    
    # Parse JSON from response
    decision = _parse_groq_response(response_text)
    
    return decision


def _parse_groq_response(response_text: str) -> Dict[str, Any]:
    """
    Parse groq's JSON response.
    
    Args:
        response_text: Raw text response from groq
    
    Returns:
        Parsed decision dictionary
    
    Raises:
        ValueError: If response is malformed or doesn't contain valid JSON
    """
    # Try to extract JSON from the response
    # groq might include markdown formatting or extra text
    json_start = response_text.find("{")
    json_end = response_text.rfind("}") + 1
    
    if json_start == -1 or json_end == 0:
        raise ValueError(
            f"No JSON found in groq response. Response: {response_text}"
        )
    
    json_str = response_text[json_start:json_end]
    
    try:
        decision = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON from groq response: {str(e)}. "
            f"Raw response: {response_text}"
        )
    
    # Validate required fields
    required_fields = {"decision", "confidence", "reasons", "action", "generated_content"}
    missing_fields = required_fields - set(decision.keys())
    
    if missing_fields:
        raise ValueError(
            f"groq response missing fields: {missing_fields}. "
            f"Response: {decision}"
        )
    
    # Validate decision value
    if decision["decision"] not in {"reinforce", "advance", "mentor"}:
        raise ValueError(
            f"Invalid decision value: {decision['decision']}. "
            f"Must be one of: reinforce, advance, mentor"
        )
    
    # Validate confidence
    try:
        confidence = float(decision["confidence"])
        if not (0 <= confidence <= 1):
            raise ValueError(
                f"Confidence must be between 0 and 1, got {confidence}"
            )
        decision["confidence"] = confidence
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid confidence value: {decision['confidence']}")
    
    # Validate reasons is a list
    if not isinstance(decision["reasons"], list) or not decision["reasons"]:
        raise ValueError(
            f"Reasons must be a non-empty list, got: {decision['reasons']}"
        )
    
    # Validate action is a dict with type and topic
    if not isinstance(decision["action"], dict):
        raise ValueError(f"Action must be a dict, got: {type(decision['action'])}")
    
    if "type" not in decision["action"]:
        raise ValueError("Action missing 'type' field")
    
    # Validate action type matches decision
    action_type = decision["action"].get("type", "")
    decision_to_action_type = {
        "reinforce": "reinforcement",
        "advance": "advanced_challenge",
        "mentor": "mentor_checkin"
    }
    
    expected_type = decision_to_action_type.get(decision["decision"])
    if action_type != expected_type:
        # Log warning but don't fail - groq might use slightly different names
        # We'll fix it in action execution
        pass
    
    return decision


def validate_groq_decision(decision: Dict[str, Any]) -> bool:
    """
    Validate that a decision has all required fields.
    
    Args:
        decision: Decision dictionary from groq
    
    Returns:
        True if valid
    
    Raises:
        ValueError: If decision is invalid
    """
    required_fields = {"decision", "confidence", "reasons", "action", "generated_content"}
    
    if not isinstance(decision, dict):
        raise ValueError(f"Decision must be a dict, got {type(decision)}")
    
    missing = required_fields - set(decision.keys())
    if missing:
        raise ValueError(f"Decision missing fields: {missing}")
    
    if decision["decision"] not in {"reinforce", "advance", "mentor"}:
        raise ValueError(f"Invalid decision: {decision['decision']}")
    
    if not isinstance(decision["confidence"], (int, float)) or not (0 <= decision["confidence"] <= 1):
        raise ValueError(f"Invalid confidence: {decision['confidence']}")
    
    if not isinstance(decision["reasons"], list) or not decision["reasons"]:
        raise ValueError(f"Invalid reasons: {decision['reasons']}")
    
    if not isinstance(decision["action"], dict) or "type" not in decision["action"]:
        raise ValueError(f"Invalid action: {decision['action']}")
    
    return True
