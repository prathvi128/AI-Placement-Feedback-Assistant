
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from graph import app as workflow_app
from nodes import generate_interview_question


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="PlacementAI | Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "generated_question_input": "",
    "generated_for_role": "",
    "custom_question": "",
    "result": None,
    "total_attempts": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
:root {
    --primary: #3B82F6;
    --primary-dark: #2563EB;
    --primary-light: #60A5FA;
    --primary-soft: #DBEAFE;
    --text-primary: #1E293B;
    --text-secondary: #475569;
    --text-muted: #64748B;
    --border: #E2E8F0;
    --bg: #FFFFFF;
    --surface: #FFFFFF;
    --card-bg: #F8FAFC;
    --radius: 12px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.08);
    --shadow: 0 2px 8px rgba(0,0,0,0.08);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.1);
}

* {
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

.stApp {
    background-color: var(--bg) !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1300px;
}

p, span, label, div, li, h1, h2, h3, h4, h5, h6 {
    color: var(--text-primary);
}

.hero {
    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    padding: 40px 48px;
    border-radius: var(--radius);
    color: white;
    margin-bottom: 24px;
    box-shadow: var(--shadow-md);
}

.hero h1 {
    color: white !important;
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 16px;
    margin-bottom: 0;
    line-height: 1.6;
}

.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 20px;
    font-weight: 700;
    color: var(--primary-dark);
    margin-top: 16px;
    margin-bottom: 20px;
}

.section-heading::before {
    content: "";
    width: 4px;
    height: 20px;
    border-radius: 4px;
    background: var(--primary);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--surface);
    border-radius: var(--radius);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
    margin-bottom: 20px;
}

.stButton > button {
    border-radius: 8px;
    min-height: 44px;
    font-weight: 600;
    font-size: 15px;
    border: 1px solid var(--border);
    background-color: var(--surface);
    color: var(--text-secondary);
    transition: all 0.18s ease;
}

.stButton > button:hover {
    border-color: var(--primary);
    color: var(--primary);
    background-color: var(--primary-soft);
}

.stButton > button * {
    color: var(--text-secondary) !important;
}

.stButton > button:hover * {
    color: var(--primary) !important;
}

.stButton > button[kind="primary"] {
    background: var(--primary);
    border: none;
    box-shadow: 0 2px 8px rgba(59,130,246,0.3);
}

.stButton > button[kind="primary"] * {
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: var(--primary-dark);
    box-shadow: 0 4px 12px rgba(59,130,246,0.4);
    transform: translateY(-1px);
}

.stTextArea textarea,
.stTextInput input {
    border-radius: 8px !important;
    background-color: var(--surface) !important;
    border: 1px solid var(--border) !important;
    padding: 12px !important;
    font-size: 15px !important;
    color: var(--text-primary) !important;
    transition: border 0.18s ease, box-shadow 0.18s ease;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: var(--text-muted) !important;
    opacity: 1;
}

.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
}

.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 8px;
    border: 1px solid var(--border) !important;
    background-color: var(--surface) !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="popover"] {
    background-color: var(--surface) !important;
}

div[data-baseweb="popover"] li {
    background-color: var(--surface) !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="popover"] li:hover {
    background-color: var(--primary-soft) !important;
}

section[data-testid="stSidebar"] {
    background: var(--card-bg);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] .stMarkdown h1 {
    color: var(--primary-dark);
    font-size: 20px;
    font-weight: 800;
}

section[data-testid="stSidebar"] .stMarkdown h3,
section[data-testid="stSidebar"] .stMarkdown h4 {
    color: var(--primary-dark);
    font-size: 14px;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stCaption,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: var(--text-secondary) !important;
    font-size: 13px;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stAlert,
section[data-testid="stSidebar"] div[data-testid^="stAlertContainer"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

section[data-testid="stSidebar"] hr {
    border-color: var(--border);
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 6px !important;
}

section[data-testid="stSidebar"] div[role="radio"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 14px;
    font-weight: 500;
    transition: all 0.15s ease;
}

section[data-testid="stSidebar"] div[role="radio"] * {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] div[role="radio"]:hover {
    background-color: var(--primary-soft);
    border-color: var(--primary);
}

section[data-testid="stSidebar"] div[aria-checked="true"] {
    background: var(--primary);
    border-color: var(--primary);
}

section[data-testid="stSidebar"] div[aria-checked="true"] * {
    color: white !important;
}

section[data-testid="stSidebar"] div[data-testid="stMetric"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}

section[data-testid="stSidebar"] div[data-testid="stMetric"] label {
    color: var(--text-muted);
    font-weight: 600;
    font-size: 12px;
}

section[data-testid="stSidebar"] div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--primary-dark);
    font-size: 1.8rem;
    font-weight: 700;
}

