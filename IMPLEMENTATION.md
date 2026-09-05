# Implementation Details - Adaptive Learning Coach

## Complete Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit UI                                 │
│  (Handles user interaction, displays decisions & content)       │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ learner dict, new_event dict
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│                   analyze_learner()                             │
│                  (agent/agent.py - PUBLIC API)                 │
│                                                                 │
│  1. Validate inputs (Pydantic)                                 │
│  2. Build context for groq                                     │
│  3. Call groq with system prompt                               │
│  4. Validate groq response                                     │
│  5. Update learner state                                       │
│  6. Execute action (generate content)                          │
│  7. Return complete result                                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ↓                 ↓                 ↓
    ┌─────────┐      ┌──────────┐      ┌──────────┐
    │Validation│      │ Context  │      │   LLM    │
    │(schemas) │      │ Builder  │      │groq Call │
    └─────────┘      └──────────┘      └──────────┘
         ↓                 ↓                 ↓
    Pydantic       format_context_    get_adaptive_
    validation     for_prompt()        decision()
         │                │                │
         ├────────────────┼────────────────┤
         ↓                ↓                ↓
┌─────────────────────────────────────────────────────────────────┐
│              State Update (state.py)                            │
│                                                                 │
│  • Append score to recent_scores                               │
│  • Recalculate average_score                                   │
│  • Update weak_topics (add/remove)                             │
│  • Update attempts, time, help_requests                        │
│  • Update streak days                                          │
│  • Record decision in previous_decisions                       │
│  • Update reinforcement_count if applicable                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         ↓                                   ↓
    ┌─────────────┐              ┌──────────────────┐
    │Act Execute  │              │  Return Result   │
    │(actions.py) │              │                  │
    └─────────────┘              └──────────────────┘
         │                             │
         ├─ if "reinforce" ────────────┤
         │  Generate practice          │
         │                             │
         ├─ if "advance" ──────────────┤
         │  Generate challenges        │
         │                             │
         └─ if "mentor" ───────────────┤
            Generate support message    │
                                        ↓
                              {decision, confidence,
                               reasons, action,
                               generated_content,
                               updated_learner}
```

## Module Responsibilities

### `agent.py` - Orchestration
- **Public API**: `analyze_learner(learner, new_event)`
- **Role**: Orchestrates the entire pipeline
- **Flow**:
  1. Validates inputs using Pydantic schemas
  2. Calls context builder to format data
  3. Calls LLM to get decision
  4. Validates decision format
  5. Updates learner state
  6. Executes action
  7. Returns complete result

### `schemas.py` - Validation
- **Classes**:
  - `LearnerRecord` - Validates learner structure
  - `LearningEvent` - Validates new event
  - `Decision` - Validates groq response
  - `AgentResult` - Validates final result
- **Validators**:
  - Score range: 0-100
  - Attempts: ≥ 1
  - Certification progress: 0-1
  - Decision: one of {reinforce, advance, mentor}

### `context.py` - Context Building
- **Functions**:
  - `build_learner_context()` - Structures data for groq
  - `format_context_for_prompt()` - Formats as readable text
- **Purpose**: Prepare complete learner information for LLM reasoning
- **Output**: Text that groq can analyze

### `llm.py` - LLM Integration
- **Functions**:
  - `get_adaptive_decision()` - Main groq call
  - `_parse_groq_response()` - JSON extraction
  - `validate_groq_decision()` - Response validation
- **Features**:
  - Handles groq API initialization
  - Extracts JSON from response
  - Validates all required fields
  - Returns structured decision

### `prompts.py` - Prompting Strategy
- **Exports**:
  - `SYSTEM_PROMPT` - Core reasoning rules (700+ lines)
  - `DECISION_PROMPT_TEMPLATE` - Context template
- **Key Rules in System Prompt**:
  - Performance is multidimensional
  - Time interpretation is contextual
  - Trajectory matters more than single scores
  - Weak topics are persistent state
  - Previous interventions matter
  - Avoid simplistic threshold rules

### `state.py` - State Management
- **Functions**:
  - `update_learner_from_event()` - Main update function
  - `update_weak_topics()` - Persistent weak topic tracking
  - `update_streak()` - Engagement tracking
  - `calculate_average_score()` - Score averaging
  - `get_learner_context_summary()` - Display helper
- **Constants**:
  - `MASTERY_THRESHOLD = 80.0` - Configurable
- **Updates**:
  - All learner fields
  - Calculates derived values
  - Maintains data integrity

### `actions.py` - Content Generation
- **Functions** (one per decision type):
  - `execute_reinforce_action()` - Practice material
  - `execute_advance_action()` - Challenge material
  - `execute_mentor_action()` - Support message
  - `_get_mentor_diagnosis()` - Personalized diagnosis
- **Purpose**: Generate contextual, personalized content
- **Output**: Human-readable text for learner

## Data Flow Example

### Scenario: At-Risk Learner

```
Input:
  learner = {
    "student_id": "STU003",
    "recent_scores": [55, 62, 48, 51],  ← declining
    "weak_topics": ["Recursion", "Trees"],
    "help_requests": 5,
    "reinforcement_count": 2,
    "deadline_days": 10
  }
  
  new_event = {
    "score": 45,
    "help_requested": True
  }

