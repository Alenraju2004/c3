# Adaptive Learning Coach - AI Agent

An intelligent learning adaptation system that uses groq to analyze learner state and recommend personalized learning strategies.

## Overview

The Adaptive Learning Coach is a 5-hour hackathon prototype that demonstrates **contextual AI reasoning** for adaptive learning. Rather than using simplistic score-based rules, the system employs groq to analyze a learner's complete history and context, then recommends one of three strategies:

- **`reinforce`** — Learner needs more practice and targeted support
- **`advance`** — Learner is ready for harder/new material
- **`mentor`** — Learner needs personalized intervention and one-on-one support

## Architecture

```
Learner State + New Event
          ↓
    Python Context Builder
          ↓
        groq LLM
          ↓
  Structured Decision
          ↓
 Python Action Executor
          ↓
  Generate Content & Update State
          ↓
      Agent Result
```

The architecture follows an **OBSERVE → REASON → DECIDE → ACT → UPDATE** workflow.

## Project Structure

```
agent/
├── __init__.py              # Public API export
├── agent.py                 # Main orchestration (public API: analyze_learner)
├── llm.py                   # groq integration
├── prompts.py               # System and decision prompts
├── context.py               # Context builder
├── actions.py               # Action execution (reinforce/advance/mentor)
├── state.py                 # Deterministic state management
└── schemas.py               # Pydantic validation

test_scenarios.py            # Full integration tests (requires API key)
test_unit.py                 # Unit tests (no API required)
requirements.txt             # Dependencies
.env.example                 # Environment template
README.md                    # This file
```

## Installation

1. **Clone/setup the project:**
   ```bash
   cd c:\Users\alenr\Documents\c3
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   # PowerShell
   $env:GROQ_API_KEY = "your-groq-api-key"
    $env:GROQ_MODEL = "openai/gpt-oss-120b"
   
   # Or create .env file with:
   GROQ_API_KEY=your-groq-api-key
    GROQ_MODEL=openai/gpt-oss-120b
   ```

## Usage

### Basic API

```python
from agent.agent import analyze_learner

# Define learner state
learner = {
    "student_id": "STU001",
    "name": "Alex",
    "course": "Python Programming",
    "current_topic": "Recursion",
    "recent_scores": [82, 76, 68],
    "average_score": 75.3,
    "weak_topics": [],
    "attempts_current_topic": 3,
    "avg_time_minutes": 22,
    "help_requests": 2,
    "current_streak_days": 5,
    "longest_streak_days": 14,
    "previous_decisions": ["advance", "reinforce"],
    "reinforcement_count": 1,
    "certification_progress": 0.65,
    "deadline_days": 20
}

# Define new learning event
new_event = {
    "topic": "Recursion",
    "score": 48,
    "time_minutes": 32,
    "attempts": 1,
    "help_requested": True,
    "completed": True
}

# Get adaptive recommendation
result = analyze_learner(learner, new_event)

# Result structure:
# {
#     "decision": "mentor",
#     "confidence": 0.87,
#     "reasons": ["...", "...", "..."],
#     "action": {
#         "type": "mentor_checkin",
#         "topic": "Recursion"
#     },
#     "generated_content": "Personalized message...",
#     "updated_learner": { ... updated state ... }
# }
```

### Learner State Structure

**Required fields:**

```python
learner = {
    # Identity
    "student_id": "STU001",
    "name": "Alex",
    "course": "Python Programming",
    "current_topic": "Recursion",
    
    # Performance
    "recent_scores": [82, 76, 68],  # Chronological list
    "average_score": 75.3,
    "weak_topics": ["Recursion"],    # Persistent unresolved issues
    
    # Learning behaviour
    "attempts_current_topic": 3,
    "avg_time_minutes": 22,
    "help_requests": 2,
    
    # Engagement
    "current_streak_days": 5,
    "longest_streak_days": 14,
    
    # History
    "previous_decisions": ["advance", "reinforce"],
    "reinforcement_count": 1,
    
    # Goals
    "certification_progress": 0.65,  # 0.0 to 1.0
    "deadline_days": 20
}
```

### Learning Event Structure

**Required fields:**

```python
new_event = {
    "topic": "Recursion",
    "score": 48,              # 0-100
    "time_minutes": 32,       # Elapsed time
    "attempts": 1,            # Number of attempts
    "help_requested": True,   # Boolean
    "completed": True         # Boolean
}
```

## Running Tests

### Unit Tests (No API Key Required)

Tests state management, validation, and weak topic tracking:

```bash
python test_unit.py
```

Output shows:
- Schema validation
- State update verification
- Weak topic tracking

### Integration Tests (Requires API Key)

Full end-to-end tests with groq:

```bash
# Set API key first
$env:GROQ_API_KEY = "your-key"

python test_scenarios.py
```

Tests include:
1. **Strong Learner** → Expect `advance`
2. **Struggling Learner** → Expect `reinforce`
3. **At-Risk Learner** → Expect `mentor`
4. **Clearing Weak Topic** → Should remove topic from weak_topics

## Key Design Principles

### 1. Dynamic Reasoning

The agent doesn't use hardcoded rules like:
- `score < 50 → mentor`
- `score > 80 → advance`

Instead, groq interprets the **complete context** and makes reasoned decisions.

### 2. Multidimensional Performance

Decisions consider:
- Recent score trajectory (not just the new score)
- Average performance over time
- Weak topics and their history
- Engagement and streak patterns
- Help requests and previous interventions
- Deadline pressure
- Certification progress

### 3. Time as Contextual Signal

