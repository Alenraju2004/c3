"""
QUICK START GUIDE - Adaptive Learning Coach AI Agent
"""

# ============================================================================
# WHAT WAS BUILT
# ============================================================================
#
# A sophisticated AI agent that analyzes learner state and recommends 
# personalized learning strategies using groq contextual reasoning.
#
# NOT a score classifier - a true adaptive coach that considers:
# - Recent score trajectory
# - Weak topic history
# - Engagement patterns
# - Previous interventions
# - Certification deadline
# - Help-seeking behavior
# - All other contextual factors
#
# ============================================================================
# KEY FILES
# ============================================================================
#
# agent/
#   agent.py          ← Main API: analyze_learner(learner, new_event)
#   llm.py            ← groq integration
#   prompts.py        ← System prompt with reasoning rules
#   context.py        ← Context builder
#   actions.py        ← Content generator (reinforce/advance/mentor)
#   state.py          ← State management
#   schemas.py        ← Validation (Pydantic)
#
# test_unit.py        ← Unit tests (no API key needed) ✓ PASSES
# test_scenarios.py   ← Integration tests (requires API key)
# example_integration.py ← Shows Streamlit integration
# README.md           ← Full documentation
#
# ============================================================================
# HOW TO USE
# ============================================================================
#
# 1. Set up environment:
#    $env:GROQ_API_KEY = "your-groq-api-key"
#    $env:GROQ_MODEL = "openai/gpt-oss-120b"  # optional
#
# 2. In your code (e.g., Streamlit):
#    from agent.agent import analyze_learner
#    
#    result = analyze_learner(learner, new_event)
#    
#    # Result contains:
#    # - decision: "reinforce" | "advance" | "mentor"
#    # - confidence: 0.87 (how confident in this decision)
#    # - reasons: ["Reason 1", "Reason 2", ...]
#    # - action: {"type": "mentor_checkin", "topic": "Recursion"}
#    # - generated_content: "Personalized message to learner..."
#    # - updated_learner: {...updated state...}
#
# 3. Display and use results:
#    print(f"Decision: {result['decision']}")
#    print(f"Why? {result['reasons']}")
#    print(f"Message:\n{result['generated_content']}")
#    
#    # Save updated learner to database
#    save_to_db(result['updated_learner'])
#
# ============================================================================
# LEARNER STRUCTURE (Required)
# ============================================================================
#
# learner = {
#     # Identity
#     "student_id": "STU001",
#     "name": "Alex",
#     "course": "Python Programming",
#     "current_topic": "Recursion",
#
#     # Performance
#     "recent_scores": [82, 76, 68],      # Most recent quizzes
#     "average_score": 75.3,               # Auto-calculated
#     "weak_topics": ["Recursion"],        # Persistent state
#
#     # Behavior
#     "attempts_current_topic": 3,
#     "avg_time_minutes": 22,
#     "help_requests": 2,
#
#     # Engagement
#     "current_streak_days": 5,
#     "longest_streak_days": 14,
#
#     # History
#     "previous_decisions": ["advance", "reinforce"],
#     "reinforcement_count": 1,
#
#     # Goals
#     "certification_progress": 0.65,      # 0.0 to 1.0
#     "deadline_days": 20
# }
#
# ============================================================================
# EVENT STRUCTURE (Required)
# ============================================================================
#
# new_event = {
#     "topic": "Recursion",
#     "score": 48,              # 0-100
#     "time_minutes": 32,       # Elapsed time
#     "attempts": 1,            # Number of attempts (≥1)
#     "help_requested": True,   # Boolean
#     "completed": True         # Boolean
# }
#
# ============================================================================
# TESTING
# ============================================================================
#
# Run unit tests (no API key required):
#   C:/Python314/python.exe test_unit.py
#
# Expected output:
#   ✓ Schema validation
#   ✓ State management
#   ✓ Weak topic tracking
#
# Run integration tests (requires GROQ_API_KEY):
#   $env:GROQ_API_KEY = "your-key"
#   C:/Python314/python.exe test_scenarios.py
#
# Show integration example:
#   C:/Python314/python.exe example_integration.py
#
# ============================================================================
# THE THREE DECISIONS
# ============================================================================
#
# 1. REINFORCE
#    When: Learner needs more practice and support
#    Why: Declining scores, below average, struggling topic
#    Action: Targeted practice material with explanations
#
# 2. ADVANCE
#    When: Learner is ready for harder/new material
#    Why: Above mastery threshold, improving, good engagement
#    Action: Advanced challenges and next-level concepts
#
# 3. MENTOR
#    When: Learner needs personalized intervention
#    Why: Repeated poor performance, previous reinforce ineffective,
#         help requests, deadline pressure
#    Action: Personalized check-in message and support plan
#
# ============================================================================
# DESIGN PRINCIPLES IMPLEMENTED
# ============================================================================
#
# ✓ Dynamic Reasoning
#   groq interprets complete context, NOT hardcoded score rules
#
# ✓ Multidimensional Performance
#   Considers trajectory, history, engagement, ALL factors together
#
# ✓ Time is Contextual
#   High score + low time = efficient ✓
#   Low score + low time = rushing ✗
#   Time never interpreted alone
#
# ✓ Trajectory Matters Most
#   90→88→86→84 (declining) vs 55→62→71→79 (improving)
#   Completely different despite similar scores
#
# ✓ Previous Interventions
#   If reinforce has been tried without improvement, mentor is better
#
# ✓ Weak Topic Tracking
#   Persistent state, not recalculated
#   Cleared only when learner scores ≥80
#
# ✓ Streak Context
#   Longer current streak = better engagement
#   But streak alone doesn't determine strategy
#
# ============================================================================
# DEPLOYMENT CONFIGURATION
# ============================================================================
#
# Customizable settings in code:
#
# agent/state.py:
#   MASTERY_THRESHOLD = 80.0   # Score to clear weak topic
#
# agent/prompts.py:
#   SYSTEM_PROMPT              # groq reasoning rules
#   DECISION_PROMPT_TEMPLATE   # Context template
#
# agent/actions.py:
#   Functions for generating reinforce/advance/mentor content
#
# ============================================================================
# STREAMLIT INTEGRATION
# ============================================================================
#
# The agent is designed for easy Streamlit integration:
#
# 1. After learner completes a quiz, collect event data
# 2. Call: result = analyze_learner(learner, new_event)
# 3. Display: decision, confidence, reasons, generated_content
# 4. Update database with: result['updated_learner']
#
# NO UI CHANGES NEEDED - just import and call the API!
#
# See example_integration.py for Streamlit code snippet
#
# ============================================================================
# ERROR HANDLING
# ============================================================================
#
# The agent validates everything:
#
# try:
#     result = analyze_learner(learner, new_event)
# except ValueError as e:
#     print(f"Validation error: {e}")  # Bad input data
# except Exception as e:
#     print(f"API error: {e}")  # groq API issue
#
# Common errors and solutions:
#   - GROQ_API_KEY not set → Set environment variable
#   - Invalid score (e.g., 150) → Ensure scores are 0-100
#   - Invalid attempts (0) → Ensure attempts ≥ 1
#   - groq connection failed → Check internet, API status
#
# ============================================================================
# EXAMPLE USAGE
# ============================================================================
#
# # Load learner from database
# learner = db.get_learner("STU001")
#
# # Learner completes a quiz
# quiz_score = 48
# quiz_time = 32
# help_was_requested = True
#
# new_event = {
#     "topic": learner["current_topic"],
#     "score": quiz_score,
#     "time_minutes": quiz_time,
#     "attempts": 1,
#     "help_requested": help_was_requested,
#     "completed": True
# }
#
# # Get adaptive recommendation
# from agent.agent import analyze_learner
# result = analyze_learner(learner, new_event)
#
# # Show results to learner
# print(f"Decision: {result['decision']}")  # "mentor"
# print(f"Reasons:")
# for r in result['reasons']:
#     print(f"  - {r}")
# print(f"\nMessage:")
# print(result['generated_content'])  # Personalized support
#
# # Update database
# db.save_learner(result['updated_learner'])
#
# ============================================================================
# ARCHITECTURE SUMMARY
# ============================================================================
#
# Input: Learner state + new event
#   ↓
# Validation: Pydantic schemas
#   ↓
# Context Building: Format learner data for groq
#   ↓
# LLM Reasoning: groq analyzes complete context
#   ↓
# Decision: One of three strategies (reinforce/advance/mentor)
#   ↓
# State Update: Deterministic Python updates
#   ↓
# Action Execution: Generate personalized content
#   ↓
# Output: Complete result with decision, reasons, content, updated state
#
# ============================================================================
# DEPENDENCIES
# ============================================================================
#
# groq              - API for LLM reasoning
# pydantic          - Input validation
# python-dotenv     - Environment variable management
#
# Installed via: pip install -r requirements.txt
#
# ============================================================================
# PERFORMANCE NOTES
# ============================================================================
#
# Execution time:
# - Validation: ~10ms
# - Context building: ~5ms
# - groq API call: ~500-2000ms (depends on network)
# - State update: ~5ms
# - Total: ~1-3 seconds per decision
#
# groq API:
# - Rate limits: Check groq documentation
# - Models available: openai/gpt-oss-120b (default)
# - Cost: Check groq pricing
#
# ============================================================================
# SUCCESS CRITERIA
# ============================================================================
#
# ✓ Agent makes contextual decisions (not rule-based)
# ✓ Considers learner trajectory and full history
# ✓ Tracks weak topics persistently
# ✓ Generates personalized content
# ✓ Updates learner state deterministically
# ✓ Returns structured decision with confidence
# ✓ Integrates cleanly with Streamlit
# ✓ Handles errors gracefully
# ✓ Validates all inputs
# ✓ No external complexity (no RAG, embeddings, etc.)
#
# ============================================================================
# GETTING STARTED NOW
# ============================================================================
#
# 1. Set environment variable:
#    $env:GROQ_API_KEY = "your-groq-api-key"
#
# 2. Test the agent:
#    C:/Python314/python.exe test_unit.py       # No API needed
#    C:/Python314/python.exe test_scenarios.py  # With API
#
# 3. Integrate with Streamlit:
#    from agent.agent import analyze_learner
#    result = analyze_learner(learner, new_event)
#
# 4. Display results to learner
#
# Done! Your adaptive learning coach is live.
#
# ============================================================================
