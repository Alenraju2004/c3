"""Streamlit dashboard for the AI Learning-Path Decision Agent."""

import copy

import streamlit as st

from agent.agent import analyze_learner


st.set_page_config(
    page_title="Learning Path Decision Agent",
    page_icon="LP",
    layout="wide",
    initial_sidebar_state="expanded",
)


LEARNER_PROFILES = [
    {
        "student_id": "STU001", "name": "Alex Rivera", "course": "Python Programming",
        "current_topic": "Functions", "recent_scores": [88, 91, 93, 95],
        "average_score": 91.75, "weak_topics": [], "attempts_current_topic": 1,
        "avg_time_minutes": 18.0, "help_requests": 0, "current_streak_days": 12,
        "longest_streak_days": 18, "previous_decisions": ["advance", "advance"],
        "reinforcement_count": 0, "certification_progress": 0.62, "deadline_days": 42,
    },
    {
        "student_id": "STU002", "name": "Jordan Kim", "course": "Python Programming",
        "current_topic": "Recursion", "recent_scores": [82, 76, 68, 62],
        "average_score": 72.0, "weak_topics": ["Recursion"], "attempts_current_topic": 3,
        "avg_time_minutes": 31.0, "help_requests": 3, "current_streak_days": 2,
        "longest_streak_days": 10, "previous_decisions": ["advance", "reinforce"],
        "reinforcement_count": 1, "certification_progress": 0.55, "deadline_days": 25,
    },
    {
        "student_id": "STU003", "name": "Casey Morgan", "course": "Data Structures",
        "current_topic": "Trees", "recent_scores": [55, 62, 48, 51],
        "average_score": 54.0, "weak_topics": ["Recursion", "Trees"], "attempts_current_topic": 4,
        "avg_time_minutes": 40.0, "help_requests": 5, "current_streak_days": 1,
        "longest_streak_days": 8, "previous_decisions": ["advance", "reinforce", "reinforce"],
        "reinforcement_count": 2, "certification_progress": 0.35, "deadline_days": 10,
    },
    {
        "student_id": "STU004", "name": "Morgan Lee", "course": "Python Programming",
        "current_topic": "Loops", "recent_scores": [65, 70, 75, 78],
        "average_score": 72.0, "weak_topics": ["Loops"], "attempts_current_topic": 3,
        "avg_time_minutes": 22.0, "help_requests": 1, "current_streak_days": 4,
        "longest_streak_days": 7, "previous_decisions": ["reinforce", "reinforce"],
        "reinforcement_count": 2, "certification_progress": 0.50, "deadline_days": 20,
    },
    {
        "student_id": "STU005", "name": "Priya Shah", "course": "SQL Fundamentals",
        "current_topic": "Joins", "recent_scores": [72, 78, 84, 89],
        "average_score": 80.75, "weak_topics": [], "attempts_current_topic": 2,
        "avg_time_minutes": 24.0, "help_requests": 1, "current_streak_days": 8,
        "longest_streak_days": 11, "previous_decisions": ["reinforce", "advance"],
        "reinforcement_count": 1, "certification_progress": 0.48, "deadline_days": 31,
    },
    {
        "student_id": "STU006", "name": "Sam Wilson", "course": "Web Development",
        "current_topic": "CSS Layout", "recent_scores": [92, 61, 88, 57],
        "average_score": 74.5, "weak_topics": ["CSS Layout"], "attempts_current_topic": 2,
        "avg_time_minutes": 20.0, "help_requests": 2, "current_streak_days": 5,
        "longest_streak_days": 9, "previous_decisions": ["reinforce"],
        "reinforcement_count": 1, "certification_progress": 0.41, "deadline_days": 28,
    },
    {
        "student_id": "STU007", "name": "Taylor Brooks", "course": "JavaScript",
        "current_topic": "Async Programming", "recent_scores": [48, 52, 59, 64],
        "average_score": 55.75, "weak_topics": ["Async Programming"], "attempts_current_topic": 5,
        "avg_time_minutes": 44.0, "help_requests": 4, "current_streak_days": 3,
        "longest_streak_days": 6, "previous_decisions": ["reinforce", "reinforce"],
        "reinforcement_count": 2, "certification_progress": 0.29, "deadline_days": 18,
    },
    {
        "student_id": "STU008", "name": "Jamie Chen", "course": "Data Analysis",
        "current_topic": "Pandas", "recent_scores": [86, 87, 89, 90],
        "average_score": 88.0, "weak_topics": [], "attempts_current_topic": 1,
        "avg_time_minutes": 16.0, "help_requests": 0, "current_streak_days": 16,
        "longest_streak_days": 16, "previous_decisions": ["advance", "advance", "advance"],
        "reinforcement_count": 0, "certification_progress": 0.74, "deadline_days": 55,
    },
    {
        "student_id": "STU009", "name": "Riley Adams", "course": "Python Programming",
        "current_topic": "Testing", "recent_scores": [79, 80, 81, 82],
        "average_score": 80.5, "weak_topics": [], "attempts_current_topic": 2,
        "avg_time_minutes": 27.0, "help_requests": 2, "current_streak_days": 6,
        "longest_streak_days": 13, "previous_decisions": ["reinforce", "advance"],
        "reinforcement_count": 1, "certification_progress": 0.58, "deadline_days": 36,
    },
    {
        "student_id": "STU010", "name": "Drew Patel", "course": "Algorithms",
        "current_topic": "Graph Search", "recent_scores": [94, 92, 89, 86],
        "average_score": 90.25, "weak_topics": [], "attempts_current_topic": 2,
        "avg_time_minutes": 35.0, "help_requests": 1, "current_streak_days": 9,
        "longest_streak_days": 21, "previous_decisions": ["advance", "advance"],
        "reinforcement_count": 0, "certification_progress": 0.67, "deadline_days": 40,
    },
    {
        "student_id": "STU011", "name": "Avery Smith", "course": "Cloud Fundamentals",
        "current_topic": "Networking", "recent_scores": [58, 64, 71, 77],
        "average_score": 67.5, "weak_topics": ["Networking"], "attempts_current_topic": 3,
        "avg_time_minutes": 33.0, "help_requests": 2, "current_streak_days": 7,
        "longest_streak_days": 12, "previous_decisions": ["reinforce"],
        "reinforcement_count": 1, "certification_progress": 0.38, "deadline_days": 22,
    },
    {
        "student_id": "STU012", "name": "Quinn Davis", "course": "Machine Learning",
        "current_topic": "Model Evaluation", "recent_scores": [83, 85, 84, 86],
        "average_score": 84.5, "weak_topics": [], "attempts_current_topic": 1,
        "avg_time_minutes": 29.0, "help_requests": 1, "current_streak_days": 10,
        "longest_streak_days": 14, "previous_decisions": ["advance", "reinforce"],
        "reinforcement_count": 1, "certification_progress": 0.71, "deadline_days": 47,
    },
    {
        "student_id": "STU013", "name": "Robin Garcia", "course": "Java", "current_topic": "Interfaces",
        "recent_scores": [67, 73, 69, 76], "average_score": 71.25, "weak_topics": ["Interfaces"],
        "attempts_current_topic": 3, "avg_time_minutes": 26.0, "help_requests": 3,
        "current_streak_days": 4, "longest_streak_days": 9, "previous_decisions": ["reinforce", "reinforce"],
        "reinforcement_count": 2, "certification_progress": 0.44, "deadline_days": 27,
    },
    {
        "student_id": "STU014", "name": "Cameron Wright", "course": "Cybersecurity",
        "current_topic": "Authentication", "recent_scores": [90, 88, 91, 94],
        "average_score": 90.75, "weak_topics": [], "attempts_current_topic": 1,
        "avg_time_minutes": 21.0, "help_requests": 0, "current_streak_days": 20,
        "longest_streak_days": 20, "previous_decisions": ["advance", "advance", "advance"],
        "reinforcement_count": 0, "certification_progress": 0.82, "deadline_days": 63,
    },
    {
        "student_id": "STU015", "name": "Reese Thompson", "course": "Python Programming",
        "current_topic": "Object-Oriented Design", "recent_scores": [61, 60, 58, 55],
        "average_score": 58.5, "weak_topics": ["Object-Oriented Design"], "attempts_current_topic": 4,
        "avg_time_minutes": 38.0, "help_requests": 6, "current_streak_days": 1,
        "longest_streak_days": 5, "previous_decisions": ["reinforce", "reinforce", "mentor"],
        "reinforcement_count": 2, "certification_progress": 0.31, "deadline_days": 12,
    },
]


