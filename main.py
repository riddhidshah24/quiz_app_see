
import streamlit as st
from questions import get_questions
from leaderboard import save_score
from utils import check_answer

# Page config
st.set_page_config(page_title="Quiz App", page_icon="🎯", layout="centered")

# Custom CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f5f0e6;
        color: #1e3a5f;
        font-family: 'Segoe UI', sans-serif;
    }

    h1 {
        color: #1e3a5f;
        text-align: center;
        font-size: 42px;
    }

    .quiz-box {
        background-color: #dce8f2;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    .stButton > button {
        background-color: #1e3a5f;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        font-weight: bold;
    }

    .stButton > button:hover {
        background-color: #355c7d;
        color: white;
    }

    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #1e3a5f;
    }

    .score-box {
        background-color: #c9e4ca;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #1e3a5f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("General Quiz ")

# Questions
questions = get_questions()

# Session State
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

# User Name
name = st.text_input(" Enter your name")

# Quiz Questions
for i, q in enumerate(questions):
    st.markdown('<div class="quiz-box">', unsafe_allow_html=True)

    st.subheader(f"Q{i+1}: {q['question']}")

    selected = st.radio(
        "Choose your answer:",
        q["options"],
        key=f"q{i}"
    )

    st.session_state.answers[i] = selected

    st.markdown('</div>', unsafe_allow_html=True)

# Submit Button
if st.button("Submit Quiz"):
    score = 0

    for i, q in enumerate(questions):
        if check_answer(st.session_state.answers[i], q["answer"]):
            score += 1

    st.session_state.score = score
    st.session_state.submitted = True

    if name:
        save_score(name, score)

# Display Result
if st.session_state.submitted:
    st.markdown(
        f'<div class="score-box"> Your Score: {st.session_state.score}/{len(questions)}</div>',
        unsafe_allow_html=True
    )

    # Leaderboard Section
    st.markdown("##Leaderboard")

    from leaderboard import load_scores

    scores = load_scores()

    # Sort scores descending
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)

    if scores:
        for idx, entry in enumerate(scores[:5], start=1):
            st.markdown(
                f"""
                <div style='
                    background-color:#dce8f2;
                    padding:12px;
                    border-radius:10px;
                    margin-bottom:10px;
                    font-size:18px;
                    color:#1e3a5f;
                    font-weight:bold;'>
                    #{idx}  {entry['name']} — {entry['score']} points
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No scores available yet.")

# Restart Button
if st.button("Restart Quiz"):
    st.session_state.submitted = False
    st.session_state.score = 0
    st.session_state.answers = {}
    st.rerun()