section[data-testid="stSidebar"] .stButton > button {
    background-color: var(--surface);
    border: 1px solid var(--border);
}

section[data-testid="stSidebar"] .stButton > button * {
    color: var(--text-secondary) !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #FEE2E2;
    border-color: #F87171;
}

section[data-testid="stSidebar"] .stButton > button:hover * {
    color: #991B1B !important;
}

div[data-testid="stMetric"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
    padding: 16px 20px;
    border-radius: var(--radius);
    box-shadow: var(--shadow-sm);
}

div[data-testid="stMetric"] label {
    color: var(--text-muted);
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--primary-dark);
    font-size: 1.8rem;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 13px;
    padding-top: 32px;
    margin-top: 32px;
    border-top: 1px solid var(--border);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: var(--card-bg);
    border-bottom: 1px solid var(--border);
    padding: 6px;
    border-radius: 8px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    transition: all 0.18s ease;
}

.stTabs [data-baseweb="tab"] p {
    color: var(--text-muted) !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: var(--primary-soft);
}

.stTabs [data-baseweb="tab"]:hover p {
    color: var(--primary-dark) !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--primary-soft);
    box-shadow: inset 0 -2px 0 var(--primary);
}

.stTabs [aria-selected="true"] p {
    color: var(--primary-dark) !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

.stRadio [role="radiogroup"] {
    gap: 12px;
}

.stRadio div[role="radio"] {
    background-color: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 18px;
    font-weight: 500;
    transition: all 0.18s ease;
}

.stRadio div[role="radio"] * {
    color: var(--text-primary) !important;
}

.stRadio div[role="radio"]:hover {
    border-color: var(--primary);
    background-color: var(--primary-soft);
}

.stRadio div[aria-checked="true"] {
    background: var(--primary);
    border-color: var(--primary);
}

.stRadio div[aria-checked="true"] * {
    color: white !important;
}

.stMarkdown p {
    color: var(--text-secondary);
    line-height: 1.65;
}

.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--text-primary);
    font-weight: 700;
}

.stMarkdown strong {
    color: var(--text-primary);
    font-weight: 700;
}

.stMarkdown em {
    color: var(--primary);
}

.stMarkdown blockquote {
    border-left: 3px solid var(--primary);
    background-color: var(--primary-soft);
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    color: var(--text-secondary);
}

.stMarkdown code {
    background-color: var(--card-bg);
    border-radius: 4px;
    padding: 2px 6px;
    font-size: 14px;
    color: var(--primary-dark);
    border: 1px solid var(--border);
}

.stAlert {
    border-radius: 8px;
    border: 1px solid transparent;
    font-size: 15px;
    box-shadow: var(--shadow-sm);
}