def status_for(learner):
    """Return a concise visual status from the learner's current signals."""
    if learner["average_score"] >= 85 and not learner["weak_topics"]:
        return "Ready to advance"
    if learner["average_score"] < 65 or learner["help_requests"] >= 5:
        return "Needs mentor support"
    return "Building mastery"


def initialize_state():
    """Seed the mock database once and keep it alive across Streamlit reruns."""
    if "learners" not in st.session_state:
        st.session_state.learners = copy.deepcopy(LEARNER_PROFILES)
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "last_learner_id" not in st.session_state:
        st.session_state.last_learner_id = None


initialize_state()

st.markdown(
    """
    <style>
    :root { color-scheme: dark; }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] { background: #0f1117; color: #f4f6fb; }
    .block-container { padding-top: 2.25rem; max-width: 1280px; }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child { background: #151923; }
    [data-testid="stMetric"], [data-testid="stForm"], [data-testid="stVerticalBlockBorderWrapper"] {
        background: #1e1e2f !important;
        border: 1px solid #34384a !important;
        color: #f4f6fb !important;
        border-radius: 10px;
    }
    [data-testid="stMetric"] { padding: 14px; }
    [data-testid="stMetricLabel"], [data-testid="stMetricValue"], [data-testid="stMetricDelta"] {
        color: #f4f6fb !important;
    }
    [data-testid="stMetricLabel"] { color: #b8c0d4 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] { padding: 0.75rem; }
    [data-testid="stForm"] { padding: 1rem; }
    [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input,
    [data-testid="stSelectbox"] > div, [data-testid="stSlider"] {
        color: #f4f6fb !important;
    }
    [data-testid="stCaptionContainer"], .stMarkdown, label { color: #d6dbea; }
    .hero { padding: 1.25rem 1.5rem; border-radius: 14px; background: linear-gradient(120deg, #102a43, #1f6f8b); color: white; margin-bottom: 1.25rem; }
    .hero h1 { margin: 0; font-size: 2.1rem; }
    .hero p { margin: .35rem 0 0; color: #d9f0f4; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## Learner directory")
    learner_labels = {
        learner["student_id"]: f"{learner['name']} · {learner['course']}"
        for learner in st.session_state.learners
    }
    selected_id = st.selectbox(
        "Select a learner",
        list(learner_labels),
        format_func=lambda learner_id: learner_labels[learner_id],
    )
    selected_learner = next(
        learner for learner in st.session_state.learners
        if learner["student_id"] == selected_id
    )
    st.divider()
    st.caption("Selected learner")
    st.markdown(f"### {selected_learner['name']}")
    st.write(selected_learner["course"])
    st.metric("Current average", f"{selected_learner['average_score']:.1f}%")
    st.write(f"**Status:** {status_for(selected_learner)}")
    st.progress(selected_learner["certification_progress"], text="Certification progress")

st.markdown(
    f"""
    <div class="hero">
        <h1>AI Learning-Path Decision Agent</h1>
        <p>Real-time intervention recommendations for {selected_learner['name']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Current context")
metric_columns = st.columns(4)
metric_columns[0].metric("Average score", f"{selected_learner['average_score']:.1f}%")
metric_columns[1].metric("Current streak", f"{selected_learner['current_streak_days']} days")
metric_columns[2].metric("Help requests", selected_learner["help_requests"])
metric_columns[3].metric("Days to deadline", selected_learner["deadline_days"])

context_columns = st.columns([1.2, 1, 1])
with context_columns[0]:
    st.markdown("**Recent score trajectory**")
    st.line_chart(selected_learner["recent_scores"], height=180)
with context_columns[1]:
    st.markdown("**Weak topics**")
    if selected_learner["weak_topics"]:
        for topic in selected_learner["weak_topics"]:
            st.warning(topic)
    else:
        st.success("No unresolved weak topics")
with context_columns[2]:
    st.markdown("**Learning profile**")
    st.write(f"Average time: **{selected_learner['avg_time_minutes']:.1f} min**")
    st.write(f"Attempts on topic: **{selected_learner['attempts_current_topic']}**")
    st.write(f"Longest streak: **{selected_learner['longest_streak_days']} days**")
    st.write(f"Past decisions: **{len(selected_learner['previous_decisions'])}**")

st.divider()
st.subheader("Trigger a new learning event")
with st.form("new_event_form"):
    event_columns = st.columns([1, 1, 1, 1.2])
    with event_columns[0]:
        event_score = st.slider("Score", min_value=0, max_value=100, value=80)
    with event_columns[1]:
        event_time = st.number_input("Time spent (minutes)", min_value=0.0, value=20.0, step=1.0)
    with event_columns[2]:
        event_attempts = st.number_input("Attempts", min_value=1, value=1, step=1)
    with event_columns[3]:
        event_help = st.checkbox("Help requested", value=False)
        st.caption(f"Event topic: {selected_learner['current_topic']}")
    submitted = st.form_submit_button("Submit Event & Analyze", type="primary", use_container_width=True)

if submitted:
    new_event = {
        "topic": selected_learner["current_topic"],
        "score": event_score,
        "time_minutes": event_time,
        "attempts": event_attempts,
        "help_requested": event_help,
        "completed": True,
    }
    with st.spinner("Analyzing learner data... 🧠"):
        try:
            result = analyze_learner(selected_learner, new_event)
            updated_learner = result["updated_learner"]
            st.session_state.learners = [
                updated_learner if learner["student_id"] == selected_id else learner
                for learner in st.session_state.learners
            ]
            st.session_state.last_result = result
            st.session_state.last_learner_id = selected_id
            st.rerun()
        except Exception as error:
            st.error(f"Analysis failed: {error}")

if st.session_state.last_result and st.session_state.last_learner_id == selected_id:
    result = st.session_state.last_result
    decision = result["decision"].lower()
    st.divider()
    st.subheader("Decision recommendation")
    if decision == "advance":
        st.success("ADVANCE", icon="🚀")
    elif decision == "reinforce":
        st.warning("REINFORCE", icon="⚠️")
    else:
        st.error("MENTOR", icon="🧑‍🏫")

    result_columns = st.columns([1, 2])
    with result_columns[0]:
        st.metric("Confidence", f"{result['confidence']:.0%}")
        action = result.get("action", {})
        if isinstance(action, dict):
            st.write(f"**Action:** {action.get('type', 'N/A')}")
            st.write(f"**Topic:** {action.get('topic', selected_learner['current_topic'])}")
    with result_columns[1]:
        st.markdown("**Why this decision**")
        for reason in result["reasons"]:
            st.markdown(f"- {reason}")

    st.info(result["generated_content"], icon="💡")