Time interpretation depends on correctness:
- High score + low time → Strong efficiency ✓
- Low score + low time → Possibly rushing ✗
- High score + high time → Mastery but inefficient
- Low score + high time → Genuine struggle

### 4. Weak Topic Tracking

Weak topics are **persistent state**, not recalculated scores:
- Added when learner scores < 80 on a topic
- Removed only when learner scores ≥ 80 on that topic
- Represents unresolved difficulties

### 5. Previous Interventions Matter

If reinforcement has been applied multiple times without improvement, `mentor` becomes more appropriate.

### 6. Trajectory Over Snapshots

A declining trend (90 → 88 → 86 → 84) is interpreted differently than an improving trend (55 → 62 → 71 → 79), even if individual scores are similar.

## System Prompt Highlights

The groq system prompt emphasizes:

✓ **Do** consider ALL factors holistically  
✓ **Do** interpret time contextually with performance  
✓ **Do** weight trajectory above single scores  
✓ **Do** track previous interventions  
✓ **Do** consider deadline and certification pressure  
✗ **Don't** use simplistic threshold rules  
✗ **Don't** interpret low time as poor performance  
✗ **Don't** base decisions on one metric alone

## Output Format

The agent returns structured JSON:

```json
{
    "decision": "reinforce|advance|mentor",
    "confidence": 0.87,
    "reasons": [
        "Recent quiz performance is declining.",
        "The learner is struggling with a known weak topic.",
        "Latest attempt is below the learner's recent average."
    ],
    "action": {
        "type": "reinforcement|advanced_challenge|mentor_checkin",
        "topic": "Recursion"
    },
    "generated_content": "Personalized message or practice material...",
    "updated_learner": { ... complete updated learner state ... }
}
```

## Action Execution

### Reinforce
Generates targeted practice for the weak/current topic:
- Core concept review
- Guided practice with explanations
- Self-check exercises

### Advance
Generates challenging material for mastery consolidation:
- Deep dive on current topic
- Complex multi-step problems
- Mini-project introduction
- Preview of next topic

### Mentor
Generates personalized check-in message:
- Diagnosis of learner's situation
- One-on-one support plan
- Resource recommendations
- Encouragement and next steps

## Error Handling

The agent validates:
- ✓ Learner record structure and field values
- ✓ Learning event data
- ✓ groq API connectivity and response format
- ✓ Decision validity (one of: reinforce, advance, mentor)
- ✓ Confidence scores (0.0 to 1.0)
- ✓ Action structure and type

Errors are raised with clear messages:
```python
try:
    result = analyze_learner(learner, new_event)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"API or processing error: {e}")
```

## Mastery Threshold

The system uses a configurable mastery threshold:

```python
MASTERY_THRESHOLD = 80.0  # in agent/state.py
```

A score at or above this threshold on a weak topic indicates the topic has been cleared/mastered.

## Configuration

### Environment Variables

```bash
GROQ_API_KEY         # Your groq API key (required)
GROQ_MODEL           # Model name (default: openai/gpt-oss-120b)
```

### Customization Points

- **Mastery threshold:** `agent/state.py` → `MASTERY_THRESHOLD`
- **System prompt:** `agent/prompts.py` → `SYSTEM_PROMPT`
- **Decision prompt template:** `agent/prompts.py` → `DECISION_PROMPT_TEMPLATE`
- **Action content generation:** `agent/actions.py` → Action functions

## Integration with Streamlit UI

The agent exposes a clean Python interface for Streamlit integration:

```python
from agent.agent import analyze_learner, get_learner_summary

# Get decision
result = analyze_learner(learner, new_event)

# Display to user
print(f"Decision: {result['decision']}")
print(f"Confidence: {result['confidence']:.0%}")
print(f"Reasons: {result['reasons']}")
print(f"Message:\n{result['generated_content']}")

# Update stored learner state
learner = result['updated_learner']
```

## Scope & Limitations

### Out of Scope
- LangChain, CrewAI, AutoGen
- Vector databases, RAG, embeddings
- Fine-tuning
- Multiple autonomous agents
- Production deployment
- Database infrastructure

### Scope
- Persistent learner state management
- Contextual groq reasoning
- Three adaptive decisions
- Structured output
- State transitions
- Deterministic validation

## Testing Checklist

- [x] Schema validation (Pydantic)
- [x] State management (score tracking, weak topics, streaks)
- [x] Context building
- [x] groq integration (mocked and real)
- [x] Action execution
- [x] Error handling
- [x] Test scenarios (strong, struggling, at-risk learners)
- [x] Weak topic clearing logic
- [x] Previous decisions tracking

## Next Steps for Hackathon Demo

1. **Set groq API key** in environment
2. **Run unit tests** to verify state management: `python test_unit.py`
3. **Run integration tests** with real groq: `python test_scenarios.py`
4. **Integrate with Streamlit UI** using the `analyze_learner()` API
5. **Demonstrate different learner scenarios** to show contextual reasoning
6. **Show weak topic tracking** (add/clear)
7. **Highlight decision reasoning** (reasons field)

## Key Files for Streamlit Integration

| File | Purpose | Use For |
|------|---------|---------|
| `agent/agent.py` | Main orchestration | Call `analyze_learner(learner, new_event)` |
| `agent/schemas.py` | Validation | Import `LearnerRecord`, `LearningEvent` for type hints |
| `agent/state.py` | State management | Reference `get_learner_context_summary()` |
| `test_scenarios.py` | Examples | Reference learner structures |

## License

Hackathon project - 5 hours

---

**Built to demonstrate adaptive learning through contextual LLM reasoning.**