div[data-testid="stAlertContentSuccess"],
div[data-testid="stAlertContentSuccess"] * { color: #065F46 !important; }
div[data-testid="stAlertContentInfo"],
div[data-testid="stAlertContentInfo"] * { color: var(--primary-dark) !important; }
div[data-testid="stAlertContentWarning"],
div[data-testid="stAlertContentWarning"] * { color: #92400E !important; }
div[data-testid="stAlertContentError"],
div[data-testid="stAlertContentError"] * { color: #991B1B !important; }

.stProgress > div > div > div {
    background: var(--primary);
    border-radius: 8px;
}

.stDownloadButton > button {
    background: #10B981;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.18s ease;
}

.stDownloadButton > button * {
    color: white !important;
}

.stDownloadButton > button:hover {
    background: #059669;
    box-shadow: 0 4px 12px rgba(16,185,129,0.3);
}

.streamlit-expanderHeader {
    border-radius: 8px;
    font-weight: 600;
    color: var(--text-primary);
}

details[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 8px;
    box-shadow: none;
}

.stDivider {
    border-color: var(--border);
    margin: 16px 0;
}

.stCaption {
    color: var(--text-muted) !important;
}

[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    gap: 0;
}

/* Fix for selectbox dropdown */
div[data-baseweb="select"] span {
    color: var(--text-primary) !important;
}

/* Fix for tabs content padding */
.stTabs [data-baseweb="tab-panel"] {
    padding: 16px 0;
}

/* Ensure proper spacing in containers */
.stContainer > div {
    gap: 0.5rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🎯 PlacementAI")
    st.caption("Your personal AI interview coach")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Interview Practice",
            "📊 My Evaluation",
            "ℹ️ About Project"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### ⚙️ Application Settings")

    st.caption("AI Model")
    st.success("GPT-OSS via OpenRouter")

    st.caption("Workflow Engine")
    st.info("LangGraph")

    st.caption("Monitoring")
    st.info("LangSmith")

    st.divider()

    st.metric(
        "Completed Evaluations",
        st.session_state.total_attempts
    )

    if st.button("🗑️ Reset Application", use_container_width=True):

        for key in defaults:
            if key == "total_attempts":
                st.session_state[key] = 0
            else:
                st.session_state[key] = defaults[key]

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
        "<div class=\"hero\">\n    <h1>AI Placement Feedback Assistant</h1>\n    <p>\n        Practice technical interviews, evaluate your answers,\n        discover improvement areas and become placement ready.\n    </p>\n</div>\n",
        unsafe_allow_html=True
    )


# ============================================================
# INTERVIEW PRACTICE PAGE
# ============================================================

if page == "🏠 Interview Practice":

    st.markdown(
        '<div class="section-heading">🚀 Start Your Interview Practice</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose your target job role and practise answering "
        "realistic interview questions."
    )

    # --------------------------------------------------------
    # JOB ROLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 1. Select Your Career Role")

        job_role = st.selectbox(
            "Target Job Role",
            [
                "Python Developer",
                "Data Scientist",
                "Machine Learning Engineer",
                "Full Stack Developer",
                "AI Engineer",
                "Software Developer",
                "Data Analyst",
                "Cloud Engineer"
            ],
            key="job_role"
        )

        st.caption(
            "Your interview question and evaluation will be based on this role."
        )

    # --------------------------------------------------------
    # QUESTION GENERATION
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 2. Choose Your Interview Question")

        question_mode = st.radio(
            "Question source",
            [
                "✨ Generate with AI",
                "✍️ Enter manually"
            ],
            horizontal=True
        )

        question = ""

        if question_mode == "✨ Generate with AI":

            st.info(
                "Let AI generate a technical interview question "
                "based on your selected job role."
            )

            if st.button(
                "✨ Generate Interview Question",
                type="primary",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "AI is preparing your interview question..."
                    ):

                        generated = generate_interview_question(job_role)

                        st.session_state.generated_question_input = generated
                        st.session_state.generated_for_role = job_role
                        st.session_state.result = None

                except Exception as e:

                    st.error(f"Question generation failed: {e}")

            if (
                st.session_state.generated_for_role
                and st.session_state.generated_for_role != job_role
            ):
                st.warning(
                    "The selected role has changed. Generate a new question."
                )

            question = st.text_area(
                "Your Interview Question",
                key="generated_question_input",
                height=110,
                placeholder="Generate a question to get started..."
            )

        else:

            question = st.text_area(
                "Enter Your Interview Question",
                key="custom_question",
                height=110,
                placeholder="Example: Explain the difference between a list and a tuple in Python."
            )

    # --------------------------------------------------------
    # STUDENT ANSWER
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown("### 3. Submit Your Interview Answer")

        student_answer = st.text_area(
            "Your Answer",
            height=190,
            placeholder=(
                "Write your answer here...\n\n"
                "Explain the concept clearly and include examples where possible."
            ),
            key="student_answer"
        )

        word_count = len(student_answer.split())

        st.caption(f"📝 Word count: {word_count}")

        evaluate_button = st.button(
            "🚀 Evaluate My Answer",
            type="primary",
            use_container_width=True
        )

    # --------------------------------------------------------
    # WORKFLOW EXECUTION
    # --------------------------------------------------------

    if evaluate_button:

        if not question.strip():

            st.warning("Please generate or enter an interview question.")

        elif not student_answer.strip():

            st.warning("Please enter your interview answer.")

        else:

            initial_state = {
                "job_role": job_role,
                "question": question,
                "student_answer": student_answer,
                "analysis": "",
                "score": 0,
                "feedback": "",
                "final_report": ""
            }

            try:

                with st.spinner(
                    "🤖 LangGraph is evaluating your interview answer..."
                ):

                    result = workflow_app.invoke(initial_state)

                    st.session_state.result = result
                    st.session_state.total_attempts += 1

            except Exception as e:

                st.error(f"Workflow execution failed: {e}")

    # --------------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------------

    if st.session_state.result is not None:

        result = st.session_state.result
        score = result["score"]

        st.divider()

        st.markdown(
            '<div class="section-heading">📊 Your Performance Dashboard</div>',
            unsafe_allow_html=True
        )

        # Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Interview Score",
                f"{score}/10"
            )

        with col2:
            st.metric(
                "Performance",
                "Good" if score >= 7 else "Needs Improvement"
            )

        with col3:
            st.metric(
                "Evaluation Status",
                "Completed"
            )

        st.progress(score / 10)

        if score >= 7:
            st.success(
                "Excellent work! Your answer meets the evaluation threshold."
            )
        else:
            st.warning(
                "Your answer needs improvement. Review the feedback below."
            )

        # Results tabs
        analysis_tab, feedback_tab, report_tab = st.tabs(
            [
                "🔍 Answer Analysis",
                "💡 Improvement Feedback",
                "📄 Final Report"
            ]
        )

        with analysis_tab:

            st.markdown("### Answer Analysis")

            st.write(result["analysis"])

            with st.expander("View Submitted Answer"):

                st.write(result["student_answer"])

        with feedback_tab:

            st.markdown("### Personalized Improvement Feedback")

            if result.get("feedback"):

                st.markdown(result["feedback"])

            else:

                st.success(
                    "No additional feedback required. "
                    "Your answer achieved the required score."
                )

        with report_tab:

            st.markdown("### Interview Evaluation Report")

            st.markdown(result["final_report"])

            st.download_button(
                label="⬇️ Download Evaluation Report",
                data=result["final_report"],
                file_name="placement_feedback_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.caption(
            "AI-generated feedback is intended for interview practice "
            "and does not represent an official hiring decision."
        )


# ============================================================
# EVALUATION HISTORY PAGE
# ============================================================

elif page == "📊 My Evaluation":

    st.markdown("## 📊 My Evaluation")

    if st.session_state.result is None:

        st.info(
            "No evaluation available yet. Complete an interview practice "
            "session to see your results here."
        )

    else:

        result = st.session_state.result

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Latest Score",
                f"{result['score']}/10"
            )

        with col2:

            st.metric(
                "Total Evaluations",
                st.session_state.total_attempts
            )

        st.markdown("### Latest Interview Details")

        st.write("**Job Role:**", result["job_role"])

        st.write("**Question:**", result["question"])

        st.write("**Score:**", f"{result['score']}/10")

        st.markdown("### Latest Feedback")

        if result.get("feedback"):
            st.write(result["feedback"])
        else:
            st.success("No additional improvement feedback required.")

        st.download_button(
            "⬇️ Download Latest Report",
            data=result["final_report"],
            file_name="placement_feedback_report.txt",
            mime="text/plain"
        )


# ============================================================
# ABOUT PAGE
# ============================================================

elif page == "ℹ️ About Project":

    st.markdown("## ℹ️ About PlacementAI")

    st.write(
        "PlacementAI is an AI-powered interview practice application "
        "that evaluates student answers and generates personalized feedback."
    )

    st.markdown("### Technology Stack")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        - **Python:** Programming language
        - **LangChain:** LLM integration
        - **LangGraph:** Workflow orchestration
        - **OpenRouter:** AI model access
        """)

    with col2:

        st.markdown("""
        - **Streamlit:** User interface
        - **LangSmith:** Workflow tracing
        - **GPT-OSS:** Language model
        """)

    st.markdown("### Workflow Architecture")

    st.code("""
START
  |
  v
Analyze Answer
  |
  v
Evaluate Answer
  |
  v
Conditional Routing
  |
  +---- Score < 7 ----> Generate Feedback
  |                            |
  +---- Score >= 7 ------------+
                               |
                               v
                       Generate Report
                               |
                               v
                              END
    """, language="text")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    PlacementAI | Built with LangChain, LangGraph, Streamlit and LangSmith
    <br>
    AI-powered interview preparation for students
</div>
""", unsafe_allow_html=True)