Step 1: Validation
  ✓ All fields present and valid
  ✓ Scores in range 0-100
  ✓ Attempts ≥ 1
  
Step 2: Context Building
  formatted_context = """
  Recent scores: 55 → 62 → 48 → 51
  Average: 54.0/100
  Weak topics: Recursion, Trees
  Help requests: 5
  Reinforcement attempts: 2
  Days to deadline: 10
  
  NEW EVENT:
  Score: 45
  Help requested: Yes
  """

Step 3: groq Reasoning (with system prompt)
  groq analyzes:
  - Score declining despite reinforcement attempts
  - Multiple weak topics unresolved
  - High help request frequency
  - Approaching deadline
  - Previous interventions haven't worked
  
  Decision: MENTOR (confidence 0.92)
  Reasons:
  - Repeated poor performance
  - Previous reinforcement not effective
  - Multiple concurrent struggles
  - Help-seeking behavior
  - Deadline pressure

Step 4: State Update
  updated_learner = {
    recent_scores: [55, 62, 48, 51, 45],
    average_score: 52.2,
    help_requests: 6,
    current_streak_days: 0,  # Reset (not completed)
    previous_decisions: [..., "mentor"],
    deadline_days: 9
  }

Step 5: Action Execution
  content = """
  Hi Casey,
  
  I've been following your progress and want to reach out personally.
  Your recent pattern shows you're struggling:
  
  55 → 62 → 48 → 51 → 45
  
  We've tried reinforcement twice, but scores haven't improved.
  You've requested help 6 times, which tells me you're looking for support.
  
  I think we need to work together differently.
  
  [Personalized support plan...]
  """

Output: {
  "decision": "mentor",
  "confidence": 0.92,
  "reasons": [
    "Repeated poor performance...",
    "Previous reinforcement...",
    ...
  ],
  "action": {
    "type": "mentor_checkin",
    "topic": "Trees"
  },
  "generated_content": "[full message]",
  "updated_learner": {...updated state...}
}
```

## Decision Tree (Conceptual)

Note: The actual implementation uses groq reasoning, not this tree. This tree represents the TYPES of factors groq considers:

```
Analyze Learner Context
        │
        ├─ Performance Analysis
        │  ├─ Recent trajectory (improving/declining/stable)
        │  ├─ Current vs average score
        │  └─ Distance from mastery threshold
        │
        ├─ Struggle Analysis
        │  ├─ Is current topic in weak_topics?
        │  ├─ How long unresolved?
        │  └─ Multiple topics affected?
        │
        ├─ Intervention History
        │  ├─ Previous decisions
        │  ├─ Reinforcement attempts & results
        │  └─ Has anything worked?
        │
        ├─ Engagement Analysis
        │  ├─ Streak patterns
        │  ├─ Help request frequency
        │  └─ Completion rate
        │
        └─ Context Analysis
           ├─ Deadline approaching?
           ├─ Certification progress
           └─ Time efficiency
                    │
                    ↓
            HOLISTIC DECISION
            by groq based on ALL factors
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
     REINFORCE   ADVANCE    MENTOR
