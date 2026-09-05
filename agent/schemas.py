"""Data schemas and validation for learner records and events."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator


class LearnerRecord(BaseModel):
    """Canonical learner structure."""
    
    # Identity
    student_id: str
    name: str
    course: str
    current_topic: str
    
    # Performance
    recent_scores: List[float] = Field(default_factory=list)
    average_score: float = 0.0
    weak_topics: List[str] = Field(default_factory=list)
    
    # Learning behaviour
    attempts_current_topic: int = 0
    avg_time_minutes: float = 0.0
    help_requests: int = 0
    
    # Engagement
    current_streak_days: int = 0
    longest_streak_days: int = 0
    
    # History / adaptation
    previous_decisions: List[str] = Field(default_factory=list)
    reinforcement_count: int = 0
    
    # Goal
    certification_progress: float = 0.0
    deadline_days: int = 0
    
    @validator("recent_scores")
    def validate_scores(cls, v):
        """Ensure all scores are between 0 and 100."""
        for score in v:
            if not (0 <= score <= 100):
                raise ValueError(f"Score must be between 0 and 100, got {score}")
        return v
    
    @validator("average_score")
    def validate_average(cls, v):
        """Ensure average score is valid."""
        if not (0 <= v <= 100):
            raise ValueError(f"Average score must be between 0 and 100, got {v}")
        return v
    
    @validator("certification_progress")
    def validate_progress(cls, v):
        """Ensure certification progress is between 0 and 1."""
        if not (0 <= v <= 1):
            raise ValueError(f"Certification progress must be between 0 and 1, got {v}")
        return v


class LearningEvent(BaseModel):
    """Canonical new event structure."""
    
    topic: str
    score: float
    time_minutes: float
    attempts: int
    help_requested: bool
    completed: bool
    
    @validator("score")
    def validate_event_score(cls, v):
        """Ensure event score is between 0 and 100."""
        if not (0 <= v <= 100):
            raise ValueError(f"Event score must be between 0 and 100, got {v}")
        return v
    
    @validator("time_minutes")
    def validate_time(cls, v):
        """Ensure time is positive."""
        if v < 0:
            raise ValueError(f"Time must be non-negative, got {v}")
        return v
    
    @validator("attempts")
    def validate_attempts(cls, v):
        """Ensure attempts is positive."""
        if v < 1:
            raise ValueError(f"Attempts must be at least 1, got {v}")
        return v


class Decision(BaseModel):
    """Structured groq decision."""
    
    decision: str
    confidence: float
    reasons: List[str]
    action: dict
    generated_content: str
    
    @validator("decision")
    def validate_decision(cls, v):
        """Ensure decision is one of the allowed values."""
        allowed = {"reinforce", "advance", "mentor"}
        if v not in allowed:
            raise ValueError(f"Decision must be one of {allowed}, got {v}")
        return v
    
    @validator("confidence")
    def validate_confidence(cls, v):
        """Ensure confidence is between 0 and 1."""
        if not (0 <= v <= 1):
            raise ValueError(f"Confidence must be between 0 and 1, got {v}")
        return v


class AgentResult(BaseModel):
    """Final agent result structure."""
    
    decision: str
    confidence: float
    reasons: List[str]
    action: dict
    generated_content: str
    updated_learner: dict
    
    @validator("decision")
    def validate_result_decision(cls, v):
        """Ensure decision is one of the allowed values."""
        allowed = {"reinforce", "advance", "mentor"}
        if v not in allowed:
            raise ValueError(f"Decision must be one of {allowed}, got {v}")
        return v