```

## Error Handling Strategy

```
┌─────────────────────────┐
│ analyze_learner() call  │
└────────────┬────────────┘
             │
      ┌──────↓──────┐
      │ Validation? │
      └──────┬──────┘
             │
      ┌──────↓──────────┐
      │   NO (error)    │
      └────────┬────────┘
               │
        ValueError: "Invalid learner..."
        
             │
      ┌──────↓──────┐
      │ Context OK? │
      └──────┬──────┘
             │
        YES, continue
             │
      ┌──────↓──────┐
      │ groq call?  │
      └──────┬──────┘
             │
      ┌──────↓──────────────┐
      │   FAILED (error)    │
      └────────┬────────────┘
               │
        Exception: "groq API failed..."
        
             │
      ┌──────↓────────────┐
      │ Response valid?   │
      └──────┬────────────┘
             │
      ┌──────↓──────────┐
      │   NO (error)    │
      └────────┬────────┘
               │
        ValueError: "Invalid decision..."
        
             │
      ┌──────↓────────────┐
      │    STATE UPDATE   │
      └────────┬──────────┘
               │
               ↓
        ✓ Complete Result
```

## Performance Characteristics

### Time Breakdown
- Input validation: ~10ms (Pydantic)
- Context building: ~5ms (string formatting)
- groq API call: 500-2000ms (network dependent)
- State update: ~5ms (arithmetic)
- Action execution: ~5ms (string formatting)
- **Total: 1-3 seconds** (dominated by groq latency)

### Space Complexity
- Learner record: ~2KB
- Event: ~0.5KB
- Context text: ~3KB
- Decision: ~1KB
- **Total per call: ~7KB**

### groq API
- Model: openai/gpt-oss-120b (default)
- Max tokens: 1024
- System prompt: ~2000 tokens (fixed)
- Context: ~300-500 tokens (variable)
- Response: ~200-300 tokens (variable)
- **Total per call: ~2.5-3K tokens**

## State Consistency Rules

The agent maintains these invariants:

1. **recent_scores is chronological**
   - New score always appended
   - List grows with each event

2. **average_score = mean(recent_scores)**
   - Always recalculated
   - Kept in sync with scores list

3. **weak_topics is persistent**
   - Only added (if score < 80)
   - Only removed (if score ≥ 80)
   - No recalculation per event

4. **previous_decisions records all decisions**
   - Append only
   - Complete history maintained

5. **attempts_current_topic matches current topic**
   - Updated when topic changes
   - Tracks attempts for current work

6. **Streak is binary progression**
   - Increments when completed
   - Resets to 0 on non-completion
   - longest_streak never decreases

7. **reinforcement_count only increments**
   - Never decremented
   - Tracks lifetime intervention count

## Extensibility Points

The architecture allows for future enhancement:

1. **New Decision Types**
   - Add to DECISION_PROMPT_TEMPLATE
   - Add action executor function
   - Update validation

2. **Enhanced Context**
   - Add new fields to learner record
   - Update context builder
   - Update system prompt reasoning

3. **Better Content Generation**
   - Implement more sophisticated action executors
   - Generate domain-specific examples
   - Add resource recommendations

4. **Alternative LLMs**
   - Replace groq with another provider
   - Keep same interface
   - Update llm.py only

5. **Personalization**
   - Learn learner preferences
   - Tailor content generation
   - Adjust decision confidence

## Testing Strategy

### Unit Tests (`test_unit.py`)
- Schema validation
- State updates
- Weak topic tracking
- Streak updates
- No groq API required

### Integration Tests (`test_scenarios.py`)
- End-to-end flow
- Real groq decisions
- Requires API key
- Tests different learner archetypes

### Manual Testing
- Load real learner data
- Verify decisions make sense
- Check content quality
- Validate state updates

---

**Last Updated**: Hackathon Implementation Complete
